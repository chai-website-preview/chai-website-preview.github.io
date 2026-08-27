#!/usr/bin/env python3
"""
Convert a WordPress WXR export into an Astro project's content tree.

Usage:
    python3 wxr_to_astro.py export.xml out_dir
    cd out_dir/media && python3 download_media.py        # while the WP site is still live

Output layout (out_dir/):
    src/content/pages/<slug>.md
    src/content/news/<date>-<slug>.md
    src/content/blog/<date>-<slug>.md
    src/content/people/<slug>.md          photo: ../../assets/people/<slug>.jpg
    src/content/jobs/<slug>.md
    src/content.config.ts                 collection schemas (image() helper for photos / featured images)
    src/data/research.yaml                840 entries
    src/data/bibliography.yaml            226 entries
    src/data/taxonomies.yaml, menu.yaml, authors.yaml (no emails), redirects.csv
    src/assets/people/                    headshots        (go through Astro's image pipeline)
    src/assets/featured/YYYY/MM/          featured images  (go through Astro's image pipeline)
    public/app/uploads/                   inline images + PDFs, copied verbatim; old WP URLs keep working
    public/app/uploads/external/          rehosted hotlinked images
    media/manifest.csv                    every file, source URL, local target, status
    media/download_media.py               downloads, auto-orients, strips EXIF, caps size
    archive/                              drafts, private posts, authors-with-emails.yaml  (gitignored)
    astro.config.mjs, .gitignore, .github/workflows/deploy.yml, README.md, unconverted_blocks.txt

Requires: pyyaml, markdownify. The downloader additionally needs Pillow.
"""
import csv
import hashlib
import html
import json
import os
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET
from collections import defaultdict
from urllib.parse import urlparse, unquote

import yaml
from markdownify import MarkdownConverter

NS = {
    "wp": "http://wordpress.org/export/1.2/",
    "content": "http://purl.org/rss/1.0/modules/content/",
    "excerpt": "http://wordpress.org/export/1.2/excerpt/",
    "dc": "http://purl.org/dc/elements/1.1/",
}
SITE = "https://humancompatible.ai"
UPLOADS_RE = re.compile(r"https?://(?:www\.)?humancompatible\.ai/app/uploads/([^ \t\r\n\"'<>)]+)")
SIZE_SUFFIX_RE = re.compile(r"-\d+x\d+(\.[A-Za-z0-9]+)$")
FILE_EXT_RE = re.compile(r"\.(jpe?g|png|gif|webp|svg|pdf|docx?|pptx?|xlsx?|zip|txt|csv)$", re.I)
IMAGE_EXT_RE = re.compile(r"\.(jpe?g|png|gif|webp)$", re.I)

# association order used by the nav; people index should group in this order
ASSOCIATION_ORDER = [
    "Faculty", "Staff", "Researchers", "Research Fellows", "Visiting Scholars", "Alumni",
    "Affiliates", "Graduate Students", "Affiliated Graduate Students", "Undergraduate Students",
    "Interns", "Former Interns", "General Assistants", "General Assistant", "In Memoriam",
]


# ----------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------
def text(el, path, default=""):
    n = el.find(path, NS)
    return (n.text or "") if n is not None else default


def meta(item):
    out = {}
    for m in item.findall("wp:postmeta", NS):
        out.setdefault(text(m, "wp:meta_key"), []).append(text(m, "wp:meta_value"))
    return out


def meta1(m, key, default=None):
    v = m.get(key)
    return v[0] if v else default


def slugify(s):
    s = html.unescape(re.sub(r"<[^>]+>", "", s or "")).lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "untitled"


def clean_title(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()


def strip_size_suffix(url):
    return SIZE_SUFFIX_RE.sub(r"\1", url)


def safe_name(name):
    """ASCII-only, no whitespace: 'Screenshot at 8.21.04\u202fAM.png' -> 'Screenshot-at-8.21.04-AM.png'"""
    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    name = re.sub(r"[^A-Za-z0-9._-]+", "-", name)
    return re.sub(r"-{2,}", "-", name).strip("-")


def upload_rel(url):
    """https://humancompatible.ai/app/uploads/2023/10/foo-300x200.jpg -> 2023/10/foo.jpg"""
    m = UPLOADS_RE.search(html.unescape(url))
    if not m:
        return None
    rel = strip_size_suffix(unquote(m.group(1).split("?")[0]))
    d, base = os.path.split(rel)
    return os.path.join(d, safe_name(base)) if d else safe_name(base)


def external_name(url):
    p = urlparse(url)
    base = os.path.basename(unquote(p.path)) or "file"
    base = re.sub(r"[^A-Za-z0-9._-]", "_", base)[:60]
    return f"{hashlib.sha1(url.encode()).hexdigest()[:8]}-{base}"  # extension added by downloader if missing


def wp_datetime(item):
    return text(item, "wp:post_date") or None


class LiteralStr(str):
    pass


yaml.add_representer(LiteralStr, lambda d, s: d.represent_scalar("tag:yaml.org,2002:str", s, style="|"))


def dump_yaml(obj):
    return yaml.dump(obj, sort_keys=False, allow_unicode=True, width=1000, default_flow_style=False)


# ----------------------------------------------------------------------------
# Gutenberg / classic HTML -> Markdown
# ----------------------------------------------------------------------------
class Converter(MarkdownConverter):
    class Options(MarkdownConverter.DefaultOptions):
        heading_style = "ATX"
        bullets = "-"
        escape_asterisks = False
        escape_underscores = False

    def convert_figure(self, el, text, parent_tags):
        return "\n\n" + text.strip() + "\n\n"

    def convert_figcaption(self, el, text, parent_tags):
        return "\n*" + text.strip() + "*\n"

    def convert_hr(self, el, text, parent_tags):
        return "\n\n---\n\n"

    def convert_div(self, el, text, parent_tags):
        return "\n\n" + text.strip() + "\n\n"

    def convert_section(self, el, text, parent_tags):
        return "\n\n" + text.strip() + "\n\n"

    # inline elements Markdown cannot express: keep them as inline HTML
    def _keep(self, el, text, attrs=("style", "class")):
        a = "".join(f' {k}="{el.get(k)}"' for k in attrs if el.get(k))
        return f"<{el.name}{a}>{text}</{el.name}>"

    def convert_span(self, el, text, parent_tags):
        return self._keep(el, text) if el.get("style") else text

    def convert_u(self, el, text, parent_tags):
        return self._keep(el, text)

    def convert_mark(self, el, text, parent_tags):
        return self._keep(el, text)

    def convert_sup(self, el, text, parent_tags):
        return self._keep(el, text)

    def convert_sub(self, el, text, parent_tags):
        return self._keep(el, text)

    def convert_cite(self, el, text, parent_tags):
        return self._keep(el, text)

    def convert_p(self, el, text, parent_tags):
        if not text.strip() and not el.find(True):
            return "\n\n<p></p>\n\n"   # WordPress renders empty paragraphs (and their margin); keep them
        return super().convert_p(el, text, parent_tags)


BLOCK_TAGS = ("<p", "<h", "<ul", "<ol", "<div", "<blockquote", "<figure", "<table", "<hr", "<pre", "<section")


def wpautop(src):
    out = []
    for p in re.split(r"\n\s*\n", src.strip()):
        p = p.strip()
        if not p:
            continue
        out.append(p if p.lower().startswith(BLOCK_TAGS) else "<p>" + p.replace("\n", "<br/>") + "</p>")
    return "\n".join(out)


RAW_BLOCK_RE = re.compile(r"<!-- wp:(html|code|chai/[a-z0-9-]+|block)(?: [^>]*?)?-->(.*?)<!-- /wp:\1 -->", re.S)


def html_to_markdown(src, label, unconverted):
    if not src or not src.strip():
        return ""
    placeholders = {}

    def stash(m):
        key = f"@@RAW{len(placeholders)}@@"
        placeholders[key] = (m.group(1), m.group(2).strip())
        unconverted.append(f"### {label}  [wp:{m.group(1)}]\n{m.group(2).strip()}\n")
        return f"\n\n{key}\n\n"

    if "<!-- wp:" in src:
        src = RAW_BLOCK_RE.sub(stash, src)
        src = re.sub(r"<!-- /?wp:[^>]*-->", "", src)
    else:
        src = wpautop(src)
    src = re.sub(r'<div[^>]*class="wp-block-spacer"[^>]*></div>', "", src)
    md = Converter().convert(src)
    md = re.sub(r"\n{3,}", "\n\n", md).strip()
    md = re.sub(r"\*{4,}", "**", md)
    # WordPress lists are "tight" (<li> without <p>); markdownify separates items with blank lines,
    # which Markdown renders as loose lists. Remove blank lines between consecutive list items.
    item = r"[ \t]*(?:[-*+]|\d+\.)[ \t]"
    md = re.sub(r"\n[ \t]+\n", "\n\n", md)
    md = re.sub(rf"(^{item}.*)\n\n(?={item})", r"\1\n", md, flags=re.M)
    md = md.replace("\ufffc", "")   # stray object-replacement characters pasted from Google Docs
    for key, (kind, body) in placeholders.items():
        # raw HTML block: keep verbatim, but strip blank lines so Markdown treats it as ONE html block
        body = re.sub(r"\n[ \t]*\n+", "\n", body)
        md = md.replace(key, f"<!-- wp:{kind} (raw) -->\n{body}\n<!-- /wp:{kind} -->")
    return md



# ----------------------------------------------------------------------------
# wptexturize-lite: WordPress turns straight quotes, dashes and ellipses into
# typographic ones at render time. The export has the raw characters, so we do
# the same conversion once here, on text only (never inside tags, code or URLs).
# ----------------------------------------------------------------------------
def _texturize_text(t, prev="", nxt=""):
    """prev/nxt = the characters surrounding this chunk in the full document (for quote direction)."""
    out = []
    t = t.replace("''", "\u201d")
    CLOSERS = set(" \t\n.,;:!?)]}")
    for i, ch in enumerate(t):
        before = t[i - 1] if i else prev
        after = t[i + 1] if i + 1 < len(t) else nxt
        if ch == '"':
            opening = (before == "" or before in " \t\n([{<>\u2014-") and after not in CLOSERS
            out.append("\u201c" if opening else "\u201d")
        elif ch == "'":
            if before.isalnum() and after.isalnum():
                out.append("\u2019")                              # don’t
            elif before == "" or before in " \t\n([{<>":
                out.append("\u2018" if after.isalnum() and not (after.isdigit() and t[i+1:i+4].endswith("0s")) else "\u2019")
            else:
                out.append("\u2019")
        else:
            out.append(ch)
    t = "".join(out)
    t = t.replace("---", "\u2014").replace(" -- ", " \u2014 ").replace("--", "\u2013")
    t = re.sub(r"(?<=\S) - (?=\S)", " \u2013 ", t)    # WordPress: spaced hyphen -> en dash
    return t.replace("...", "\u2026")


def texturize(md):
    out, i, prev = [], 0, ""
    # protect fenced code, inline code, HTML tags, link/image URLs, bare URLs
    for m in re.finditer(r"```.*?```|`[^`]*`|<[^>]+>|\]\([^)]*\)|https?://\S+", md, re.S):
        chunk = md[i:m.start()]
        out.append(_texturize_text(chunk, prev, m.group(0)[0]))
        out.append(m.group(0))
        prev = ">" if m.group(0).startswith("<") else (m.group(0)[-1] if m.group(0) else prev)
        if chunk: prev = chunk[-1] if not m.group(0).startswith("<") else ">"
        i = m.end()
    out.append(_texturize_text(md[i:], prev))
    return "".join(out)


# ----------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------
def main(xml_path, out):
    root = ET.parse(xml_path).getroot()
    channel = root.find("channel")
    items = channel.findall("item")
    by_id = {text(i, "wp:post_id"): i for i in items}

    def P(*parts):
        return os.path.join(out, *parts)

    for d in ["src/content/pages", "src/content/news", "src/content/blog", "src/content/people",
              "src/content/jobs", "src/data", "src/assets/people", "src/assets/featured",
              "public/app/uploads", "media", "archive/drafts", ".github/workflows"]:
        os.makedirs(P(d), exist_ok=True)

    unconverted, media_rows, redirects = [], [], []
    new_path_by_id = {}

    # ---- authors ----------------------------------------------------------
    authors = []
    for a in channel.findall("wp:author", NS):
        authors.append({"login": text(a, "wp:author_login"),
                        "display_name": text(a, "wp:author_display_name"),
                        "email": text(a, "wp:author_email")})
    with open(P("archive/authors-with-emails.yaml"), "w") as f:
        f.write(dump_yaml(authors))
    with open(P("src/data/authors.yaml"), "w") as f:
        f.write(dump_yaml([{k: v for k, v in a.items() if k != "email"} for a in authors]))

    # ---- taxonomies -------------------------------------------------------
    taxonomies = defaultdict(list)
    for t in channel.findall("wp:term", NS):
        term = {
            "id": int(text(t, "wp:term_id")), "slug": text(t, "wp:term_slug"),
            "name": clean_title(text(t, "wp:term_name")), "parent": text(t, "wp:term_parent") or None,
            "description": text(t, "wp:term_description") or None}
        for tm in t.findall("wp:termmeta", NS):
            k = text(tm, "wp:meta_key")
            if not k.startswith("_"):
                term[k] = text(tm, "wp:meta_value")
        taxonomies[text(t, "wp:term_taxonomy")].append(term)
    for c in channel.findall("wp:category", NS):
        taxonomies["category"].append({"id": int(text(c, "wp:term_id")), "slug": text(c, "wp:category_nicename"),
                                       "name": clean_title(text(c, "wp:cat_name"))})
    taxonomies["person-association-order"] = ASSOCIATION_ORDER
    with open(P("src/data/taxonomies.yaml"), "w") as f:
        f.write(dump_yaml(dict(taxonomies)))
    with open(P("src/data/people-order.json"), "w") as f:
        json.dump(ASSOCIATION_ORDER, f, indent=2)
    with open(P("src/data/taxonomies.json"), "w") as f:
        json.dump({k: v for k, v in taxonomies.items() if isinstance(v, list)}, f, indent=2)

    # ---- attachments ------------------------------------------------------
    attachments = {}
    for it in items:
        if text(it, "wp:post_type") != "attachment":
            continue
        pid, url, m = text(it, "wp:post_id"), html.unescape(text(it, "wp:attachment_url")), meta(it)
        broken = not FILE_EXT_RE.search(url or "") or not meta1(m, "_wp_attached_file")
        attachments[pid] = {"id": pid, "url": url, "rel": upload_rel(url) if not broken else None,
                            "alt": meta1(m, "_wp_attachment_image_alt", ""),
                            "title": clean_title(text(it, "title")), "broken": broken,
                            "parent": text(it, "wp:post_parent")}

    def record(kind, url, local, used_by, status, wp_id=""):
        media_rows.append({"kind": kind, "wp_id": wp_id, "source_url": url,
                           "local_path": local or "", "used_by": used_by, "status": status})

    # every non-broken attachment lands in public/app/uploads (stable URLs); featured/headshots ALSO
    # get a copy in src/assets so Astro can optimize them.
    for a in attachments.values():
        record("attachment", a["url"], f"public/app/uploads/{a['rel']}" if a["rel"] else None,
               f"attachment parent {a['parent']}" if a["parent"] not in ("", "0") else "",
               "broken-record (file missing on server)" if a["broken"] else "ok", a["id"])

    def scan_inline(raw, label):
        for url in set(re.findall(r'(?:src|href)="([^"]+)"', raw)):
            if UPLOADS_RE.search(url):
                rel = upload_rel(url)
                if not any(a["rel"] == rel for a in attachments.values()):
                    record("inline-upload", url, f"public/app/uploads/{rel}", label,
                           "NOT in media library - verify on server")
            elif url.startswith("/assets/"):
                record("theme-asset", url, "public/app/theme" + url[len("/assets"):], label,
                       "copy from theme directory")
        for url in set(re.findall(r'<img[^>]+src="(https?://[^"]+)"', raw)):
            if "humancompatible.ai" not in url:
                record("hotlink", html.unescape(url), f"public/app/uploads/external/{external_name(url)}", label,
                       "external - download & rehost")

    def rewrite_urls(md, raw):
        md = UPLOADS_RE.sub(lambda m: "/app/uploads/" + upload_rel(m.group(0)), md)
        md = re.sub(r"https?://(?:www\.)?humancompatible\.ai(?=/|\)|\"|\s|$)", "", md)
        md = md.replace('src="/assets/', 'src="/app/theme/')
        for url in set(re.findall(r'<img[^>]+src="(https?://[^"]+)"', raw)):
            if "humancompatible.ai" not in url:
                md = md.replace(url, f"/app/uploads/external/{external_name(url)}")
        return md

    def convert_body(it, label):
        raw = text(it, "content:encoded")
        scan_inline(raw, label)
        return texturize(rewrite_urls(html_to_markdown(raw, label, unconverted), raw))

    # ---- front matter -----------------------------------------------------
    def base_fm(it):
        m = meta(it)
        raw_slug = unquote(text(it, "wp:post_name"))
        if re.fullmatch(r"[a-z0-9_.-]+", raw_slug or "") and not raw_slug.isdigit():
            slug = raw_slug                         # keep the live URL exactly as WordPress had it
        else:
            slug = slugify(text(it, "title"))       # junk slug (stray bytes, bare post id): derive from title
        fm = {"title": _texturize_text(clean_title(text(it, "title"))),
              "slug": slug,
              "date": wp_datetime(it), "status": text(it, "wp:status"),
              "author": text(it, "dc:creator"), "wp_id": int(text(it, "wp:post_id")),
              "original_url": text(it, "link")}
        old_slugs = list(m.get("_wp_old_slug", []))
        if raw_slug and raw_slug != slug:
            old_slugs.append(raw_slug)
        if old_slugs:
            fm["old_slugs"] = old_slugs
        excerpt = text(it, "excerpt:encoded").strip()
        if excerpt:
            fm["excerpt"] = _texturize_text(html.unescape(re.sub(r"<[^>]+>", "", excerpt)))
        return fm, m

    def featured(it, m, fm, asset_dir, asset_name=None, label=""):
        """Route the featured image into src/assets/<asset_dir>/ and return the content-relative path."""
        tid = meta1(m, "_thumbnail_id")
        if not tid:
            return None, None
        a = attachments.get(tid)
        if not a or a["broken"]:
            fm["featured_image_missing_id"] = int(tid)
            return None, None
        ext = os.path.splitext(a["rel"])[1].lower()
        if asset_name:
            local = f"src/assets/{asset_dir}/{asset_name}{ext}"
        else:
            local = f"src/assets/{asset_dir}/{a['rel']}"
        record("featured-image", a["url"], local, label, "ok", tid)
        # content files live at src/content/<coll>/x.md -> ../../assets/...
        return "../../" + local[len("src/"):], a["alt"]

    def write_md(coll, fname, fm, body):
        if fm.get("status") != "publish":
            path = P("archive/drafts", coll, f"{fm['wp_id']}-{fname}")
            os.makedirs(os.path.dirname(path), exist_ok=True)
        else:
            path = P("src/content", coll, fname)
        fm = {k: v for k, v in fm.items() if v not in (None, "", [])}
        with open(path, "w") as f:
            f.write("---\n" + dump_yaml(fm) + "---\n\n" + body + "\n")

    # ---- pages ------------------------------------------------------------
    for it in items:
        if text(it, "wp:post_type") != "page":
            continue
        fm, m = base_fm(it)
        tpl = meta1(m, "_wp_page_template")
        if tpl and tpl != "default":
            fm["wp_template"] = tpl
        label = f"pages:{fm['slug']}"
        img, alt = featured(it, m, fm, "featured", label=label)
        if img:
            fm["featured_image"], fm["featured_image_alt"] = img, alt or None
        write_md("pages", f"{fm['slug']}.md", fm, convert_body(it, label))
        site_path = "/" if fm["wp_id"] == 9 else f"/{fm['slug']}/"
        new_path_by_id[str(fm["wp_id"])] = site_path
        redirects.append((fm["original_url"], site_path, fm["status"]))

    # ---- posts ------------------------------------------------------------
    for it in items:
        if text(it, "wp:post_type") != "post":
            continue
        fm, m = base_fm(it)
        cats = [c.get("nicename") for c in it.findall("category") if c.get("domain") == "category"]
        fm["categories"] = cats
        section = "blog" if "blog" in cats and "news" not in cats else "news"
        label = f"{section}:{fm['slug']}"
        img, alt = featured(it, m, fm, "featured", label=label)
        if img:
            fm["featured_image"], fm["featured_image_alt"] = img, alt or None
        raw = text(it, "content:encoded")
        first_p = re.search(r"<p>(.*?)</p>", raw, re.S)          # first *unstyled* paragraph, as the theme does
        if first_p and first_p.group(1).strip():
            fm["summary_html"] = texturize(rewrite_urls(first_p.group(1).strip(), raw))
        date = (fm["date"] or "0000-00-00")[:10]
        write_md(section, f"{date}-{fm['slug']}.md", fm, convert_body(it, label))
        y, mo, d = date.split("-")
        site_path = f"/{section}/{y}/{mo}/{d}/{fm['slug']}/"
        new_path_by_id[str(fm["wp_id"])] = site_path
        redirects.append((fm["original_url"], site_path, fm["status"]))
        for old in fm.get("old_slugs", []):
            redirects.append((f"{SITE}/news/{y}/{mo}/{d}/{old}/", site_path, fm["status"]))

    # ---- people -----------------------------------------------------------
    for it in items:
        if text(it, "wp:post_type") != "people":
            continue
        fm, m = base_fm(it)
        fm = {"name": fm.pop("title"), **fm}
        role = meta1(m, "title", "").replace("\\n", "\n").strip()
        if role:
            fm["role"] = LiteralStr(role) if "\n" in role else role
        assoc = [c.text for c in it.findall("category") if c.get("domain") == "person-association"]
        fm["associations"] = assoc
        fm["sort_slug"] = unquote(text(it, "wp:post_name")) or fm["slug"]   # live site orders cards by WP post_name
        fm["menu_order"] = int(text(it, "wp:menu_order") or 0)
        label = f"people:{fm['slug']}"
        raw_bio = text(it, "content:encoded")
        fm["classic_bio"] = "<p" not in raw_bio   # no <p> tags in the stored content -> live site shows no paragraph breaks
        # the theme printed the stored content as-is (block comments aside): keep that HTML for pixel parity
        fm["bio_html"] = LiteralStr(rewrite_urls(re.sub(r"<!-- /?wp:[^>]*-->", "", raw_bio).strip(), raw_bio))
        img, _ = featured(it, m, fm, "people", asset_name=fm["slug"], label=label)
        if img:
            fm["photo"] = img
        fm["hide_photo_on_page"] = meta1(m, "cybocfi_hide_featured_image", "") == "yes"
        write_md("people", f"{fm['slug']}.md", fm, convert_body(it, label))
        site_path = f"/people/{fm['slug']}/"
        new_path_by_id[str(fm["wp_id"])] = site_path
        redirects.append((fm["original_url"], site_path, fm["status"]))

    # ---- jobs -------------------------------------------------------------
    for it in items:
        if text(it, "wp:post_type") != "jobs":
            continue
        fm, m = base_fm(it)
        fm["always_show_expanded"] = meta1(m, "always_show_expanded", "") in ("1", "yes", "true")
        fm["menu_order"] = int(text(it, "wp:menu_order") or 0)
        write_md("jobs", f"{fm['slug']}.md", fm, convert_body(it, f"jobs:{fm['slug']}"))
        site_path = f"/jobs/{fm['slug']}/"
        new_path_by_id[str(fm["wp_id"])] = site_path
        redirects.append((fm["original_url"], site_path, fm["status"]))

    # ---- research / bibliography (YAML, loaded with Astro's file() loader) --
    def collect(post_type, tax, fields):
        rows, seen_ids = [], set()
        for it in items:
            if text(it, "wp:post_type") != post_type:
                continue
            m = meta(it)
            title = _texturize_text(html.unescape(re.sub(r"<[^>]+>", "", text(it, "title") or "")))  # verbatim, incl. trailing spaces
            base = slugify(title) if title else f"untitled-{text(it, 'wp:post_id')}"
            rid = base if base not in seen_ids else f"{base}-{text(it, 'wp:post_id')}"
            seen_ids.add(rid)
            row = {"id": rid, "title": title}
            if not title:
                row["needs_review"] = "empty title"
            for f in fields:
                v = meta1(m, f)
                if v is not None:
                    v = html.unescape(v)
                    if not v.strip():
                        continue
                    if f in ("year", "priority", "imported_row"):
                        if v.strip().isdigit():
                            v = int(v)
                        else:
                            row.setdefault("needs_review", f"{f}={v!r}")
                            continue
                    row[f] = v
            cats = [c for c in it.findall("category") if c.get("domain") == tax]
            row["categories"] = [c.get("nicename") for c in cats]          # term slugs (names are not unique)
            row["category_names"] = [clean_title(c.text) for c in cats]
            body = text(it, "content:encoded").strip()
            if body:
                # kept as the HTML WordPress would render (wpautop + texturize); templates use set:html
                row["notes_html"] = texturize(rewrite_urls(body if "<p" in body else wpautop(body), body))
            row["date"], row["wp_id"] = wp_datetime(it), int(text(it, "wp:post_id"))
            rows.append(row)
        rows.sort(key=lambda r: (-(r["year"] if isinstance(r.get("year"), int) else 0), r["title"].lower()))
        return rows

    research = collect("research", "research-category", ["year", "author", "venue", "link", "imported_row"])
    bib = collect("bibliography", "bibliography-category", ["author", "url", "media", "priority", "imported_row"])
    with open(P("src/data/research.yaml"), "w") as f:
        f.write(dump_yaml(research))
    with open(P("src/data/bibliography.yaml"), "w") as f:
        f.write(dump_yaml(bib))

    # ---- menu -------------------------------------------------------------
    menu_items = {}
    for it in items:
        if text(it, "wp:post_type") != "nav_menu_item":
            continue
        m, pid = meta(it), text(it, "wp:post_id")
        obj_type, obj_id = meta1(m, "_menu_item_type"), meta1(m, "_menu_item_object_id")
        url = meta1(m, "_menu_item_url") if obj_type == "custom" else new_path_by_id.get(obj_id)
        label = clean_title(text(it, "title")) or (clean_title(text(by_id[obj_id], "title")) if obj_id in by_id else "")
        menu_items[pid] = {"label": label, "url": url, "order": int(text(it, "wp:menu_order") or 0),
                           "parent": meta1(m, "_menu_item_menu_item_parent", "0"), "children": []}
    roots = []
    for pid, mi in sorted(menu_items.items(), key=lambda kv: kv[1]["order"]):
        (menu_items[mi["parent"]]["children"] if mi["parent"] in menu_items else roots).append(mi)

    def tidy(mi):
        o = {"label": mi["label"], "url": mi["url"]}
        if mi["children"]:
            o["children"] = [tidy(c) for c in sorted(mi["children"], key=lambda c: c["order"])]
        return o

    menu = {"nav-bar": [tidy(mi) for mi in roots]}
    with open(P("src/data/menu.yaml"), "w") as f:
        f.write(dump_yaml(menu))
    with open(P("src/data/menu.json"), "w") as f:
        json.dump(menu, f, indent=2)

    # ---- redirects --------------------------------------------------------
    with open(P("src/data/redirects.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["from", "to"])
        seen = set()
        for old, new, status in redirects:
            op = urlparse(old).path
            if status == "publish" and op not in ("", "/") and op != new and (op, new) not in seen:
                seen.add((op, new))
                w.writerow([op, new])
    n_redirects = len(seen)

    # ---- media manifest ---------------------------------------------------
    seen, rows = set(), []
    for r in media_rows:
        k = (r["source_url"], r["local_path"], r["used_by"])
        if k not in seen:
            seen.add(k)
            rows.append(r)
    with open(P("media/manifest.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["kind", "wp_id", "source_url", "local_path", "used_by", "status"])
        w.writeheader()
        w.writerows(rows)
    with open(P("media/download_media.py"), "w") as f:
        f.write(DOWNLOADER)
    with open(P("unconverted_blocks.txt"), "w") as f:
        f.write("Blocks kept as raw HTML inside the Markdown. Review each by hand.\n\n" + "\n".join(unconverted))

    # ---- Astro scaffolding files -----------------------------------------
    with open(P("src/content.config.ts"), "w") as f:
        f.write(CONTENT_CONFIG)
    with open(P("astro.config.mjs"), "w") as f:
        f.write(ASTRO_CONFIG)
    with open(P(".gitignore"), "w") as f:
        f.write(GITIGNORE)
    with open(P(".github/workflows/deploy.yml"), "w") as f:
        f.write(WORKFLOW)
    with open(P("README.md"), "w") as f:
        f.write(README)

    # ---- summary ----------------------------------------------------------
    def cnt(p):
        return len([x for x in os.listdir(P(p)) if x.endswith(".md")])

    print(f"pages {cnt('src/content/pages')}  news {cnt('src/content/news')}  blog {cnt('src/content/blog')}  "
          f"people {cnt('src/content/people')}  jobs {cnt('src/content/jobs')}   "
          f"archived drafts {sum(len(fs) for _, _, fs in os.walk(P('archive/drafts')))}")
    print(f"research {len(research)}  bibliography {len(bib)}  redirects {n_redirects}  "
          f"raw blocks to review {len(unconverted)}")
    st = defaultdict(int)
    for r in rows:
        st[(r["kind"], r["status"].split(" ")[0])] += 1
    for k, v in sorted(st.items()):
        print(f"  {k[0]:15s} {k[1]:15s} {v}")


# ----------------------------------------------------------------------------
# generated files
# ----------------------------------------------------------------------------
DOWNLOADER = r'''#!/usr/bin/env python3
"""Fetch everything in manifest.csv into the project tree, then normalise images.

    python3 download_media.py [--dry-run] [--skip-download] [--max-edge 1600]

Safe to re-run: files that already exist are not re-downloaded, and images that are
already within the size cap and carry no EXIF are left untouched.

For every image (jpg/png/gif/webp) this:
  * applies the EXIF orientation, then strips ALL metadata
  * downscales so the long edge is <= --max-edge (headshots under src/assets/people: 800)
  * re-encodes JPEG q=85 progressive, PNG optimised; format is otherwise preserved
Hotlinked files with no extension get one from their detected format, and the
references inside src/content are rewritten to match.

Rows with status 'broken-record' and kind 'theme-asset' are skipped.
Requires Pillow.
"""
import csv, io, os, re, sys, time, urllib.request
from urllib.parse import quote
from PIL import Image, ImageOps

args = sys.argv[1:]
DRY = "--dry-run" in args
SKIP_DL = "--skip-download" in args
MAX_EDGE = int(args[args.index("--max-edge") + 1]) if "--max-edge" in args else 1600
HEADSHOT_EDGE = 800

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.abspath(os.path.join(here, ".."))

with open(os.path.join(here, "manifest.csv"), encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

fetched = {}        # source_url -> first local path that has it
renames = {}        # old local path -> new local path (extension added)
failed = []


def fetch(url):
    # Percent-encode anything outside the ASCII URL charset (non-breaking spaces, '·', ...)
    # without double-encoding sequences that are already %XX.
    url = quote(url, safe=":/?&=%+@#,;~")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (site migration)"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def sniff_ext(data):
    try:
        fmt = Image.open(io.BytesIO(data)).format
        return {"JPEG": ".jpg", "PNG": ".png", "GIF": ".gif", "WEBP": ".webp"}.get(fmt)
    except Exception:
        return None


for r in rows:
    url, local = r["source_url"], r["local_path"]
    if not local or r["status"].startswith("broken") or r["kind"] == "theme-asset":
        continue
    dest = os.path.join(root, local)
    has_ext = bool(re.search(r"\.[A-Za-z0-9]{2,5}$", local))
    if os.path.exists(dest) or (not has_ext and any(os.path.exists(dest + e) for e in (".jpg", ".png", ".gif", ".webp"))):
        continue
    if SKIP_DL:
        continue
    if DRY:
        print("would fetch", url, "->", local)
        continue
    try:
        if url in fetched:
            with open(os.path.join(root, fetched[url]), "rb") as fh:
                data = fh.read()
        else:
            data = fetch(url)
            time.sleep(0.15)
        if not has_ext:
            ext = sniff_ext(data)
            if ext:
                renames[local] = local + ext
                local, dest = local + ext, dest + ext
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "wb") as out:
            out.write(data)
        fetched.setdefault(url, local)
        print("fetched", local)
    except Exception as e:
        failed.append((url, str(e)))
        print("FAILED", url, e)


# ---- normalise images (idempotent) ----------------------------------------
def normalise(path):
    ext = os.path.splitext(path)[1].lower()
    if ext not in (".jpg", ".jpeg", ".png", ".gif", ".webp"):
        return
    try:
        im = Image.open(path)
    except Exception as e:
        print("unreadable", path, e)
        return
    if ext == ".gif" and getattr(im, "n_frames", 1) > 1:
        return  # leave animated gifs alone
    edge = HEADSHOT_EDGE if "/src/assets/people/" in path.replace(os.sep, "/") else MAX_EDGE
    has_meta = bool(im.getexif()) or "icc_profile" in im.info or "xmp" in im.info
    if max(im.size) <= edge and not has_meta:
        return  # nothing to do; don't recompress on every run
    im = ImageOps.exif_transpose(im)
    if max(im.size) > edge:
        im.thumbnail((edge, edge), Image.LANCZOS)
    if ext in (".jpg", ".jpeg"):
        if im.mode not in ("RGB", "L"):
            im = im.convert("RGB")
        im.save(path, "JPEG", quality=85, optimize=True, progressive=True)
    elif ext == ".png":
        im.save(path, "PNG", optimize=True)
    elif ext == ".webp":
        im.save(path, "WEBP", quality=85)
    elif ext == ".gif":
        im.save(path, "GIF")
    print("normalised", os.path.relpath(path, root))


def ref_forms(local):
    """How a local path is referenced from src/content/*.md."""
    if local.startswith("public/"):
        return [local[len("public"):]]                       # /app/uploads/...
    if local.startswith("src/assets/"):
        return ["../../assets/" + local[len("src/assets/"):]]  # relative from src/content/<coll>/
    return []


if not DRY:
    for sub in ("src/assets", "public/app/uploads"):
        for dp, _, fs in os.walk(os.path.join(root, sub)):
            for fn in fs:
                normalise(os.path.join(dp, fn))

    if renames:
        for dp, _, fs in os.walk(os.path.join(root, "src/content")):
            for fn in fs:
                p = os.path.join(dp, fn)
                with open(p, encoding="utf-8") as fh:
                    s = fh.read()
                s2 = s
                for old, new in renames.items():
                    for o, n in zip(ref_forms(old), ref_forms(new)):
                        s2 = s2.replace(o, n)
                if s2 != s:
                    with open(p, "w", encoding="utf-8") as fh:
                        fh.write(s2)
        with open(os.path.join(here, "renames.csv"), "a", encoding="utf-8") as f:
            for old, new in renames.items():
                f.write(f"{old},{new}\n")

print(f"done. failures: {len(failed)}")
for u, e in failed:
    print("  ", u, e)
'''

CONTENT_CONFIG = '''import { defineCollection, type SchemaContext } from "astro:content";
import { z } from "astro/zod";
import { glob, file } from "astro/loaders";

// Shared fields produced by the WordPress migration.
const wpBase = {
  slug: z.string(),
  date: z.string(), // "YYYY-MM-DD HH:MM:SS" as WordPress stored it
  status: z.literal("publish"),
  author: z.string().optional(),
  wp_id: z.number(),
  original_url: z.string().optional(),
  old_slugs: z.array(z.string()).optional(),
  excerpt: z.string().optional(),
};

const post = ({ image }: SchemaContext) =>
  z.object({
    title: z.string(),
    ...wpBase,
    categories: z.array(z.string()).default([]),
    featured_image: image().optional(),
    featured_image_alt: z.string().optional(),
    featured_image_missing_id: z.number().optional(),
    summary_html: z.string().optional(), // first paragraph as HTML; used by listings and the home page
  });

const news = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/news" }),
  schema: post,
});

const blog = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/blog" }),
  schema: post,
});

const pages = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/pages" }),
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      ...wpBase,
      wp_template: z.string().optional(),
      featured_image: image().optional(),
      featured_image_alt: z.string().optional(),
    }),
});

const people = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/people" }),
  schema: ({ image }) =>
    z.object({
      name: z.string(),
      ...wpBase,
      role: z.string().optional(),
      associations: z.array(z.string()).default([]),
      sort_slug: z.string().optional(),
      menu_order: z.number().default(0),
      photo: image().optional(),
      featured_image_missing_id: z.number().optional(),
      hide_photo_on_page: z.boolean().default(false),
      classic_bio: z.boolean().default(false), // no <p> in the stored bio: live theme showed it without paragraph breaks
      bio_html: z.string().optional(),          // stored bio HTML as the theme printed it (used by the People page)
    }),
});

const jobs = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/jobs" }),
  schema: z.object({
    title: z.string(),
    ...wpBase,
    always_show_expanded: z.boolean().default(false),
    menu_order: z.number().default(0),
  }),
});

const research = defineCollection({
  loader: file("./src/data/research.yaml"),
  schema: z.object({
    title: z.string(),
    year: z.number().optional(),
    author: z.string().optional(),
    venue: z.string().optional(),
    link: z.string().optional(),
    categories: z.array(z.string()).default([]),      // term slugs
    category_names: z.array(z.string()).default([]),
    order: z.record(z.string(), z.number()).optional(), // {category-slug: position on the live site} (tools/apply_live_order.py)
    notes_html: z.string().optional(),
    needs_review: z.string().optional(),
    imported_row: z.number().optional(),
    date: z.string().optional(),
    wp_id: z.number(),
  }),
});

const bibliography = defineCollection({
  loader: file("./src/data/bibliography.yaml"),
  schema: z.object({
    title: z.string(),
    author: z.string().optional(),
    url: z.string().optional(),
    media: z.string().optional(),
    priority: z.number().optional(),
    categories: z.array(z.string()).default([]),      // term slugs
    category_names: z.array(z.string()).default([]),
    order: z.record(z.string(), z.number()).optional(), // {category-slug: position on the live site} (tools/apply_live_order.py)
    notes_html: z.string().optional(),
    imported_row: z.number().optional(),
    date: z.string().optional(),
    wp_id: z.number(),
  }),
});

export const collections = { news, blog, pages, people, jobs, research, bibliography };
'''

ASTRO_CONFIG = '''// @ts-check
import { defineConfig } from "astro/config";

export default defineConfig({
  site: "https://humancompatible.ai",
  // WordPress URLs all ended in "/"; keep that so nothing external breaks.
  trailingSlash: "always",
  build: { format: "directory" },
});
'''

GITIGNORE = '''node_modules/
dist/
.astro/
archive/
media/renames.csv
.DS_Store
'''

WORKFLOW = '''# Builds the site and pushes ONLY the generated dist/ to a separate public repo that
# GitHub Pages serves from. Keeps this (source) repo private on a free plan.
#
# One-time setup:
#   1. Create the public repo (e.g. <org>/chai-website-build), enable Pages from branch gh-pages.
#   2. ssh-keygen -t ed25519 -f deploy_key -N ""
#      - add deploy_key.pub to the PUBLIC repo: Settings > Deploy keys (allow write)
#      - add deploy_key (private) to THIS repo: Settings > Secrets > Actions, name DEPLOY_KEY
#   3. Set EXTERNAL_REPO below.
#
# If you have GitHub Team / Enterprise and can serve Pages from this repo directly, replace the
# last step with actions/upload-pages-artifact + actions/deploy-pages instead.
name: Build and deploy
on:
  push:
    branches: [main]
  workflow_dispatch:
env:
  EXTERNAL_REPO: CHANGE-ME-org/chai-website-build
jobs:
  build-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: npm
      - name: Cache optimized images
        uses: actions/cache@v4
        with:
          path: node_modules/.astro
          key: astro-images-${{ hashFiles('src/assets/**') }}
          restore-keys: astro-images-
      - run: npm ci
      - run: npm run build
      - uses: peaceiris/actions-gh-pages@v4
        with:
          deploy_key: ${{ secrets.DEPLOY_KEY }}
          external_repository: ${{ env.EXTERNAL_REPO }}
          publish_branch: gh-pages
          publish_dir: ./dist
          cname: humancompatible.ai
'''

README = '''# humancompatible.ai — site source

Content migrated from WordPress with `wxr_to_astro.py`. This directory is an Astro project skeleton:
add the Astro toolchain on top (`npm create astro@latest -- --template minimal` into a temp dir and copy
`package.json` in, or just `npm init -y && npm i astro`), then `npm run dev`.

## Layout

    src/content/{pages,news,blog,people,jobs}/   Markdown with front matter (schemas in src/content.config.ts)
    src/data/research.yaml, bibliography.yaml    metadata-only collections (Astro file() loader)
    src/data/menu.yaml, taxonomies.yaml          nav + term lists; taxonomies.yaml has the people grouping order
    src/data/redirects.csv                       old path -> new path (generate meta-refresh stubs from this)
    src/assets/people/<slug>.jpg                 headshots  } referenced from front matter with relative paths,
    src/assets/featured/YYYY/MM/                 featured   } go through Astro's <Image> pipeline
    public/app/uploads/                          inline images + PDFs, served verbatim at the same URLs WP used
    public/app/uploads/external/                 rehosted hotlinked images
    public/app/theme/                            copy the old theme's assets/images/ here (logos, spotlight photos)
    media/manifest.csv + download_media.py       run once while WordPress is still live
    archive/                                     drafts, private/pending posts, authors with emails. GITIGNORED.

## First run

    cd media && python3 download_media.py        # downloads, orients, strips EXIF, caps long edge (once, while WP is live)
    cd .. && npm install                          # Astro + sharp, ~1 min
    npm run dev                                   # http://localhost:4321
    npm run build                                 # writes dist/ (463 pages, a few seconds)

`npm run check` validates every front-matter field against `src/content.config.ts`.

Re-running `wxr_to_astro.py` regenerates src/content, src/data, media/manifest.csv and the config files;
it never touches src/pages, src/layouts, src/styles or downloaded media, so it is safe to repeat.

## Preview templates

`src/pages/` holds deliberately plain templates so every content type renders: home, /news, /blog,
/people (grouped in nav order), /research and /bibliography (grouped by category), /jobs, and one
route per static page. They exist to check the migration, not as the design. Raw HTML blocks carried
over from WordPress are outlined with a dashed orange border.

## Things left for a human

- `unconverted_blocks.txt`: 18 raw HTML / custom blocks kept verbatim in the Markdown (About page logos,
  the 2023/2024 workshop pages). Clean up by hand.
- `src/data/research.yaml` has a few empty titles (`needs_review`) and duplicate category names.
- The mailing-list signup form lived in the theme; grab the Mailchimp embed from the live site.
- Listing pages (/people, /research, /bibliography, /jobs, home, news, blog) need templates — they were
  Blade templates in the theme and are not in the export.
- Two typo'd mailto links: Contact page (`chai-info@` vs `chai-admin@`), Donate page (`berkely.edu`).
- The `archive/` folder is not committed. Keep a copy somewhere safe and decide with CHAI whether any of
  the three substantive drafts should be published.
'''

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
