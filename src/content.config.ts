import { defineCollection, type SchemaContext } from "astro:content";
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
