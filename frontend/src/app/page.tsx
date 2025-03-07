import styles from "./page.module.css";

export default function Home() {
  return (
    <main className="content">
      <div
        className="rvo-max-width-layout rvo-max-width-layout--md rvo-min-width-layout--sm openbsw-alert">
        <div className="rvo-alert rvo-alert--info rvo-alert--padding-md" data-alert-id="index-poc-alert">
            <span className="utrecht-icon rvo-icon rvo-icon-info rvo-icon--xl rvo-status-icon-info" role="img"
                  aria-label="Info"></span>
          <div className="rvo-alert-text">
            <strong>Proof of Concept</strong>
            <div>
              <div>
                Dit systeem is nog in ontwikkeling. Er zijn geen garanties dat
                de data veilig blijft of bewaard blijft.
              </div>
            </div>
          </div>
          <button className="utrecht-button utrecht-button--subtle rvo-button__close utrecht-button--rvo-md"
                  type="button" aria-label="Sluiten">
              <span className="utrecht-icon rvo-icon rvo-icon-kruis rvo-icon--md rvo-icon--hemelblauw" role="img"
                    aria-label="Kruis"></span>
          </button>
        </div>

        <div className="rvo-layout-grid-container openbsw-panel-container">
          <div
            className="rvo-layout-grid rvo-layout-gap--md rvo-layout-grid-columns--two rvo-layout-grid--division"
            style={{"--division": "1fr 1fr"}}
          >
            <div className="openbsw-panel">
              <h4>Mijn dossiers</h4>
              <p className="utrecht-button-group">
                <button
                  className="utrecht-button utrecht-button--primary-action utrecht-button--rvo-sm"
                  type="button"
                >
                    <span
                      className="utrecht-icon rvo-icon rvo-icon-plus rvo-icon--sm rvo-icon--hemelblauw"
                      role="img"
                      aria-label="Plus"
                    ></span>
                  Nieuw dossier
                </button>
                <button
                  className="utrecht-button utrecht-button--secondary-action utrecht-button--rvo-sm"
                  type="button"
                >
                  Al mijn dossiers
                </button>
              </p>
            </div>
            <div className="openbsw-panel">
              <h4>Agenda afspraken</h4>
              <p className="utrecht-button-group">
                <button
                  className="utrecht-button utrecht-button--primary-action utrecht-button--rvo-sm"
                  type="button"
                >
                    <span
                      className="utrecht-icon rvo-icon rvo-icon-plus rvo-icon--sm rvo-icon--hemelblauw"
                      role="img"
                      aria-label="Plus"
                    ></span>
                  Afspraak inplannen
                </button>
                <button
                  className="utrecht-button utrecht-button--secondary-action utrecht-button--rvo-sm"
                  type="button"
                >
                  Mijn agenda
                </button>
              </p>
            </div>
          </div>
        </div>


        <div className="rvo-layout-grid-container">
          <div
            className="rvo-layout-grid rvo-layout-gap--xl rvo-layout-grid-columns--twelve rvo-layout-grid--division openbsw-applicatie-bar"
            style={{"--division": "2fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr"}}
          >
            <div className="openbsw-applicatie-bar-head">
              <p>
                Mijn applicaties
              </p>
              <a
                className="rvo-link rvo-link--with-icon rvo-link--no-underline rvo-link--hemelblauw rvo-link--normal"
                href="#"
              >
                bewerken
                <span
                  className="utrecht-icon rvo-icon rvo-icon-bewerken rvo-icon--sm rvo-icon--hemelblauw  rvo-link__icon--after"
                  role="img"
                  aria-label="Bewerken"
                ></span>
              </a>
            </div>
            <div className="openbsw-applicatie-bar-item">
              <div className="openbsw-applicatie-bar-item-icon">
                  <span
                    className="utrecht-icon rvo-icon rvo-icon-tekstballonnen-met-punten rvo-icon--xl rvo-icon--zwart"
                    role="img"
                    aria-label="Tekstballonnen met punten"
                  ></span>
              </div>
              <a
                className="rvo-link rvo-link--with-icon rvo-link--no-underline rvo-link--hemelblauw rvo-link--normal"
                href="#"
              >
                Chat
              </a>
            </div>
            {/*<div className="openbsw-applicatie-bar-item">*/}
            {/*  <div className="openbsw-applicatie-bar-item-icon">*/}
            {/*    <span*/}
            {/*      className="utrecht-icon rvo-icon rvo-icon-document-met-potlood rvo-icon--xl rvo-icon--zwart"*/}
            {/*      role="img"*/}
            {/*      aria-label="Document met potlood"*/}
            {/*    ></span>*/}
            {/*  </div>*/}
            {/*  <a*/}
            {/*    className="rvo-link rvo-link--with-icon rvo-link--no-underline rvo-link--hemelblauw rvo-link--normal"*/}
            {/*    href="#"*/}
            {/*  >*/}
            {/*    Docs*/}
            {/*  </a>*/}
            {/*</div>*/}
            <div className="openbsw-applicatie-bar-item">
              <div className="openbsw-applicatie-bar-item-icon">
                  <span
                    className="utrecht-icon rvo-icon rvo-icon-silhouet-voor-scherm-raam-met-silhouet rvo-icon--xl rvo-icon--zwart"
                    role="img"
                    aria-label="Silhouet voor scherm met silhouet"
                  ></span>
              </div>
              <a
                className="rvo-link rvo-link--with-icon rvo-link--no-underline rvo-link--hemelblauw rvo-link--normal"
                href="#"
              >
                Meet
              </a>
            </div>
            <div className="openbsw-applicatie-bar-item">
              <div className="openbsw-applicatie-bar-item-icon">
                  <span
                    className="utrecht-icon rvo-icon rvo-icon-grafiek rvo-icon--xl rvo-icon--zwart"
                    role="img"
                    aria-label="Grafiek"
                  ></span>
              </div>
              <a
                className="rvo-link rvo-link--with-icon rvo-link--no-underline rvo-link--hemelblauw rvo-link--normal"
                href="#"
              >
                Spread-sheets
              </a>
            </div>
            <div className="openbsw-applicatie-bar-item">
              <div className="openbsw-applicatie-bar-item-icon">
                    <span
                      className="utrecht-icon rvo-icon rvo-icon-map-vol-documenten rvo-icon--xl rvo-icon--zwart"
                      role="img"
                      aria-label="Map vol documenten"
                    ></span>
              </div>
              <a
                className="rvo-link rvo-link--with-icon rvo-link--no-underline rvo-link--hemelblauw rvo-link--normal"
                href="#"
              >
                Files
              </a>
            </div>
            <div className="openbsw-applicatie-bar-item">
              <div className="openbsw-applicatie-bar-item-icon">
                    <span
                      className="utrecht-icon rvo-icon rvo-icon-kalender rvo-icon--xl rvo-icon--zwart"
                      role="img"
                      aria-label="Kalender"
                    ></span>
              </div>
              <a
                className="rvo-link rvo-link--with-icon rvo-link--no-underline rvo-link--hemelblauw rvo-link--normal"
                href="#"
              >
                Kalender
              </a>
            </div>
            <div className="openbsw-applicatie-bar-item">
              <div className="openbsw-applicatie-bar-item-icon">
                    <span
                      className="utrecht-icon rvo-icon rvo-icon-kalender-met-vinkje rvo-icon--xl rvo-icon--zwart"
                      role="img"
                      aria-label="Kalender met vinkje"
                    ></span>
              </div>
              <a
                className="rvo-link rvo-link--with-icon rvo-link--no-underline rvo-link--hemelblauw rvo-link--normal"
                href="#"
              >
                Taken
              </a>
            </div>
            <div className="openbsw-applicatie-bar-item">
              <div className="openbsw-applicatie-bar-item-icon">
                    <span
                      className="utrecht-icon rvo-icon rvo-icon-bord-met-grafieken rvo-icon--xl rvo-icon--zwart"
                      role="img"
                      aria-label="Bord met grafieken"
                    ></span>
              </div>
              <a
                className="rvo-link rvo-link--with-icon rvo-link--no-underline rvo-link--hemelblauw rvo-link--normal"
                href="#"
              >
                Projecten
              </a>
            </div>
            <div className="openbsw-applicatie-bar-item">
              <div className="openbsw-applicatie-bar-item-icon">
                    <span
                      className="utrecht-icon rvo-icon rvo-icon-online-leren rvo-icon--xl rvo-icon--zwart"
                      role="img"
                      aria-label="Online leren"
                    ></span>
              </div>
              <a
                className="rvo-link rvo-link--with-icon rvo-link--no-underline rvo-link--hemelblauw rvo-link--normal"
                href="#"
              >
                Kennis
              </a>
            </div>
            <div className="openbsw-applicatie-bar-item">
              <div className="openbsw-applicatie-bar-item-icon">
                    <span
                      className="utrecht-icon rvo-icon rvo-icon-sleutelbos rvo-icon--xl rvo-icon--zwart"
                      role="img"
                      aria-label="Sleutelbos"
                    ></span>
              </div>
              <a
                className="rvo-link rvo-link--with-icon rvo-link--no-underline rvo-link--hemelblauw rvo-link--normal"
                href="#"
              >
                Wacht-woord manager
              </a>
            </div>
            <div className="openbsw-applicatie-bar-item">
              <div className="openbsw-applicatie-bar-item-icon">
                    <span
                      className="utrecht-icon rvo-icon rvo-icon-half-tandwiel-half-brein rvo-icon--xl rvo-icon--zwart"
                      role="img"
                      aria-label="Half tandwiel half brein"
                    ></span>
              </div>
              <a
                className="rvo-link rvo-link--with-icon rvo-link--no-underline rvo-link--hemelblauw rvo-link--normal"
                href="#"
              >
                AI assistent
              </a>
            </div>
          </div>
        </div>


        <div className="rvo-layout-grid-container openbsw-panel-container">
          <div
            className="rvo-layout-grid rvo-layout-gap--md rvo-layout-grid-columns--three rvo-layout-grid--division"
            style={{"--division": "1fr 1fr 1fr"}}
          >
            <div className="openbsw-panel">
              <h4>Mijn documenten</h4>
              <p className="utrecht-button-group">
                <button
                  className="utrecht-button utrecht-button--primary-action utrecht-button--rvo-sm"
                  type="button"
                >
                    <span
                      className="utrecht-icon rvo-icon rvo-icon-plus rvo-icon--sm rvo-icon--hemelblauw"
                      role="img"
                      aria-label="Plus"
                    ></span>
                  Nieuw document
                </button>
              </p>
            </div>
            <div className="openbsw-panel">
              <h4>Mijn taken</h4>
              <p className="utrecht-button-group">
                <button
                  className="utrecht-button utrecht-button--primary-action utrecht-button--rvo-sm"
                  type="button"
                >
                    <span
                      className="utrecht-icon rvo-icon rvo-icon-plus rvo-icon--sm rvo-icon--hemelblauw"
                      role="img"
                      aria-label="Plus"
                    ></span>
                  Nieuwe taak
                </button>
              </p>
            </div>
            <div className="openbsw-panel">
              <h4>Updates</h4>
              <p>
                <a
                  className="rvo-link rvo-link--with-icon rvo-link--hemelblauw rvo-link--normal"
                  href="#"
                >
                  Meer updates
                </a>
              </p>
            </div>
          </div>
        </div>

      </div>
    </main>
  );
}
