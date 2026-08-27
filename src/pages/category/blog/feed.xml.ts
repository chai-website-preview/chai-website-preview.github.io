import rss from "@astrojs/rss";
import { getCollection } from "astro:content";
import { postPath, newest } from "../../../lib/dates";
export async function GET(context: { site: URL }) {
  const posts = (await getCollection("blog")).sort(newest).slice(0, 20);
  return rss({
    title: "Center for Human-Compatible Artificial Intelligence – Blog",
    description: "Center for Human-Compatible AI is building exceptional AI for humanity",
    site: context.site,
    items: posts.map((p) => ({
      title: p.data.title, link: postPath("blog", p), pubDate: new Date(p.data.date.replace(" ", "T")),
      description: p.data.summary_html ?? p.data.excerpt ?? "",
    })),
  });
}
