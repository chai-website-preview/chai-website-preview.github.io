// @ts-check
import { defineConfig } from "astro/config";

export default defineConfig({
  site: "https://humancompatible.ai",
  // WordPress URLs all ended in "/"; keep that so nothing external breaks.
  trailingSlash: "always",
  build: { format: "directory" },
  // Content was converted from WordPress HTML; typography (curly quotes, dashes) is already applied by the
  // extractor, and WordPress never autolinked bare URLs/emails — so keep Markdown rendering literal.
  markdown: { gfm: false, smartypants: false },
});
