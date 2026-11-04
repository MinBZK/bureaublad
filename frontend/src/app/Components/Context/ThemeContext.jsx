"use client";

import { createContext, useContext, useState, useEffect, useMemo } from "react";
import { ConfigProvider, theme as antdTheme } from "antd";
import { useAppContext } from "./AppContext";
import {
  BRAND_PALETTES,
  DEFAULT_BRAND,
  getBrandPalette,
  paletteToCssVariables,
} from "../../Common/brandPalettes";

const THEME_STORAGE_KEY = "theme";
const BRAND_STORAGE_KEY = "brand-palette";
const DEFAULT_THEME = "light";

const ThemeContext = createContext({
  theme: DEFAULT_THEME,
  setTheme: () => {},
  toggleTheme: () => {},
  brand: DEFAULT_BRAND,
  setBrand: () => {},
  palettes: BRAND_PALETTES,
});

const readStorage = (key, fallback) => {
  if (typeof window === "undefined") return fallback;
  return localStorage.getItem(key) || fallback;
};

export function ThemeProvider({ children }) {
  const [theme, setThemeState] = useState(() =>
    readStorage(THEME_STORAGE_KEY, DEFAULT_THEME),
  );
  const [brand, setBrandState] = useState(() =>
    readStorage(BRAND_STORAGE_KEY, DEFAULT_BRAND),
  );
  const { appConfig } = useAppContext();

  // Apply light/dark class to the html element whenever the theme changes.
  useEffect(() => {
    if (theme === "dark") {
      document.documentElement.classList.add("dark-theme");
    } else {
      document.documentElement.classList.remove("dark-theme");
    }
  }, [theme]);

  // Apply the selected Rijkshuisstijl palette as CSS custom properties.
  useEffect(() => {
    const root = document.documentElement;
    const variables = paletteToCssVariables(getBrandPalette(brand));

    Object.entries(variables).forEach(([property, value]) => {
      root.style.setProperty(property, value);
    });
  }, [brand]);

  // Load external CSS from backend config.
  useEffect(() => {
    if (!appConfig?.theme_css) return;

    if (document.querySelector(`link[href="${appConfig.theme_css}"]`)) return;

    const link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = appConfig.theme_css;
    link.type = "text/css";
    link.setAttribute("precedence", "default");

    document.head.appendChild(link);

    return () => {
      if (link.parentNode) link.parentNode.removeChild(link);
    };
  }, [appConfig?.theme_css]);

  const setTheme = (newTheme) => {
    setThemeState(newTheme);
    localStorage.setItem(THEME_STORAGE_KEY, newTheme);
  };

  const toggleTheme = () => {
    setTheme(theme === "light" ? "dark" : "light");
  };

  const setBrand = (newBrand) => {
    if (!BRAND_PALETTES[newBrand]) return;
    setBrandState(newBrand);
    localStorage.setItem(BRAND_STORAGE_KEY, newBrand);
  };

  const palette = getBrandPalette(brand);

  const antdConfig = useMemo(
    () => ({
      algorithm:
        theme === "dark" ? antdTheme.darkAlgorithm : antdTheme.defaultAlgorithm,
      token: {
        colorPrimary: palette.primary,
        colorInfo: palette.accent,
        colorLink: palette.accent,
        colorLinkHover: palette.primaryHover,
        borderRadius: 0,
        fontFamily: '"RijksSansVF", "Fira Sans", "Segoe UI", Arial, sans-serif',
      },
    }),
    [theme, palette],
  );

  return (
    <ConfigProvider theme={antdConfig}>
      <ThemeContext.Provider
        value={{
          theme,
          setTheme,
          toggleTheme,
          brand,
          setBrand,
          palettes: BRAND_PALETTES,
        }}
      >
        {children}
      </ThemeContext.Provider>
    </ConfigProvider>
  );
}

export function useTheme() {
  return useContext(ThemeContext);
}
