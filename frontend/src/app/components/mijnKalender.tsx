'use client'

import {useContext, useEffect, useState} from "react";
import {keycloak} from "../auth/keycloak";
import {KeycloakContext} from "../auth/KeycloakProvider";
import LifecycleTag from "@/app/components/lifecycleTag";

interface MijnKalenderItemsProps {
  baseUrl: string
}

interface MijnKalenderItemsData {
  title: string,
  start: string,
  end: string,
}

function MijnKalenderItems({baseUrl}: MijnKalenderItemsProps) {
  const [error, setError] = useState(new Error());
  const [isLoaded, setIsLoaded] = useState(false);
  const [items, setItems] = useState([] as MijnKalenderItemsData[]);

  const keycloakContext = useContext(KeycloakContext);

  useEffect(() => {
    if (keycloakContext.authenticated) {
      const today = new Date().toISOString().substring(0, 10);
      fetch(baseUrl + "/v1/caldav/calendars/" + today, {
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
          <div key={item.title + '/' + item.start}>
            <div
              className="rvo-layout-row rvo-layout-align-items-start rvo-layout-align-content-start rvo-layout-justify-items-start rvo-layout-justify-content-start rvo-layout-gap--0">
              <div className="rvo-margin--sm">
                  <span
                    className="utrecht-icon rvo-icon rvo-icon-kalender-met-vlakken rvo-icon--xl rvo-icon--hemelblauw"
                    role="img"
                    aria-label="Kalender met vlakken"></span>
              </div>
              <div>
                <span className="openbsw-document-titel">{item.title}</span><br/>
                <span className="openbsw-document-datum">
                  {new Date(Date.parse(item.start)).toLocaleTimeString('nl-NL', {timeStyle: "short"})} - {new Date(Date.parse(item.end)).toLocaleTimeString('nl-NL', {timeStyle: "short"})}
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>
    );
  }
}

interface MijnKalenderProps {
  baseUrl: string
}

export default function MijnKalender({baseUrl}: MijnKalenderProps) {
  const nextHour = new Date();
  nextHour.setHours(nextHour.getHours() + 1);
  nextHour.setMinutes(0, 0, 0);
  const fromTimestamp = nextHour.valueOf() / 1000;
  const toTimestamp = nextHour.setHours(nextHour.getHours() + 1).valueOf() / 1000;
  return (
    <div className="openbsw-panel">
      <LifecycleTag status={'In ontwikkeling'} mode={'long'}/>
      <h4>Agenda van vandaag</h4>
      <div className="rvo-scrollable-content openbsw-panel-scrollable-content">
        <MijnKalenderItems baseUrl={baseUrl}></MijnKalenderItems>
      </div>
      <p className="utrecht-button-group">
        <a
          className="utrecht-button utrecht-button--primary-action utrecht-button--rvo-sm"
          href={'https://files.la-suite.apps.digilab.network/apps/calendar/dayGridMonth/now/new/popover/0/' + fromTimestamp + '/' + toTimestamp}
          target="_blank"
        >
          <span
            className="utrecht-icon rvo-icon rvo-icon-plus rvo-icon--sm rvo-icon--hemelblauw"
            role="img"
            aria-label="Plus"
          ></span>
          Afspraak inplannen
        </a>
        <a
          className="utrecht-button utrecht-button--secondary-action utrecht-button--rvo-sm"
          href="https://files.la-suite.apps.digilab.network/apps/calendar/"
          target="_blank"
        >
          Mijn agenda
        </a>
      </p>
    </div>
  )
}