import { INITIAL_LOCALE, LOCALE_STORAGE_LANG_KEY } from "@/i18n/config";
import axios from "axios";

const api = axios.create({
  baseURL: "/api/v1",
});

// Add request interceptor to include Accept-Language header
api.interceptors.request.use(
  (config) => {
    // Get locale from localStorage (same key as LanguageContext uses)
    const locale =
      typeof window !== "undefined"
        ? localStorage.getItem(LOCALE_STORAGE_LANG_KEY) || INITIAL_LOCALE
        : INITIAL_LOCALE;

    // Backend expects formats like 'nl-NL', 'en-US'
    // Convert 'nl' -> 'nl-NL', 'en' -> 'en-US', etc.
    const formattedLocale = locale.includes("-")
      ? locale
      : `${locale}-${locale.toUpperCase()}`;

    config.headers["Accept-Language"] = formattedLocale;
    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

export default api;
