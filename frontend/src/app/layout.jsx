// import "./globals.css";
import React from "react";
import { KeycloakProvider } from "./Context/auth/KeycloakProvider";
import PageLayout from "./Layout/PageLayout";
import { AppProvider } from "./Context/AppContext";
export const metadata = {
  title: "Mijn Bureaublad",
  description: "Open BSW bureaublad",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <KeycloakProvider>
        <body>
          <AppProvider>
            <PageLayout>{children}</PageLayout>
          </AppProvider>
        </body>
      </KeycloakProvider>
    </html>
  );
}
