Not part of the Astro site. These are the asset paths the OLD WordPress site asks for.

chai.berkeley.edu still serves the WordPress instance, and every one of its pages hardcodes
https://humancompatible.ai/... for its stylesheets, scripts and theme images. Since this repo
started serving that domain, those requests 404 and the WordPress site renders as unstyled text.
The files here and under ../app/themes/chai/dist/ are parked at the filenames WordPress asks for:

  wp/wp-includes/css/dist/block-library/style.min.css   WordPress core block library CSS
  wp/wp-includes/js/jquery/jquery.min.js                jQuery 3.7.1
  wp/wp-includes/js/jquery/jquery-migrate.min.js        jQuery Migrate 3.4.1
  wp/wp-includes/js/comment-reply.min.js                WordPress core 6.7.2; single posts only
  app/themes/chai/dist/styles/main_dea8ca41.css         the old theme's stylesheet
  app/themes/chai/dist/scripts/main_dea8ca41.js         the old theme's script

They began as copies of assets the Astro site itself vendored, back when it reproduced the old
design. It no longer does — the Kadence design replaced it and deleted the originals — so these are
now the only copies, kept for chai.berkeley.edu alone. Nothing the live site serves loads them.

So are the four theme images and the icon font that survive next door in
app/themes/chai/dist/images/ and vendor/. main_dea8ca41.css references three of them by
root-absolute url() — the hero banner, the nav texture (37 rules) and fa-solid-900_1551f4f6.woff2 —
and the WordPress markup requests chai-logo_a729cbef.png on every page and RSS_3d934d36.png on two.
Delete those and chai.berkeley.edu gets its typography back but loses its images and every icon.

The ?ver= query strings WordPress appends are ignored by static hosting, so one file per path is
enough. dea8ca41 is the theme's asset hash on the WordPress side: if that instance is ever rebuilt
the hash changes and these copies stop being found.

Delete public/wp/ and the whole of public/app/themes/chai/ once chai.berkeley.edu no longer serves
WordPress. That is the only reason any of it is still here.
