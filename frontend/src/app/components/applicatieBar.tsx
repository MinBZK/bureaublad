export default function ApplicatieBar() {
  return (
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
  )
}