import "./globals.css";
import "./custom-style.css";

import { AppProvider } from "./Components/Context/AppContext";
import ThemeLoader from "./Components/ThemeLoader/ThemeLoader";
import PageLayout from "./Components/Layout/PageLayout";
import { TranslationsProvider } from "../i18n/TranslationsProvider";
import { LanguageProvider } from "../i18n/LanguageContext";
import { getTranslations, INITIAL_LOCALE } from "../i18n/config";

export const metadata = {
  title: "Mijn Bureaublad",
  description: "Open BSW bureaublad",
};

export default async function RootLayout({ children }) {
  const messages = await getTranslations(INITIAL_LOCALE);
  return (
    <html lang={INITIAL_LOCALE}>
      <body suppressHydrationWarning>
        <LanguageProvider initialLocale={INITIAL_LOCALE}>
          <TranslationsProvider initialMessages={messages}>
            <AppProvider>
              <ThemeLoader />
              <PageLayout>{children}</PageLayout>
            </AppProvider>
          </TranslationsProvider>
        </LanguageProvider>
      </body>
    </html>
  );
}
