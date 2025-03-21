const applicaties = [{
  id: 0,
  title: 'Chat',
  url: 'https://chat.la-suite.apps.digilab.network/',
  iconClass: 'rvo-icon-tekstballonnen-met-punten',
  iconLabel: 'Tekstballonnen met punten'
}, {
  id: 1,
  title: 'Meet',
  url: 'https://meet.la-suite.apps.digilab.network/',
  iconClass: 'rvo-icon-silhouet-voor-scherm-raam-met-silhouet',
  iconLabel: 'Silhouet voor scherm met silhouet'
}, {
  id: 2,
  title: 'Spread-sheets',
  url: 'https://grist.la-suite.apps.digilab.network/',
  iconClass: 'rvo-icon-grafiek',
  iconLabel: 'Spread-sheets'
}, {
  id: 3,
  title: 'Files',
  url: 'https://files.la-suite.apps.digilab.network/',
  iconClass: 'rvo-icon-map-vol-documenten',
  iconLabel: 'Map vol documenten'
}, {
  id: 4,
  title: 'Taken',
  url: 'https://webmail.opendesk.apps.digilab.network/appsuite/#app=io.ox/tasks',
  iconClass: 'rvo-icon-kalender-met-vinkje',
  iconLabel: 'Kalender met vinkje'
}, {
  id: 5,
  title: 'Projecten',
  url: 'https://projects.opendesk.apps.digilab.network/auth/keycloak',
  iconClass: 'rvo-icon-bord-met-grafieken',
  iconLabel: 'Bord met grafieken'
}, {
  id: 6,
  title: 'Kennis',
  url: 'https://wiki.opendesk.apps.digilab.network/',
  iconClass: 'rvo-icon-online-leren',
  iconLabel: 'Online leren'
}, {
  id: 7,
  title: 'Wacht-woord manager',
  url: 'https://vault.la-suite.apps.digilab.network/',
  iconClass: 'rvo-icon-sleutelbos',
  iconLabel: 'Sleutelbos'
}, {
  id: 8,
  title: 'AI assistent',
  url: 'https://ai-assistant.la-suite.apps.digilab.network/',
  iconClass: 'rvo-icon-half-tandwiel-half-brein',
  iconLabel: 'Half tandwiel half brein'
}, {
  id: 9,
  title: 'Kalender',
  url: 'https://webmail.opendesk.apps.digilab.network/appsuite/#app=io.ox/calendar',
  iconClass: 'rvo-icon-kalender',
  iconLabel: 'Kalender'
}, {
  id: 10,
  title: 'Docs',
  url: 'https://docs.la-suite.apps.digilab.network/',
  iconClass: 'rvo-icon-document-met-potlood',
  iconLabel: 'Docs'
}];

export default function ApplicatieBar() {
  const userApplicaties = applicaties.map(applicatie =>
    <div key={applicatie.id} className="openbsw-applicatie-bar-item">
      <div className="openbsw-applicatie-bar-item-icon">
        <span
          className={'utrecht-icon rvo-icon ' + applicatie.iconClass + ' rvo-icon--xl rvo-icon--zwart'}
          role="img"
          aria-label={applicatie.iconLabel}
        ></span>
      </div>
      <a
        className="rvo-link rvo-link--with-icon rvo-link--no-underline rvo-link--hemelblauw rvo-link--normal"
        href={applicatie.url}
      >
        {applicatie.title}
      </a>
    </div>
  ).slice(0, 10);

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
        {userApplicaties}
      </div>
    </div>
  )
}