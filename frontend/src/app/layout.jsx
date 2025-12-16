import "./globals.css";
import "./custom-style.css";

import { AppProvider } from "./Components/Context/AppContext";
import ThemeLoader from "./Components/ThemeLoader/ThemeLoader";
import PageLayout from "./Components/Layout/PageLayout";
import { Suspense } from "react";
import Loading from "./Common/Loading";

export const metadata = {
  title: "Mijn Bureaublad",
  description: "Open BSW bureaublad",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body suppressHydrationWarning>
        <Suspense fallback={<Loading />}>
          <AppProvider>
            <ThemeLoader />
            <PageLayout>{children}</PageLayout>
          </AppProvider>
        </Suspense>
      </body>
    </html>
  );
}
