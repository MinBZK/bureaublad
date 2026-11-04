# Custom Theming Guide

This application follows the Rijkshuisstijl (Rijksoverheid) visual language and supports custom theming through CSS variables. Clients can easily customize colors by providing a custom CSS file through the configuration API or by using the palette picker in the header.

## Adjustable colours

Every colour is driven by CSS custom properties. The default palette is
**Lintblauw** (`#154273`), the Rijksoverheid main colour. The in-app palette
picker writes the selected 100% colour to `--rh-*` variables and persists the
choice in `localStorage`.

The complete official Rijkshuisstijl palette is available (see
`src/app/Common/brandPalettes.js`):

| Colour      | HEX       |
| ----------- | --------- |
| Lintblauw   | `#154273` |
| Paars       | `#42145f` |
| Violet      | `#a90061` |
| Robijnrood  | `#ca005d` |
| Roze        | `#f092cd` |
| Rood        | `#d52b1e` |
| Oranje      | `#e17000` |
| Donkergeel  | `#ffb612` |
| Geel        | `#f9e11e` |
| Donkerbruin | `#673327` |
| Bruin       | `#94710a` |
| Donkergroen | `#275937` |
| Groen       | `#39870c` |
| Mosgroen    | `#777b00` |
| Mintgroen   | `#76d2b6` |
| Donkerblauw | `#01689b` |
| Hemelblauw  | `#007bc7` |
| Lichtblauw  | `#8fcae7` |

### Colour rules

The implementation follows the Rijkshuisstijl colour rules:

- Only the **100%** values of the communication colours are selectable.
- Tints (75%, 60%, 45%, 30%, 15%) are generated with
  `--color-primary-tint-*` for supporting surfaces, charts and tables, and are
  only used together with the 100% colour of the same hue.
- **Cool Gray** (`#0f172a`) is not a communication colour and is not offered in
  the picker. It is reserved for neutral surfaces, borders, tables and charts.
- Any organisation may use every colour; no colour is claimed.
- Text on a primary colour is chosen automatically (white or Cool Gray) for the
  best contrast.

## How It Works

The application dynamically loads custom theme CSS from a URL provided by the configuration API:

1. The backend configuration API returns a `theme_css` URL in the config response
2. [ThemeContext.jsx](src/app/Components/Context/ThemeContext.jsx) automatically loads the CSS file from that URL
3. The custom CSS file overrides the default CSS variables to apply your brand's theme

## How to Customize

### Step 1: Create Your Custom CSS File

Create a CSS file with your custom theme. You can use this template:

```css
/**
 * CUSTOM THEME
 *
 * Override CSS variables to customize the application theme
 */

:root {
  /* Use the official 100% Rijkshuisstijl colours.
     Override the semantic variables so the theme can also override the
     in-app colour picker. */
  --color-primary: #39870c;
  --color-primary-hover: color-mix(in srgb, var(--color-primary) 86%, black);
  --color-primary-active: color-mix(in srgb, var(--color-primary) 74%, black);
  --color-on-primary: #ffffff;
  --color-accent: #154273;

  /* Neutral surfaces are derived from Cool Gray, not a communication colour */
  --color-background-neutral: #f1f5f9;
  --color-border-default: #cbd5e1;
}
```

### Step 2: Host Your CSS File

Host your custom CSS file on a publicly accessible URL, for example:

- `https://yourdomain.com/assets/custom-theme.css`
- `https://cdn.yourdomain.com/theme.css`

### Step 3: Configure the API

Update your backend configuration API to return the `theme_css` URL:

```json
{
  "theme_css": "https://yourdomain.com/assets/custom-theme.css",
  "applications": [...],
  ...
}
```

### Step 4: Reload the Application

The theme will be automatically loaded when users access the application. No code changes required!

## Local Development

For local development and testing:

1. Edit [src/app/custom-style.css](src/app/custom-style.css) with your custom variables
2. This file is imported in [layout.jsx](src/app/layout.jsx) and will be used as a fallback or for testing
3. The file includes 4 pre-made example themes at the bottom that you can copy and paste
4. Once finalized, host the CSS file and configure the API as described above

## Pre-made Theme Examples

The [custom-style.css](src/app/custom-style.css) file includes ready-to-use theme examples at the bottom:

- **Hemelblauw** - Blue accent palette
- **Groen** - Green accent palette
- **Rood** - Red accent palette
- **Paars** - Purple accent palette

Simply copy one of these example themes and paste it at the top of the file (uncommented) to try it out.

## Available CSS Variables

### Base/Generic Colors (Foundation)

These generic colors are reused across multiple components to ensure consistency:

- `--color-primary` - Primary colour, always a 100% Rijkshuisstijl value (default: #154273)
- `--color-primary-hover` - Functional hover state (default: #123963)
- `--color-primary-active` - Functional active state (default: #103155)
- `--color-on-primary` - Readable text colour on the primary colour (default: #ffffff)
- `--color-primary-tint-75/60/45/30/15` - Official support tints, always paired with the 100% colour
- `--color-accent` - Accent/link colour, also a 100% Rijkshuisstijl value (default: #007bc7)
- `--color-text-light` - Light text color for dark backgrounds (default: #ffffff)
- `--color-text-dark` - Dark text color for light backgrounds (default: #0f172a)
- `--color-text-muted` - Muted/secondary text (default: #475569)
- `--color-background-light` - Light background (default: #ffffff)
- `--color-background-neutral` - Neutral background (default: #f1f5f9)
- `--color-border-default` - Default border color (default: #cbd5e1)
- `--color-border-subtle` - Subtle border/placeholder color (default: #94a3b8)

**Note:** You can override the base colors to automatically update all components that use them, or override individual component colors for fine-grained control.

### Header Colors

- `--header-background` - Background color of the header and dark menu
- `--header-text-color` - Text color in the header (uses `--color-text-light` by default)

### Button Colors

- `--button-primary-bg` - Primary button background (uses `--color-primary`)
- `--button-primary-hover` - Primary button on hover (uses `--color-primary-hover`)
- `--button-primary-active` - Primary button when clicked (uses `--color-primary-active`)
- `--button-primary-text` - Primary button text color (uses `--color-text-light`)

### Layout Colors

- `--layout-background` - Overall layout background (uses `--color-background-neutral`)
- `--layout-content-background` - Content area background (uses `--color-background-neutral`)

### Menu Colors

- `--menu-item-selected-bg` - Selected menu item background (uses `--color-primary`)
- `--menu-item-hover-bg` - Menu item on hover (uses `--color-primary`)
- `--menu-item-active-bg` - Menu item when active (uses `--color-primary-active`)
- `--menu-item-selected-text` - Selected menu item text color (uses `--color-text-light`)

### Card Colors

- `--card-background` - Background color for cards (uses `--color-background-light`)
- `--card-text-color` - Text color inside cards (uses `--color-text-dark`)
- `--card-border-color` - Border color for cards (uses `--color-border-default`)

### Input Colors

- `--input-background` - Background color for input fields (uses `--color-background-light`)
- `--input-text-color` - Text color in input fields (uses `--color-text-dark`)
- `--input-border-color` - Border color for input fields (uses `--color-border-default`)
- `--input-placeholder-color` - Placeholder text color (uses `--color-border-subtle`)

### Icon Colors

- `--icon-color` - Color for icons (uses `--color-text-dark`)

## Customization Approaches

There are two ways to customize the theme:

### Approach 1: Override Base Colors (Recommended for Simple Themes)

Change the base/generic colors to automatically update all components:

```css
:root {
  /* Override base colours - affects all components using them */
  --color-primary: #39870c;
  --color-primary-hover: color-mix(in srgb, var(--color-primary) 86%, black);
  --color-primary-active: color-mix(in srgb, var(--color-primary) 74%, black);
  --color-on-primary: #ffffff;
  --color-accent: #154273;
}
```

This approach is ideal when you want a consistent color scheme across the entire application.

### Approach 2: Override Individual Component Colors (Fine-grained Control)

Override specific component colors for more control:

```css
:root {
  /* Override specific components, still using 100% brand colours */
  --button-primary-bg: #39870c;
  --menu-item-selected-bg: #39870c;
  --card-background: #f1f5f9;
}
```

This approach gives you maximum flexibility to customize each component independently.

### Approach 3: Hybrid (Best of Both)

Combine both approaches - set base colors and override specific components:

```css
:root {
  /* Set base colours */
  --color-primary: #39870c;
  --color-on-primary: #ffffff;

  /* Override specific components that need another official colour */
  --header-background: #154273;
}
```

## Color Format

You can use any valid CSS color format:

- Hex: `#39870c`
- RGB: `rgb(57, 135, 12)`
- RGBA: `rgba(57, 135, 12, 0.9)`
- HSL: `hsl(98, 84%, 29%)`

**Note:** For communication colours, use the official 100% hex values listed
above. Do not use arbitrary colours or tint percentages as a primary/accent
colour.
