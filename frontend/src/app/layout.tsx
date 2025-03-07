import type { Metadata } from "next";
import "./globals.css";

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
                  <div className="rvo-layout-row rvo-layout-gap--0 rvo-margin-inline-start--2xl">
                    <div>
                      <input id="field" placeholder="Zoek collega's, dossiers of vraag hulp van je persoonlijke assistent"
                             type="text" className="utrecht-textbox utrecht-textbox--html-input utrecht-textbox--lg"
                             dir="auto" defaultValue=""
    //                         style={{backgroundColor: "var(--rvo-color-grijs-100)", color: "var(--rvo-color-grijs-900)"}}
                      />
                    </div>
                    <div>
                      <button className="utrecht-button utrecht-button--primary-action utrecht-button--rvo-md"
                              type="button">
                        <span className="utrecht-icon rvo-icon rvo-icon-zoek rvo-icon--md rvo-icon--hemelblauw" role="img"
                              aria-label="Home"></span>
                      </button>
                    </div>
                  </div>
                </li>
                <li className="rvo-menubar__item rvo-menubar__item--active rvo-menubar__item--align-right">
                  <a
                    className="rvo-link rvo-menubar__link rvo-link--logoblauw" href="#">
                    <span className="utrecht-icon rvo-icon rvo-icon-user rvo-icon--md rvo-icon--hemelblauw" role="img"
                          aria-label="Home"></span>
                    Margriet de Wildt
                  </a>
                </li>
              </ul>
            </nav>
          </div>
        </div>
        {children}
      </body>
    </html>
  );
}
