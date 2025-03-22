'use client'

import {useContext, useEffect, useState} from "react";
import {keycloak} from "../auth/keycloak";
import {KeycloakContext} from "../auth/KeycloakProvider";
import FileTypeIcon from "./fileTypeIcon";

interface MijnDocumentenItemsProps {
  baseUrl?: string
}

interface DocumentenItemsData {
  url: string,
  object_filename: string,
  type: string,
  date: string,
  activity_id: string,
}

function MijnDocumentenItems({baseUrl}: MijnDocumentenItemsProps) {
  const [error, setError] = useState(new Error());
  const [isLoaded, setIsLoaded] = useState(false);
  const [items, setItems] = useState([] as DocumentenItemsData[]);

  const keycloakContext = useContext(KeycloakContext);

  useEffect(() => {
    if (keycloakContext.authenticated) {
      fetch(baseUrl + "/v1/ocs/activities", {
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
  }, [keycloakContext, baseUrl])

  if (error.message) {
    return <div>Foutmelding: {error.message}</div>;
  } else if (!isLoaded) {
    return <div>Laden...</div>;
  } else {
    return (
      <div className="rvo-layout-column rvo-layout-gap--0">
        {items.map(item => (
          <a href={item.url} key={item.activity_id}
             className="rvo-link rvo-link--with-icon rvo-link--no-underline rvo-link--zwart rvo-link--normal"
             target="_blank">
            <div>
              <div
                className="rvo-layout-row rvo-layout-align-items-start rvo-layout-align-content-start rvo-layout-justify-items-start rvo-layout-justify-content-start rvo-layout-gap--0">
                <div className="rvo-margin--sm">
                  <FileTypeIcon fileName={item.object_filename}></FileTypeIcon>
                </div>
                <div>
                  <span className="openbsw-document-titel">{item.object_filename}</span><br/>
                  <span className="openbsw-document-datum">{item.type} {item.date}</span>
                </div>
              </div>
            </div>
          </a>
        ))}
      </div>
    );
  }
}

interface MijnDocumentenProps {
  baseUrl: string
}

export default function MijnDocumenten({baseUrl}: MijnDocumentenProps) {
  return (
    <div className="openbsw-panel">
      <h4>Mijn documenten</h4>
      {/*<ul*/}
      {/*  className="rvo-tabs rvo-ul rvo-ul--no-margin rvo-ul--no-padding rvo-ul--icon rvo-ul--icon-option-2 openbsw-tabs"*/}
      {/*  role="tablist"*/}
      {/*  aria-label="Tabs"*/}
      {/*>*/}
      {/*  <li role="presentation" className="rvo-tabs__item">*/}
      {/*    <a*/}
      {/*      className="rvo-link rvo-tabs__item-link rvo-tabs__item-link--active rvo-link--active rvo-link--no-underline"*/}
      {/*      role="tab"*/}
      {/*      aria-selected="true"*/}
      {/*      href="#tab-1"*/}
      {/*    >*/}
      {/*      Recent*/}
      {/*    </a>*/}
      {/*  </li>*/}
      {/*  <li role="presentation" className="rvo-tabs__item">*/}
      {/*    <a*/}
      {/*      className="rvo-link rvo-tabs__item-link rvo-link--no-underline rvo-link--normal"*/}
      {/*      role="tab"*/}
      {/*      aria-selected="false"*/}
      {/*      href="#tab-2"*/}
      {/*    >*/}
      {/*      Favorieten*/}
      {/*    </a>*/}
      {/*  </li>*/}
      {/*</ul>*/}
      {/*<div id="tab-1">*/}
      {/*</div>*/}
      {/*<div id="tab-2">*/}
      {/*</div>*/}
      <div className="rvo-scrollable-content openbsw-panel-scrollable-content">
        <MijnDocumentenItems baseUrl={baseUrl}></MijnDocumentenItems>
      </div>
      <p className="utrecht-button-group openbsw-">
        <a
          className="utrecht-button utrecht-button--primary-action utrecht-button--rvo-sm rvo-link--no-underline"
          href="https://docs.la-suite.apps.digilab.network/docs/"
          target="_blank"
        >
          <span
            className="utrecht-icon rvo-icon rvo-icon-plus rvo-icon--sm rvo-icon--hemelblauw"
            role="img"
            aria-label="Plus"
          ></span>
          Nieuw document
        </a>
      </p>
    </div>
  )
}