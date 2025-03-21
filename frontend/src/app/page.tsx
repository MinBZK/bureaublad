import ApplicatieBar from "@/app/components/applicatieBar";
import SiteAlert from "@/app/components/siteAlert";
import MijnDocumenten from "@/app/components/mijnDocumenten";
import MijnTaken from "@/app/components/mijnTaken";
import MijnDossiers from "@/app/components/mijnDossiers";
import Updates from "@/app/components/updates";
import MijnKalender from "@/app/components/mijnKalender";

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
            <MijnDossiers baseUrl={process.env.BACKEND_BASE_URL}></MijnDossiers>
            <MijnKalender baseUrl={process.env.BACKEND_BASE_URL}></MijnKalender>
          </div>
        </div>

        <ApplicatieBar/>

        <div className="rvo-layout-grid-container openbsw-panel-container">
          <div
            className="rvo-layout-grid rvo-layout-gap--md rvo-layout-grid-columns--three rvo-layout-grid--division"
            style={{"--division": "1fr 1fr 1fr"}}
          >
            <MijnDocumenten baseUrl={process.env.BACKEND_BASE_URL}></MijnDocumenten>
            <MijnTaken baseUrl={process.env.BACKEND_BASE_URL}></MijnTaken>
            <Updates></Updates>
          </div>
        </div>

      </div>
    </main>
  );
}
