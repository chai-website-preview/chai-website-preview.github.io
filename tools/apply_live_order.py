#!/usr/bin/env python3
"""Record the *display order* of research and bibliography entries from saved copies of the
live pages, so the static site lists them in exactly the same sequence.

WordPress ordered these lists by a meta value with an unstable tie-break, so the order cannot be
reproduced from the export alone. This annotates:
  src/data/research.yaml        -> `order` on each entry (position within its category)
  src/data/bibliography.yaml    -> `order` on each entry
  src/data/taxonomies.json/yaml -> `order` on each bibliography-category term (supercats and cats)

Usage (from the project root):
  python3 tools/apply_live_order.py --research "Research Publications.html" --bibliography "Recommended Materials.html"

Re-run after every `wxr_to_astro.py` regeneration. Entries that are not on the saved page keep no
`order` and sort after the ordered ones (year desc / priority asc, then wp_id).
"""
import argparse, html, json, re, unicodedata
import yaml

def norm(t):
    t = html.unescape(t or "")
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    t = re.sub(r"[\u2018\u2019'\u201c\u201d\"]", "", t)
    return re.sub(r"[^a-z0-9]+", " ", t.lower()).strip().rstrip(".")

def main_of(path):
    s = open(path, encoding="utf-8", errors="replace").read()
    b = s[s.find("<main"):s.find("</main>")]
    return re.sub(r"<script.*?</script>", "", b, flags=re.S)

def assign_orders(data, by_cat):
    """Give every entry an {category: position} map. Duplicate titles consume successive positions
    (in wp_id order), so two posts with the same title keep their distinct live positions."""
    used = {cat: [False] * len(titles) for cat, titles in by_cat.items()}
    matched = 0
    for r in sorted(data, key=lambda r: r["wp_id"]):
        r.pop("order", None)
        for cat in r["categories"]:
            titles = by_cat.get(cat)
            if not titles:
                continue
            key = norm(r["title"])
            for i, t in enumerate(titles):
                if t == key and not used[cat][i]:
                    used[cat][i] = True
                    r.setdefault("order", {})[cat] = i
                    break
        if "order" in r:
            matched += 1
    return matched


def apply_research(path, data):
    b = main_of(path)
    by_cat = {}
    for m in re.finditer(r'<h4 id="([^"]+)"[^>]*>.*?</h4>\s*<ul class="publications">(.*?)</ul>', b, re.S):
        slug, block = m.group(1), m.group(2)
        titles = [norm(t) for t in re.findall(r'<a href="[^"]*">(.*?)</a>', block, re.S)]
        # entries without a link render the title as plain text after the year
        for li in re.findall(r"<li>(.*?)</li>", block, re.S):
            if "<a " not in li:
                t = re.sub(r"<i>.*?</i>", "", li, flags=re.S)
                t = re.sub(r"^.*?\d{4}\.\s*", "", re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", t)).strip(), flags=re.S)
                titles.append(norm(t))
        by_cat[slug] = titles
    matched = assign_orders(data, by_cat)
    print(f"research: {matched}/{len(data)} entries matched to the live page ({len(by_cat)} categories)")

def apply_bibliography(path, data, taxonomies):
    b = main_of(path)
    # category order: sequence of h3.bib-supercategory / h4.bib-category ids
    seq = re.findall(r'<h(?:3|4) class="bib-(?:supercategory|category)" id="([^"]+)"', b)
    seq = [x for x in seq if x != "contents"]
    order = {slug: i for i, slug in enumerate(seq)}
    for term in taxonomies.get("bibliography-category", []):
        if term["slug"] in order:
            term["order"] = order[term["slug"]]
    # entry sequence per category as (media, priority, title) so same-titled entries in different
    # media groups / priorities are told apart
    by_cat = {}
    media = None
    for m in re.finditer(r'<h5 class="bib-media[^"]*">([^<]+)</h5>|<div class="bib-entry ([a-z0-9-]+) (\d)[^"]*">\s*<span class="bib-entry-title">.*?<a href="[^"]*">(.*?)</a>', b, re.S):
        if m.group(1):
            media = m.group(1).rstrip(":").strip()
        else:
            by_cat.setdefault(m.group(2), []).append((media, int(m.group(3)), norm(m.group(4))))
    used = {cat: [False] * len(v) for cat, v in by_cat.items()}
    matched = 0
    for r in sorted(data, key=lambda r: r["wp_id"]):
        r.pop("order", None)
        key = (r.get("media"), r.get("priority"), norm(r["title"]))
        for cat in r["categories"]:
            seqc = by_cat.get(cat)
            if not seqc:
                continue
            for i, k in enumerate(seqc):
                if k == key and not used[cat][i]:
                    used[cat][i] = True
                    r.setdefault("order", {})[cat] = i
                    break
        if "order" in r:
            matched += 1
    print(f"bibliography: {matched}/{len(data)} entries matched; {len(order)} categories ordered")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--research"); ap.add_argument("--bibliography")
    a = ap.parse_args()
    tax = json.load(open("src/data/taxonomies.json"))
    if a.research:
        d = yaml.safe_load(open("src/data/research.yaml"))
        apply_research(a.research, d)
        yaml.dump(d, open("src/data/research.yaml", "w"), sort_keys=False, allow_unicode=True, width=1000)
    if a.bibliography:
        d = yaml.safe_load(open("src/data/bibliography.yaml"))
        apply_bibliography(a.bibliography, d, tax)
        yaml.dump(d, open("src/data/bibliography.yaml", "w"), sort_keys=False, allow_unicode=True, width=1000)
        json.dump(tax, open("src/data/taxonomies.json", "w"), indent=2)
        ty = yaml.safe_load(open("src/data/taxonomies.yaml")); ty["bibliography-category"] = tax["bibliography-category"]
        yaml.dump(ty, open("src/data/taxonomies.yaml", "w"), sort_keys=False, allow_unicode=True, width=1000)
