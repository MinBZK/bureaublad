import type { Metadata } from "next";
import "./globals.css";
import React from "react";
import UserMenu from "@/app/components/userMenu";
import {KeycloakProvider} from "@/app/auth/KeycloakProvider";
import Search from "@/app/components/search";

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
        <body className="rvo-theme openbsw-bureaublad">
          {/*<header className="openbsw-bureaublad-header">*/}
          {/*  <div className="rvo-header openbsw-bureaublad-header-image"></div>*/}
          {/*</header>*/}

          <div className="rvo-menubar__background rvo-menubar__background--horizontal-rule openbsw-menubar">
            <div className="rvo-max-width-layout rvo-max-width-layout--md rvo-max-width-layout-inline-padding--none">
              <nav className="rvo-menubar rvo-menubar--lg">
                <ul className="rvo-menubar__list">
                  <li className="rvo-menubar__item">
                    <a className="rvo-link rvo-menubar__link rvo-link--logoblauw" href="#">
                      <span className="utrecht-icon rvo-icon rvo-icon-home rvo-icon--md rvo-icon--hemelblauw" role="img"
                            aria-label="Home"></span>
                      Home
                    </a></li>
                  <li className="rvo-menubar__item">
                    <Search baseUrl={process.env.BACKEND_BASE_URL}></Search>
                  </li>
                  <li className="rvo-menubar__item rvo-menubar__item--active rvo-menubar__item--align-right">
                    <UserMenu></UserMenu>
                  </li>
                </ul>
              </nav>
            </div>
          </div>
          {children}
        </body>
      </KeycloakProvider>
    </html>
  );
}
