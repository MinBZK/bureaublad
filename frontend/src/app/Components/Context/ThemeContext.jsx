"use client";

import { createContext, useContext, useState, useEffect } from "react";
import { useAppContext } from "./AppContext";

const THEME_STORAGE_KEY = "theme";
const DEFAULT_THEME = "light";

const ThemeContext = createContext({
  theme: DEFAULT_THEME,
  setTheme: () => {},
  toggleTheme: () => {},
});

export function ThemeProvider({ children }) {
  const [theme, setThemeState] = useState(() => {
    if (typeof window !== "undefined") {
      return localStorage.getItem(THEME_STORAGE_KEY) || DEFAULT_THEME;
    }
    return DEFAULT_THEME;
  });
  const { appConfig } = useAppContext();

  // Apply theme class to html element whenever theme changes
  useEffect(() => {
    if (theme === "dark") {
      document.documentElement.classList.add("dark-theme");
    } else {
      document.documentElement.classList.remove("dark-theme");
    }
  }, [theme]);

  // Load external CSS from backend config
  useEffect(() => {
    if (!appConfig?.theme_css) return;

    // Check if we already added this link (avoid duplicates)
    if (document.querySelector(`link[href="${appConfig.theme_css}"]`)) return;

    // Create a new <link> element for the custom stylesheet
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
    const newTheme = theme === "light" ? "dark" : "light";
    setTheme(newTheme);
  };

  return (
    <ThemeContext.Provider value={{ theme, setTheme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  return useContext(ThemeContext);
}
