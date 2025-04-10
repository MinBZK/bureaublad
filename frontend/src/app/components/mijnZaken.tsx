'use client'

import {useContext, useEffect, useState} from "react";
import {keycloak} from "../auth/keycloak";
import {KeycloakContext} from "../auth/KeycloakProvider";

interface MijnZakenItemsProps {
  baseUrl: string
}

interface MijnZakenItemsData {
  url: string,
  uuid: string,
  omschrijving: string,
  startdatum: string,
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
          <a href={item.url} key={item.uuid}
             className="rvo-link rvo-link--with-icon rvo-link--no-underline rvo-link--zwart rvo-link--normal"
             target="_blank">
            <div>
              <div
                className="rvo-layout-row rvo-layout-align-items-start rvo-layout-align-content-start rvo-layout-justify-items-start rvo-layout-justify-content-start rvo-layout-gap--0">
                <div className="rvo-margin--sm">
                  <span className="utrecht-icon rvo-icon rvo-icon-map rvo-icon--xl rvo-icon--hemelblauw" role="img"
                        aria-label="Map"></span>
                </div>
                <div>
                  <span className="openbsw-document-titel">{item.omschrijving}</span><br/>
                  <span className="openbsw-document-datum">{item.startdatum}</span>
                </div>
              </div>
            </div>
          </a>
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