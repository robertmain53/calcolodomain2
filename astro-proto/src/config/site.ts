export const siteUrl = "https://calcdomain.com";

export const locales = ["en"] as const;
export type Locale = (typeof locales)[number];
export const defaultLocale: Locale = "en";

export const siteName = "CalcDomain";
export const siteDescription =
  "Calculator hub with professional-grade tools, semantic navigation, and deep topical clusters.";

export const hubs = [
  "Finance & Business",
  "Engineering & Construction",
  "Math & Science",
  "Health & Sport",
] as const;
