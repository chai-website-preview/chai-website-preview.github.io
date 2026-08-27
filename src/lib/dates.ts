// Helpers for the WordPress-shaped `date: "YYYY-MM-DD HH:MM:SS"` strings.
export const ymd = (d: string) => d.slice(0, 10).split("-");
export const postPath = (section: "news" | "blog", e: { data: { date: string; slug: string } }) => {
  const [y, m, day] = ymd(e.data.date);
  return `/${section}/${y}/${m}/${day}/${e.data.slug}/`;
};
const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
/** "07 Mar 2025" — the theme's date format (d M Y). */
export const fmt = (d: string) => {
  const [y, m, day] = ymd(d);
  return `${day} ${MONTHS[Number(m) - 1]} ${y}`;
};
export const newest = <T extends { data: { date: string } }>(a: T, b: T) => b.data.date.localeCompare(a.data.date);
export const PER_PAGE = 10; // WordPress posts_per_page
