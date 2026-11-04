import "./globals.css";
import "./custom-style.css";

import { AppProvider } from "./Components/Context/AppContext";
import { ThemeProvider } from "./Components/Context/ThemeContext";
import PageLayout from "./Components/Layout/PageLayout";
import { TranslationsProvider } from "../i18n/TranslationsProvider";
import { LanguageProvider } from "../i18n/LanguageContext";
import { getTranslations, INITIAL_LOCALE } from "../i18n/config";
import { Suspense } from "react";
import Loading from "./Common/Loading";

export const metadata = {
  title: "Mijn Bureau",
  description:
    "De autonome, open source digitale werkplek voor de overheid. Veilig, zelf-gehost en volledig onder eigen regie.",
};

export default async function RootLayout({ children }) {
  const messages = await getTranslations(INITIAL_LOCALE);
  return (
    <html lang={INITIAL_LOCALE}>
      <body suppressHydrationWarning>
        <Suspense fallback={<Loading />}>
          <LanguageProvider initialLocale={INITIAL_LOCALE}>
            <TranslationsProvider initialMessages={messages}>
              <AppProvider>
                <ThemeProvider>
                  <PageLayout>{children}</PageLayout>
                </ThemeProvider>
              </AppProvider>
            </TranslationsProvider>
          </LanguageProvider>
        </Suspense>
      </body>
    </html>
  );
}
