'use client'

import React, {useContext, useEffect, useRef, useState} from "react";
import {KeycloakContext} from "@/app/auth/KeycloakProvider";
import {keycloak} from "@/app/auth/keycloak";
import FileTypeIcon from "@/app/components/fileTypeIcon";

interface SearchResultsProps {
  term?: string
}

function shortenUrl(url: string, maxLength: number) {
  const schemeIndex = url.indexOf('://');
  if (schemeIndex >= 0) {
    url = url.slice(schemeIndex + 3);
  }
  if (url.length > maxLength) {
    const keep = (maxLength / 2) - 1;
    return url.slice(0, keep) + '...' + url.slice(url.length - keep);
  }
  return url;
}

function SearchResults({term}: SearchResultsProps) {
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [items, setItems] = useState([]);

  const keycloakContext = useContext(KeycloakContext);

  useEffect(() => {
    if (term && keycloakContext.authenticated) {
      fetch("http://localhost:8000/v1/nextcloud/search?term=" + term, {
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
  }, [keycloakContext, term])

  if (!term) {
    return (
      <>
        Type een zoekterm
      </>
    );
  } else if (!isLoaded) {
    return (
      <div className="rvo-loader">
        <span className="rvo-loader__icon rvo-loader__icon--animated">
          <span
            className="utrecht-icon rvo-icon rvo-icon-pijlen-in-cirkel-om-document rvo-icon--2xl rvo-icon--grijs-700"
            role="img"
            aria-label="Pijlen in cirkel om document"
          ></span>
        </span>
        Zoeken naar: {term}
      </div>
    );
  } else if (error) {
    return (
      <>
        Foutmelding: {error.message}
      </>
    );
  } else if (items.length === 0) {
    return (
      <>
        Geen resultaten gevonden
      </>
    )
  } else {
    return (
      <>
        <h3 className="utrecht-heading-3">Zoekresultaten</h3>
        <div className="rvo-scrollable-content openbsw-search-scrollable-content">
          <div className="rvo-layout-column rvo-layout-gap--0">
            {items.map(item => (
              <a href={item.url} key={item.url} className="rvo-link rvo-link--with-icon rvo-link--no-underline rvo-link--zwart rvo-link--normal" target="_blank">
                <div>
                  <div
                    className="rvo-layout-row rvo-layout-align-items-start rvo-layout-align-content-start rvo-layout-justify-items-start rvo-layout-justify-content-start rvo-layout-gap--0">
                    <div className="rvo-margin--sm">
                      <FileTypeIcon fileName={item.name} />
                    </div>
                    <div>
                      <span className="openbsw-document-titel">{item.name}</span><br/>
                      <span className="openbsw-search-result--date">{shortenUrl(item.url, 60)}</span>
                    </div>
                  </div>
                </div>
              </a>
            ))}
          </div>
        </div>
      </>
    );
  }
}

export default function Search() {
  const [query, setQuery] = useState("");
  const [isVisible, setIsVisible] = useState(false); // Manages the visibility state of the popover
  const popoverRef = useRef(null); // Reference to the popover element
  const triggerRef = useRef(null); // Reference to the button element that triggers the popover
  const inputRef = useRef(null);

  const handleOnClick = () => {
    setIsVisible(true);
    submitQuery();
  };

  function handleKeyUp(e: React.KeyboardEvent<HTMLInputElement>) {
    if (e.key === "Enter") {
      handleOnClick();
    }
  }

  function submitQuery() {
    setQuery(inputRef.current.value);
  }

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        popoverRef.current && !popoverRef.current.contains(event.target) &&
        triggerRef.current && !triggerRef.current.contains(event.target) &&
        inputRef.current && !inputRef.current.contains(event.target)
      ) {
        setIsVisible(false); // Close the popover if clicked outside
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  return (
    <div className="rvo-layout-row rvo-layout-gap--0 rvo-margin-inline-start--2xl openbsw-search-container">
      <input id="field" placeholder="Zoek collega's, dossiers of vraag hulp van je persoonlijke assistent"
             type="text" className="utrecht-textbox utrecht-textbox--html-input openbsw-textbox--menu"
             dir="auto" defaultValue=""
             onKeyUp={handleKeyUp}
             ref={inputRef}
      />
      <button
        ref={triggerRef}
        onClick={handleOnClick}
        className="utrecht-button utrecht-button--primary-action utrecht-button--rvo-md  popover-trigger"
        aria-haspopup="true"
        aria-expanded={isVisible}
        aria-controls="popover-content"
      >
        <span className="utrecht-icon rvo-icon rvo-icon-zoek rvo-icon--md rvo-icon--hemelblauw" role="img"
              aria-label="Vergrootglas"></span>
      </button>
      {isVisible && (
        <div
          id="popover-content"
          ref={popoverRef}
          className="rvo-card rvo-card--outline rvo-card--padding-sm openbsw-search-popover-content"
          role="dialog"
          aria-modal="true"
        >
          <SearchResults term={query}></SearchResults>
        </div>
      )}
    </div>
  )
}
