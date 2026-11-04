# i18n Migration Guide

This guide shows you how to update components to use translations instead of hardcoded text.

## Translation Files Location

- English: `frontend/messages/en.json`
- Dutch: `frontend/messages/nl.json`

## How to Use Translations in Components

### Step 1: Import the hook

```jsx
import { useTranslations } from "../../../../i18n/TranslationsProvider";
```

### Step 2: Use the hook in your component

```jsx
function MyComponent() {
  const t = useTranslations("NamespaceName");

  return <div>{t("keyName")}</div>;
}
```

### Step 3: Multiple namespaces

If you need translations from multiple namespaces:

```jsx
function MyComponent() {
  const tHome = useTranslations("HomePage");
  const tTheme = useTranslations("Theme");

  return (
    <div>
      <h1>{tHome("title")}</h1>
      <button>{tTheme("colors")}</button>
    </div>
  );
}
```

## Adding New Translations

When you add new user-facing text:

1. Add the key and translations to both `en.json` and `nl.json`
2. Use the appropriate namespace
3. Use the `useTranslations` hook in your component

## 📁 File Structure

```
frontend/
├── messages/
│   ├── en.json          # English translations
│   └── nl.json          # Dutch translations
├── src/
│   ├── i18n/
│   │   ├── config.js              # Translation configuration
│   │   ├── LanguageContext.jsx    # Language state management
│   │   └── TranslationsProvider.jsx  # Translation provider
│   └── app/
│       ├── layout.jsx   # Wraps app with providers
│       └── Components/
│           └── Layout/
│               └── Components/
│                   └── HeaderLayout.jsx  # Contains language toggle
```
