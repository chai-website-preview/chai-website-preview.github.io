/**
 * Staging builds (the internal preview on GitHub Pages) set CHAI_STAGING=1.
 * They must never be indexed: the preview is a near-duplicate of the live site and would
 * otherwise compete with it in search. Production builds leave the variable unset.
 */
export const IS_STAGING = process.env.CHAI_STAGING === "1";
