# humancompatible.ai — site source

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

## Templates

`src/pages/` and `src/components/` reproduce the live site's theme (HTML5 UP "Verti" via Sage) DOM-for-DOM;
the theme's own CSS/JS in `public/app/themes/chai/dist/` are used unchanged. See PORTING.md.

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
