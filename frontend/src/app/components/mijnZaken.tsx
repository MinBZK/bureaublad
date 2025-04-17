'use client'

import {useContext, useEffect, useState} from "react";
import {keycloak} from "../auth/keycloak";
import {KeycloakContext} from "../auth/KeycloakProvider";
import {CustomModal} from "./customModal";

interface MijnZakenItemsProps {
  baseUrl: string
}

interface MijnZakenItemsData {
  identificatie: string;
  url: string,
  uuid: string,
  omschrijving: string,
  toelichting?: string
  startdatum: string,
  einddatum?: string;
  archiefstatus: string;
  vertrouwelijkheidaanduiding: string;
  verantwoordelijkeOrganisatie: string;
  registratiedatum: string;
  zaaktype: string;
  bronorganisatie: string;
}

interface MijnZakenItemProps {
  zaakItem: MijnZakenItemsData
}

function MijnZakenItem({zaakItem}: MijnZakenItemProps) {
  const [isCustomModalOpen, setIsCustomModalOpen] = useState(false);

  return (
    <a href="#"
       onClick={() => setIsCustomModalOpen(true)}
       className="rvo-link rvo-link--with-icon rvo-link--no-underline rvo-link--zwart rvo-link--normal">
      <div>
        <div
          className="rvo-layout-row rvo-layout-align-items-start rvo-layout-align-content-start rvo-layout-justify-items-start rvo-layout-justify-content-start rvo-layout-gap--0">
          <div className="rvo-margin--sm">
                <span className="utrecht-icon rvo-icon rvo-icon-map rvo-icon--xl rvo-icon--hemelblauw" role="img"
                      aria-label="Map"></span>
          </div>
          <div>
            <span className="openbsw-document-titel">{zaakItem.omschrijving}</span><br/>
            <span className="openbsw-document-datum">{zaakItem.startdatum}</span>
          </div>
        </div>
      </div>
      {isCustomModalOpen &&
        <CustomModal onClose={() => setIsCustomModalOpen(false)} title={zaakItem.omschrijving}>
            <h3>Toelichting</h3>
            <p>
                OpenZaak is een API-systeem. Het is de bedoeling om vanuit applicaties hiermee
                te integreren om zaken en documenten te beheren. In het kader van Open BSW is
                hier geen applicatie voor beschikbaar. Vandaar dat hier alleen een overzicht
                van enkele facetten van een zaak worden getoond.
            </p>
          <dl className="rvo-data-list">
            <dt>Titel</dt>
            <dd>{zaakItem.omschrijving}</dd>
            <dt>Toelichting</dt>
            <dd>{zaakItem.toelichting}</dd>
            <dt>Identificatie</dt>
            <dd>{zaakItem.identificatie}</dd>
            <dt>Bronorganisatie</dt>
            <dd>{zaakItem.bronorganisatie}</dd>
            <dt>Zaaktype</dt>
            <dd>{zaakItem.zaaktype}</dd>
            <dt>Registratiedatum</dt>
            <dd>{zaakItem.registratiedatum}</dd>
            <dt>Verantwoordelijke organisatie</dt>
            <dd>{zaakItem.verantwoordelijkeOrganisatie}</dd>
            <dt>Startdatum</dt>
            <dd>{zaakItem.startdatum}</dd>
            <dt>Einddatum</dt>
            <dd>{zaakItem.einddatum}</dd>
            <dt>Vertrouwelijkheidaanduiding</dt>
            <dd>{zaakItem.vertrouwelijkheidaanduiding}</dd>
            <dt>Archiefstatus</dt>
            <dd>{zaakItem.archiefstatus}</dd>
            <dt>UUID</dt>
            <dd>{zaakItem.uuid}</dd>
          </dl>
        </CustomModal>
      }
    </a>
  );
}

function MijnZakenItems({baseUrl}: MijnZakenItemsProps) {
  const [error, setError] = useState(new Error());
  const [isLoaded, setIsLoaded] = useState(false);
  const [items, setItems] = useState([] as MijnZakenItemsData[]);

  const keycloakContext = useContext(KeycloakContext);

  useEffect(() => {
    if (keycloakContext.authenticated) {
      fetch(baseUrl + "/v1/zaken/zaken", {
        method: "GET",
        mode: "cors",
        headers: {
          "Accept": "application/json",
          "Content-Type": "application/json",
          "Authorization": `Bearer ${keycloak.token}`,
        }
      })
        .then(res => res.json())
        .then(
          (result) => {
            setIsLoaded(true);
            if (result.detail) {
              setError(result.detail)
            } else {
              setItems(result);
            }
          },
          // Note: it's important to handle errors here
          // instead of a catch() block so that we don't swallow
          // exceptions from actual bugs in components.
          (error) => {
            setIsLoaded(true);
            setError(error);
          }
        )
    }
  }, [keycloakContext, baseUrl]);

  if (error.message) {
    return <div>Foutmelding: {error.message}</div>;
  } else if (!isLoaded) {
    return <div>Laden...</div>;
  } else {
    return (
      <div className="rvo-layout-column rvo-layout-gap--0">
        {items.map(item => (
          <MijnZakenItem  key={item.uuid} zaakItem={item}/>
        ))}
      </div>
    );
  }
}

interface MijnZakenProps {
  baseUrl: string
}

export default function MijnZaken({baseUrl}: MijnZakenProps) {
  return (
    <div className="openbsw-panel">
      <h4>Mijn zaken</h4>
      <div className="rvo-scrollable-content openbsw-panel-scrollable-content">
        <MijnZakenItems baseUrl={baseUrl}></MijnZakenItems>
      </div>
      {/*<p className="utrecht-button-group openbsw-">*/}
      {/*  <a*/}
      {/*    className="utrecht-button utrecht-button--primary-action utrecht-button--rvo-sm rvo-link--no-underline"*/}
      {/*    href="https://docs.la-suite.apps.digilab.network/docs/"*/}
      {/*    target="_blank"*/}
      {/*  >*/}
      {/*    <span*/}
      {/*      className="utrecht-icon rvo-icon rvo-icon-plus rvo-icon--sm rvo-icon--hemelblauw"*/}
      {/*      role="img"*/}
      {/*      aria-label="Plus"*/}
      {/*    ></span>*/}
      {/*    Nieuwe zaak*/}
      {/*  </a>*/}
      {/*  <a*/}
      {/*    className="utrecht-button utrecht-button--secondary-action utrecht-button--rvo-sm  rvo-link--no-underline"*/}
      {/*    href="https://docs.la-suite.apps.digilab.network/docs/"*/}
      {/*    target="_blank"*/}
      {/*  >*/}
      {/*    Al mijn zaken*/}
      {/*  </a>*/}
      {/*</p>*/}
    </div>
  )
}