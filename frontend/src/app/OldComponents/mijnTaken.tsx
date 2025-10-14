"use client";

import { useContext, useEffect, useState } from "react";
import { KeycloakContext } from "../Context/auth/KeycloakProvider";
import { keycloak } from "../Context/auth/keycloak";
import LifecycleTag from "@/app/OldComponents/lifecycleTag";

interface TakenItemsData {
  url: string;
  title: string;
  end: string;
  start: string;
}

interface MijnTakenItemsProps {
  baseUrl: string;
}

function MijnTakenItems({ baseUrl }: MijnTakenItemsProps) {
  const [error, setError] = useState(new Error());
  const [isLoaded, setIsLoaded] = useState(false);
  const [items, setItems] = useState([] as TakenItemsData[]);

  const keycloakContext = useContext(KeycloakContext);

  useEffect(() => {
    if (keycloakContext.authenticated) {
      fetch(baseUrl + "/v1/caldav/tasks", {
        method: "GET",
        mode: "cors",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          Authorization: `Bearer ${keycloak.token}`,
        },
      })
        .then((res) => res.json())
        .then(
          (result) => {
            setIsLoaded(true);
            if (result.detail) {
              setError(result.detail);
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
          },
        );
    }
  }, [keycloakContext, baseUrl]);

  if (error.message) {
    return <div>Foutmelding: {error.message}</div>;
  } else if (!isLoaded) {
    return <div>Laden...</div>;
  } else {
    return (
      <div>
        {items.map((item) => (
          <a
            href={item.url}
            key={item.title + "/" + item.start}
            className="rvo-link rvo-link--with-icon rvo-link--no-underline rvo-link--zwart rvo-link--normal"
            target="_blank"
          >
            <div>
              <div className="rvo-layout-row rvo-layout-align-items-start rvo-layout-align-content-start rvo-layout-justify-items-start rvo-layout-justify-content-start rvo-layout-gap--0">
                <div className="rvo-margin--sm">
                  <span
                    className="utrecht-icon rvo-icon rvo-icon-kalender-met-vinkje rvo-icon--xl rvo-icon--hemelblauw"
                    role="img"
                    aria-label="Kalender met vinkje"
                  ></span>
                </div>
                <div>
                  <span className="openbsw-document-titel">{item.title}</span>
                  <br />
                  {item.end && (
                    <span className="openbsw-document-datum">
                      Tot:{" "}
                      {new Date(Date.parse(item.end)).toLocaleString("nl-NL", {
                        timeStyle: "short",
                        dateStyle: "short",
                      })}
                    </span>
                  )}
                  {!item.end && item.start && (
                    <span className="openbsw-document-datum">
                      Vanaf:{" "}
                      {new Date(Date.parse(item.start)).toLocaleString(
                        "nl-NL",
                        {
                          timeStyle: "short",
                          dateStyle: "short",
                        },
                      )}
                    </span>
                  )}
                </div>
              </div>
            </div>
          </a>
        ))}
      </div>
    );
  }
}

interface MijnTakenProps {
  baseUrl: string;
}

export default function MijnTaken({ baseUrl }: MijnTakenProps) {
  return (
    <div className="openbsw-panel">
      <LifecycleTag status={"In ontwikkeling"} mode={"long"} />
      <h4>Mijn taken</h4>
      <div className="rvo-scrollable-content openbsw-panel-scrollable-content">
        <MijnTakenItems baseUrl={baseUrl}></MijnTakenItems>
      </div>
      <p className="utrecht-button-group">
        <a
          className="utrecht-button utrecht-button--primary-action utrecht-button--rvo-sm"
          href="https://files.la-suite.apps.digilab.network/apps/tasks/collections/all"
          target="_blank"
        >
          <span
            className="utrecht-icon rvo-icon rvo-icon-plus rvo-icon--sm rvo-icon--hemelblauw"
            role="img"
            aria-label="Plus"
          ></span>
          Nieuwe taak
        </a>
      </p>
    </div>
  );
}
