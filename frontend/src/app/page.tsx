import ApplicatieBar from "@/app/components/applicatieBar";
import SiteAlert from "@/app/components/siteAlert";
import MijnDocumenten from "@/app/components/mijnDocumenten";
import MijnTaken from "@/app/components/mijnTaken";
import MijnDossiers from "@/app/components/mijnDossiers";
import Updates from "@/app/components/updates";

export default function Home() {
  return (
    <main className="content">
      <div
        className="rvo-max-width-layout rvo-max-width-layout--md rvo-min-width-layout--sm openbsw-alert">
        <SiteAlert/>

        <div className="rvo-layout-grid-container openbsw-panel-container">
          <div
            className="rvo-layout-grid rvo-layout-gap--md rvo-layout-grid-columns--two rvo-layout-grid--division"
            style={{"--division": "1fr 1fr"}}
          >
            <MijnDossiers></MijnDossiers>
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

        <ApplicatieBar/>

        <div className="rvo-layout-grid-container openbsw-panel-container">
          <div
            className="rvo-layout-grid rvo-layout-gap--md rvo-layout-grid-columns--three rvo-layout-grid--division"
            style={{"--division": "1fr 1fr 1fr"}}
          >
            <MijnDocumenten></MijnDocumenten>
            <MijnTaken></MijnTaken>
            <Updates></Updates>
          </div>
        </div>

      </div>
    </main>
  );
}
