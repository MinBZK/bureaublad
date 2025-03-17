'use client'

import {useContext, useEffect, useState} from "react";
import {keycloak} from "@/app/auth/keycloak";
import {KeycloakContext} from "@/app/auth/KeycloakProvider";

function MijnTakenItems() {
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [items, setItems] = useState([]);

  const keycloakContext = useContext(KeycloakContext);

  useEffect(() => {
    if (keycloakContext.authenticated) {
      fetch("http://localhost:8000/v1/nextcloud/activities", {
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
  }, [keycloakContext])

  if (error) {
    return <div>Foutmelding: {error.message}</div>;
  } else if (!isLoaded) {
    return <div>Laden...</div>;
  } else {
    return (
      <div>
        {items.map(item => (
          <a href={item.url} key={item.activity_id} className="rvo-link rvo-link--with-icon rvo-link--no-underline rvo-link--zwart rvo-link--normal" target="_blank">
            <div>
              <div
                className="rvo-layout-row rvo-layout-align-items-start rvo-layout-align-content-start rvo-layout-justify-items-start rvo-layout-justify-content-start rvo-layout-gap--0">
                <div className="rvo-margin--sm">
                  <span className="utrecht-icon rvo-icon rvo-icon-document-met-lijnen rvo-icon--xl rvo-icon--hemelblauw" role="img"
                        aria-label="Document met lijnen"></span>
                </div>
                <div>
                  <span className="openbsw-document-titel">{item.title}</span><br/>
                  <span className="openbsw-document-datum">{item.updated_date}</span>
                </div>
              </div>
            </div>
          </a>
        ))}
      </div>
    );
  }
}

export default function MijnTaken() {
  return (
    <div className="openbsw-panel">
      <h4>Mijn taken</h4>
      <div className="rvo-scrollable-content openbsw-panel-scrollable-content">
        <MijnTakenItems></MijnTakenItems>
      </div>
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
  )
}