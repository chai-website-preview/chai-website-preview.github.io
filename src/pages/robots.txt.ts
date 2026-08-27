import { IS_STAGING } from "../lib/env";

// Production mirrors the live site's intent (allow everything, advertise the sitemap).
// Staging blocks all crawlers — see src/lib/env.ts.
export async function GET({ site }: { site: URL }) {
  const body = IS_STAGING
    ? "User-agent: *\nDisallow: /\n"
    : `User-agent: *\nDisallow:\n\nSitemap: ${new URL("sitemap-index.xml", site).href}\n`;
  return new Response(body, { headers: { "Content-Type": "text/plain; charset=utf-8" } });
}
