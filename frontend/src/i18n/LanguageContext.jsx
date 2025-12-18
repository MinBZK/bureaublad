"use client";

import { createContext, useContext, useState } from "react";
import { INITIAL_LOCALE, LOCALE_STORAGE_LANG_KEY } from "./config";

const LanguageContext = createContext({
  locale: "nl",
  setLocale: () => {},
});
// Language Provider to manage and provide current locale and set the language in the header
export function LanguageProvider({ children, initialLocale = INITIAL_LOCALE }) {
  // Initialize locale from localStorage or use initialLocale
  const [locale, setLocaleState] = useState(() => {
    if (typeof window !== "undefined") {
      const savedLocale = localStorage.getItem(LOCALE_STORAGE_LANG_KEY);
      return savedLocale || initialLocale;
    }
    return initialLocale;
  });

  // Custom setLocale that saves to localStorage
  const setLocale = (newLocale) => {
    setLocaleState(newLocale);
    if (typeof window !== "undefined") {
      localStorage.setItem(LOCALE_STORAGE_LANG_KEY, newLocale);
    }
  };

  return (
    <LanguageContext.Provider value={{ locale, setLocale }}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage() {
  return useContext(LanguageContext);
}
