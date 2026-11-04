/**
 * Rijkshuisstijl colour system.
 *
 * Only the official 100% colour values from the Rijkshuisstijl digital style
 * guide are selectable. Cool Gray is deliberately excluded from the picker:
 * it is not a communication colour and is reserved for neutral surfaces,
 * tables and charts.
 *
 * Usage rules (https://www.rijkshuisstijl.nl, ItemId=10489):
 * - Always use the 100% version of a communication colour.
 * - Tints (75/60/45/30/15%) may only support the 100% colour of the same hue.
 * - Cool Gray may not be used as a communication colour.
 * - Colours cannot be claimed; every organisation may use all of them.
 */

/** The 100% Rijkshuisstijl colours. Lintblauw is the main colour. */
export const RIJKSHUISSTIJL_COLORS = {
  lintblauw: { label: "Lintblauw", hex: "#154273", main: true },
  paars: { label: "Paars", hex: "#42145f" },
  violet: { label: "Violet", hex: "#a90061" },
  robijnrood: { label: "Robijnrood", hex: "#ca005d" },
  roze: { label: "Roze", hex: "#f092cd" },
  rood: { label: "Rood", hex: "#d52b1e" },
  oranje: { label: "Oranje", hex: "#e17000" },
  donkergeel: { label: "Donkergeel", hex: "#ffb612" },
  geel: { label: "Geel", hex: "#f9e11e" },
  donkerbruin: { label: "Donkerbruin", hex: "#673327" },
  bruin: { label: "Bruin", hex: "#94710a" },
  donkergroen: { label: "Donkergroen", hex: "#275937" },
  groen: { label: "Groen", hex: "#39870c" },
  mosgroen: { label: "Mosgroen", hex: "#777b00" },
  mintgroen: { label: "Mintgroen", hex: "#76d2b6" },
  donkerblauw: { label: "Donkerblauw", hex: "#01689b" },
  hemelblauw: { label: "Hemelblauw", hex: "#007bc7" },
  lichtblauw: { label: "Lichtblauw", hex: "#8fcae7" },
};

/**
 * Cool Gray is a supporting neutral, not a communication colour. It is only
 * used for surfaces, borders, tables and charts.
 */
export const COOL_GREY = { label: "Cool Gray", hex: "#0f172a" };

/** Official support percentages for communication colours. */
export const COLOR_PERCENTAGES = [75, 60, 45, 30, 15];

const LINTBLAUW = RIJKSHUISSTIJL_COLORS.lintblauw.hex;
const HEMELBLAUW = RIJKSHUISSTIJL_COLORS.hemelblauw.hex;

const clamp = (value) => Math.min(255, Math.max(0, value));

const hexToRgb = (hex) => {
  const normalized = hex.replace("#", "");
  return [
    parseInt(normalized.slice(0, 2), 16),
    parseInt(normalized.slice(2, 4), 16),
    parseInt(normalized.slice(4, 6), 16),
  ];
};

const rgbToHex = (rgb) =>
  `#${rgb
    .map((channel) => clamp(Math.round(channel)).toString(16).padStart(2, "0"))
    .join("")}`;

/** Mix a colour towards black. Used for functional hover/active states. */
const shade = (hex, amount) =>
  rgbToHex(hexToRgb(hex).map((channel) => channel * (1 - amount)));

const relativeLuminance = (hex) => {
  const [r, g, b] = hexToRgb(hex).map((channel) => {
    const value = channel / 255;
    return value <= 0.03928 ? value / 12.92 : ((value + 0.055) / 1.055) ** 2.4;
  });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
};

const contrastRatio = (a, b) => {
  const light = Math.max(relativeLuminance(a), relativeLuminance(b));
  const dark = Math.min(relativeLuminance(a), relativeLuminance(b));
  return (light + 0.05) / (dark + 0.05);
};

/**
 * Pick white or Cool Gray for text on top of a 100% colour, whichever gives
 * the best contrast. This keeps the primary colour at its official 100% value.
 */
export const readableTextColor = (hex) =>
  contrastRatio(hex, "#ffffff") >= contrastRatio(hex, COOL_GREY.hex)
    ? "#ffffff"
    : COOL_GREY.hex;

const buildPalette = ({ label, hex, main = false }) => ({
  label,
  hex,
  main,
  // The 100% value is always used for primary surfaces and controls.
  primary: hex,
  // Functional UI states, not communication tints.
  primaryHover: shade(hex, 0.14),
  primaryActive: shade(hex, 0.26),
  onPrimary: readableTextColor(hex),
  // A second official 100% colour for links and accents.
  accent: hex === LINTBLAUW ? HEMELBLAUW : LINTBLAUW,
});

export const BRAND_PALETTES = Object.fromEntries(
  Object.entries(RIJKSHUISSTIJL_COLORS).map(([key, colour]) => [
    key,
    buildPalette(colour),
  ]),
);

export const DEFAULT_BRAND = "lintblauw";

export const getBrandPalette = (key) =>
  BRAND_PALETTES[key] || BRAND_PALETTES[DEFAULT_BRAND];

/**
 * Map a palette to the CSS custom properties consumed by globals.css.
 * Only the 100% value is exposed as a brand colour; supporting tints are
 * generated in CSS so they can adapt to light and dark surfaces.
 */
export const paletteToCssVariables = (palette) => ({
  "--rh-primary": palette.primary,
  "--rh-primary-hover": palette.primaryHover,
  "--rh-primary-active": palette.primaryActive,
  "--rh-on-primary": palette.onPrimary,
  "--rh-brand-accent": palette.accent,
});
