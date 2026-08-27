#!/usr/bin/env python3
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
