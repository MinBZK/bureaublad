import "./globals.css";
import React from "react";
import { KeycloakProvider } from "./Context/auth/KeycloakProvider";
import PageLayout from "./Components/Layout/PageLayout";
import ThemeLoader from "./Components/ThemeLoader/ThemeLoader";
import { AppProvider } from "./Context/AppContext";
export const metadata = {
  title: "Mijn Bureaublad",
  description: "Open BSW bureaublad",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <AppProvider>
          <ThemeLoader />
          <PageLayout>{children}</PageLayout>
        </AppProvider>
      </body>
    </html>
  );
}
