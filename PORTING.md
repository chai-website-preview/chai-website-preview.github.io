# Porting the live design (HTML5 UP "Verti" via Sage)

Goal for phase 1: the Astro site is visually identical to humancompatible.ai as it is today.
Strategy: transplant. The theme's compiled CSS/JS are used verbatim from `public/app/themes/chai/dist/`;
templates reproduce the live DOM (same ids/classes) so those files apply unchanged.

## Status — every template ported, DOM-diffed against saved copies of the live pages

| Template            | Result of structural diff vs live                                              |
|---------------------|--------------------------------------------------------------------------------|
| Site chrome         | identical (nav, dropdowns, mobile panel and modals come from the theme's own main.js) |
| Home                | identical                                                                       |
| People (+ /people/<slug>/) | identical (174 cards, 10 sections, modals); Dillon Sandhu's slug cleaned up from `5396` |
| News / Blog index   | identical, incl. pagination (10 per page) and "Continue Reading" cards          |
| Single post         | identical                                                                       |
| Research            | identical: 840 entries, category tree, per-category order captured from live   |
| Bibliography        | identical: 226 entries, priority buttons + script, media groups, TOC blurbs    |
| Jobs                | identical, incl. expand/collapse buttons                                        |
| Static pages        | identical (About incl. partner-logo block)                                      |

Only differences left are ones the browser or the theme's JS introduce at runtime (heading ids, normalised
trailing slashes on external links) — not in the generated markup.

## Live-site quirks reproduced on purpose (fix after cutover if wanted)

- People: the "In Memoriam" association (1 person) is never rendered. Bios that were written without
  `<p>` tags show no paragraph breaks (the theme printed stored HTML raw). Graduate Students has a stray
  empty `<p>` under its heading.
- Research: entries with no link render `<a href="">`; author/venue fields keep trailing spaces
  (visible as "Sadigh ." on the live site); a couple of links are malformed (`hhttps://`, `not found`).
- Contact page links `mailto:chai-info@` while showing `chai-admin@`; Donate page has `berkely.edu`.
- Nav links `/people/#research-fellows` and `/people#…` inconsistently — kept as-is.

## Things that lived in the Blade templates (now in src/snippets or hard-coded)

- Research intro paragraphs, Jobs intro paragraphs, Bibliography intro/"Contents" copy, Bibliography
  page CSS and priority-threshold script, the home page YouTube id, the Mailchimp form.

## Ordering rules (derived from the live pages)

- People cards: alphabetical by WordPress slug (`sort_slug`) within each fixed section.
- Research categories: alphabetical by name; entries by live position (`order`), then year desc.
- Bibliography categories: live order (`order` on the term); entries by live position; media groups
  in the term's `media` list order.
- Jobs: newest first. Home "Highlights": four newest news posts, oldest first.

Live positions come from `tools/apply_live_order.py`, run against saved copies of /research and
/bibliography. Re-run it after every `wxr_to_astro.py` regeneration (see README).

## Missing files (Save Page As does not fetch CSS-referenced assets)

Into `public/app/theme/images/logos/` and `public/app/theme/images/people/`: the theme's `assets/images/`
folder from the server (partner logos on About, photos on Spotlights).

## RSS

Generated at /category/news/feed.xml, /category/blog/feed.xml and /feed.xml (GitHub Pages cannot serve
XML at the bare /feed/ paths WordPress used). The RSS icon on /news points at the new URL.

## Visual diff loop (next step)

With the assets in place: `npm run build && npx astro preview`, then compare against the live site at
1440 / 1024 / 736 / 480 px (the theme's breakpoints). Since the DOM and CSS are identical, remaining
differences should be image-only.
