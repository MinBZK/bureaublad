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

// Add response interceptor to handle token refresh conflicts (409)
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 409) {
      const retryCount = error.config._retryCount || 0;
      if (retryCount < 3) {
        error.config._retryCount = retryCount + 1;
        // Exponential backoff: 200ms, 400ms, 800ms
        await new Promise((r) => setTimeout(r, 200 * Math.pow(2, retryCount)));
        return api.request(error.config);
      }
    }
    return Promise.reject(error);
  },
);

export default api;
