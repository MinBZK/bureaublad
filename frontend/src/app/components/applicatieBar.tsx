import LifecycleTag from "@/app/components/lifecycleTag";

interface Applicatie {
  id: number;
  title: string;
  url: string;
  iconClass: string;
  iconLabel: string;
  status: "In ontwikkeling" | "Proef" | "Productie";
}

const applicaties: Applicatie[] = [
  {
    id: 0,
    title: "Chat",
    url: "https://chat.la-suite.apps.digilab.network/",
    iconClass: "rvo-icon-tekstballonnen-met-punten",
    iconLabel: "Tekstballonnen met punten",
    status: "In ontwikkeling",
  },
  {
    id: 1,
    title: "Meet",
    url: "https://meet.la-suite.apps.digilab.network/",
    iconClass: "rvo-icon-silhouet-voor-scherm-raam-met-silhouet",
    iconLabel: "Silhouet voor scherm met silhouet",
    status: "In ontwikkeling",
  },
  {
    id: 10,
    title: "Docs",
    url: "https://docs.la-suite.apps.digilab.network/",
    iconClass: "rvo-icon-document-met-potlood",
    iconLabel: "Document met potlood",
    status: "In ontwikkeling",
  },
  {
    id: 12,
    title: "Drive",
    url: "https://drive.la-suite.apps.digilab.network/",
    iconClass: "rvo-icon-map",
    iconLabel: "Map",
    status: "In ontwikkeling",
  },
  {
    id: 2,
    title: "Spread-sheets",
    url: "https://grist.la-suite.apps.digilab.network/",
    iconClass: "rvo-icon-grafiek",
    iconLabel: "Spread-sheets",
    status: "In ontwikkeling",
  },
  {
    id: 5,
    title: "Projecten",
    url: "https://projects.opendesk.apps.digilab.network/auth/keycloak",
    iconClass: "rvo-icon-bord-met-grafieken",
    iconLabel: "Bord met grafieken",
    status: "In ontwikkeling",
  },
  {
    id: 6,
    title: "Kennis",
    url: "https://wiki.opendesk.apps.digilab.network/",
    iconClass: "rvo-icon-online-leren",
    iconLabel: "Online leren",
    status: "In ontwikkeling",
  },
  {
    id: 8,
    title: "AI assistent",
    url: "https://ai-assistant.la-suite.apps.digilab.network/",
    iconClass: "rvo-icon-half-tandwiel-half-brein",
    iconLabel: "Half tandwiel half brein",
    status: "In ontwikkeling",
  },
  {
    id: 3,
    title: "Files",
    url: "https://files.la-suite.apps.digilab.network/",
    iconClass: "rvo-icon-map-vol-documenten",
    iconLabel: "Map vol documenten",
    status: "In ontwikkeling",
  },
  {
    id: 11,
    title: "Kalender",
    url: "https://webmail.opendesk.apps.digilab.network/appsuite/#app=io.ox/calendar",
    iconClass: "rvo-icon-kalender",
    iconLabel: "Kalender",
    status: "In ontwikkeling",
  },
  {
    id: 4,
    title: "Taken",
    url: "https://webmail.opendesk.apps.digilab.network/appsuite/#app=io.ox/tasks",
    iconClass: "rvo-icon-kalender-met-vinkje",
    iconLabel: "Kalender met vinkje",
    status: "In ontwikkeling",
  },
  {
    id: 7,
    title: "Wacht-woord manager",
    url: "https://vault.la-suite.apps.digilab.network/",
    iconClass: "rvo-icon-sleutelbos",
    iconLabel: "Sleutelbos",
    status: "In ontwikkeling",
  },
  {
    id: 9,
    title: "OpenZaak",
    url: "https://open-zaak.commonground.apps.digilab.network/",
    iconClass: "rvo-icon-map-met-loep",
    iconLabel: "Map met loep",
    status: "In ontwikkeling",
  },
];

export default function ApplicatieBar() {
  const userApplicaties = applicaties
    .map((applicatie) => (
      <div key={applicatie.id} className="openbsw-applicatie-bar-item">
        <a
          className="rvo-link rvo-link--with-icon rvo-link--no-underline rvo-link--hemelblauw rvo-link--normal"
          href={applicatie.url}
          target="_blank"
        >
          <div className="rvo-layout-column rvo-layout-gap--2xs">
            <div className="openbsw-applicatie-bar-item-icon">
              <span
                className={
                  "utrecht-icon rvo-icon " +
                  applicatie.iconClass +
                  " rvo-icon--xl rvo-icon--zwart"
                }
                role="img"
                aria-label={applicatie.iconLabel}
              ></span>
            </div>
            <LifecycleTag status={applicatie.status} mode={"short"} />
            <div>{applicatie.title}</div>
          </div>
        </a>
      </div>
    ))
    .slice(0, 10);

  return (
    <div className="rvo-layout-grid-container">
      <div
        className="rvo-layout-grid rvo-layout-gap--xl rvo-layout-grid-columns--twelve rvo-layout-grid--division openbsw-applicatie-bar"
        style={
          {
            "--division": "2fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr",
          } as React.CSSProperties
        }
      >
        <div className="openbsw-applicatie-bar-head">
          <p>Mijn applicaties</p>
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
        {userApplicaties}
      </div>
    </div>
  );
}
