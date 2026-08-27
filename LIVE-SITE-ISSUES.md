# Known issues that also exist on the live WordPress site

These were found while porting to Astro. **Each one was verified against
https://humancompatible.ai as it stands today and reproduces there too**, so the Astro port is
faithful — fixing them is a content decision for CHAI, not a migration task. Deliberately left
alone so the port stays a point-for-point replica.

Verified 2026-08-27.

## Page metadata the live site does not have

The live site emits no `meta description`, no Open Graph tags, no Twitter Card tags, no analytics
of any kind, and no RSS autodiscovery `<link>`. The port matches. **Adding these would be an
improvement, not a fidelity fix** — worth doing deliberately after cutover rather than silently.

## Image alt text

Featured images render `alt=""` across the site. This is not a migration failure: the WordPress
export contains exactly one `_wp_attachment_image_alt` value in the entire database ("Ian Baker").
The alt text was never authored.

This is the most consequential item here. On the `/news` and `/blog` listing cards the image is the
only child of its link, so those cards have **no accessible name at all** (WCAG 2.4.4 / 4.1.2).
Cheapest remedy: fall back to the post title instead of `""` in `PostBox.astro` / `PostList.astro`.
Proper remedy: author alt text for ~236 images.

## Broken links (byte-identical on live)

| Where | Problem |
|---|---|
| `/jobs/` intern testimonials | 3 LinkedIn hrefs end in a U+FFFD replacement character (Beth Barnes, Stephen Casper, Dmitrii Krasheninnikov) |
| `/privacypolicy/` ×3 | `href="https://humancompatible.ai/chai-admin@lists.berkeley.edu"` — missing the `mailto:` scheme, so it resolves as a page URL |
| `/about/` | `href="http://http://umich.edu/"` — doubled scheme |
| `/contact/` | links `mailto:chai-info@…` while displaying `chai-admin@…` |
| `/donate/` | `berkely.edu` typo |
| `/chai2024/` | Whova logo `<img>` — the upstream endpoint now returns HTTP 400, so it is broken on live too and unrecoverable |

## Research bibliography data (`src/data/research.yaml`, 840 entries)

Mostly scrape residue from however the list was originally assembled:

- 1 entry with an empty title (`wp_id 783`, flagged `needs_review`)
- 2 malformed links: `hhttps://arxiv.org/abs/2204.01437` (`wp_id 3409`) and the literal string
  `"not found "` (`wp_id 4255`)
- 2 entries with two URLs concatenated (`wp_id 3430`, `2465`)
- 3 entries with no link, rendering `<a href="">` — a focusable self-link
- ~21 true duplicate entries (same title *and* category), e.g. `wp_id 4191/4248/4290`
- ~74 links pointing at a Google Scholar citation page rather than the paper
- Whitespace/newline residue in ~58 `venue` and `author` fields — ~20 venues prefixed `"Journal\n"`,
  7 authors prefixed with a lab code, 1 mangled author (`wp_id 4195`,
  `"Nathaniel Lubinarchive pageThomas Krendl Gilbertarchive page"`). Visible on live as e.g. "Sadigh ."
- A duplicate category name, *"1.2. Overviews of societal-scale risks from AI"*, mapped to two slugs
  (37 entries vs 1) so the heading renders twice
- A junk `"0. NOTE:"` category, and its identically-named child, holding 4 entries

## Template quirks (already noted in PORTING.md:24-38)

- The **"In Memoriam"** association is never rendered on `/people/`. One person (Joseph Halpern) holds
  only that association, so he has no route into the page. `/people/joseph-halpern/` still builds and
  its script tries to open a modal that was never rendered, leaving a blank page. **Worth raising with
  CHAI** rather than leaving broken.
- Bios stored without `<p>` tags show no paragraph breaks (the theme printed stored HTML raw).
- A stray empty `<p>` sits under the Graduate Students heading.
- The nav mixes `/people#faculty` and `/people/#research-fellows` inconsistently.
- `sarah-otis` has no bio at all.

## Other

- The mailing-list form posts to `smithamilli.us10.list-manage.com` — a **personal** Mailchimp
  account, not a CHAI-owned one. Matches live, but worth confirming CHAI intends this.
- The email input has no `<label>`, only a placeholder (WCAG 3.3.2).

## Deliberate deviations from live (not bugs)

- **Feeds.** WordPress served `/feed/`, `/category/news/feed/`, `/category/blog/feed/`. GitHub Pages
  cannot serve XML from an extensionless path, so the feeds live at `/feed.xml`,
  `/category/news/feed.xml`, `/category/blog/feed.xml`, with meta-refresh stubs at the old paths.
- **`robots.txt`.** Live's is WordPress-specific (`Disallow: /wp/wp-admin/`). The static build ships a
  minimal one pointing at the sitemap.
