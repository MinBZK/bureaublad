# Custom Theming Guide

This application supports custom theming through CSS variables. Clients can easily customize colors by providing a custom CSS file through the configuration API.

## How It Works

The application dynamically loads custom theme CSS from a URL provided by the configuration API:

1. The backend configuration API returns a `theme_css` URL in the config response
2. [ThemeLoader.jsx](src/app/Components/ThemeLoader/ThemeLoader.jsx) automatically loads the CSS file from that URL
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
  /* Base/Generic colors - Recommended approach
     Override these to automatically update all components */
  --color-primary: #43a047;
  --color-primary-hover: #66bb6a;
  --color-primary-active: #2e7d32;
  --color-background-neutral: #e8f5e9;
  --color-border-default: #c8e6c9;

  /* Component-specific overrides (Optional)
     Override these for fine-grained control */
  --header-background: #2e7d32;
  --avatar-name-bg: #ef6c00;
  --avatar-call-bg: #66bb6a;
  --avatar-doc-bg: #43a047;
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

- **Blue Corporate Theme** - Professional blue tones
- **Green Nature Theme** - Fresh green palette
- **Purple Modern Theme** - Modern purple design
- **Dark Theme** - Dark mode optimized colors

Simply copy one of these example themes and paste it at the top of the file (uncommented) to try it out.

## Available CSS Variables

### Base/Generic Colors (Foundation)

These generic colors are reused across multiple components to ensure consistency:

- `--color-primary` - Primary brand color (default: #1677ff)
- `--color-primary-hover` - Primary color on hover (default: #4096ff)
- `--color-primary-active` - Primary color when active/clicked (default: #0958d9)
- `--color-text-light` - Light text color for dark backgrounds (default: #ffffff)
- `--color-text-dark` - Dark text color for light backgrounds (default: #000000)
- `--color-background-light` - Light background (default: #ffffff)
- `--color-background-neutral` - Neutral background (default: #f5f5f5)
- `--color-border-default` - Default border color (default: #d9d9d9)
- `--color-border-subtle` - Subtle border/placeholder color (default: #bfbfbf)

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

### Avatar Colors

- `--avatar-name-bg` - Background color for name/profile avatars (default: #f56a00)
- `--avatar-call-bg` - Background color for call/phone avatars (default: #87d068)
- `--avatar-doc-bg` - Background color for document avatars (default: #4096ff)
- `--avatar-ai-bg` - Background color for AI conversation avatars (uses `--color-primary`)

### Card Colors

- `--card-background` - Background color for cards/widgets (uses `--color-background-light`)
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
  /* Override base colors - affects all components using them */
  --color-primary: #2e7d32;
  --color-primary-hover: #43a047;
  --color-primary-active: #1b5e20;
  --color-text-light: #ffffff;
  --color-text-dark: #000000;
}
```

This approach is ideal when you want a consistent color scheme across the entire application.

### Approach 2: Override Individual Component Colors (Fine-grained Control)

Override specific component colors for more control:

```css
:root {
  /* Override specific components */
  --button-primary-bg: #2e7d32;
  --menu-item-selected-bg: #43a047;
  --card-background: #e8f5e9;
}
```

This approach gives you maximum flexibility to customize each component independently.

### Approach 3: Hybrid (Best of Both)

Combine both approaches - set base colors and override specific components:

```css
:root {
  /* Set base colors */
  --color-primary: #2e7d32;
  --color-text-light: #ffffff;

  /* Override specific components that need different colors */
  --avatar-ai-bg: #1565c0; /* Different from primary */
  --header-background: #1b5e20; /* Darker than primary */
}
```

## Color Format

You can use any valid CSS color format:

- Hex: `#2e7d32`
- RGB: `rgb(46, 125, 50)`
- RGBA: `rgba(46, 125, 50, 0.9)`
- HSL: `hsl(122, 39%, 49%)`
- Color names: `green`
  ```

  ```
