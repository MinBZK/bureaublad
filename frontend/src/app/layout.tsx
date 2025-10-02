import type { Metadata } from "next";
// import "./globals.css";
import React from "react";
import { KeycloakProvider } from "./auth/KeycloakProvider";
import PageLayout from "./Components/PageLayout";

export const metadata: Metadata = {
  title: "Mijn Bureaublad",
  description: "Open BSW bureaublad",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <KeycloakProvider>
        <body>
          <PageLayout>{children}</PageLayout>
        </body>
      </KeycloakProvider>
    </html>
  );
}
