import ApplicatieBar from "./components/applicatieBar";
import SiteAlert from "./components/siteAlert";
import MijnDocumenten from "./components/mijnDocumenten";
import MijnTaken from "./components/mijnTaken";
import MijnDossiers from "./components/mijnDossiers";
import Updates from "./components/updates";
import MijnKalender from "./components/mijnKalender";

export function valueOrEmptyString(textContent: string | null | undefined): string {
  if (textContent) {
    return textContent;
  }
  return '';
}

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
            <MijnDossiers baseUrl={valueOrEmptyString(process.env.BACKEND_BASE_URL)}></MijnDossiers>
            <MijnKalender baseUrl={valueOrEmptyString(process.env.BACKEND_BASE_URL)}></MijnKalender>
          </div>
        </div>

        <ApplicatieBar/>

        <div className="rvo-layout-grid-container openbsw-panel-container">
          <div
            className="rvo-layout-grid rvo-layout-gap--md rvo-layout-grid-columns--three rvo-layout-grid--division"
            style={{"--division": "1fr 1fr 1fr"}}
          >
            <MijnDocumenten baseUrl={valueOrEmptyString(process.env.BACKEND_BASE_URL)}></MijnDocumenten>
            <MijnTaken baseUrl={valueOrEmptyString(process.env.BACKEND_BASE_URL)}></MijnTaken>
            <Updates></Updates>
          </div>
        </div>

      </div>
    </main>
  );
}
