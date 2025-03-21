'use client'

import React, {RefObject, useContext, useEffect, useRef, useState} from "react";
import {KeycloakContext} from "../auth/KeycloakProvider";
import {keycloak} from "../auth/keycloak";
import FileTypeIcon from "./fileTypeIcon";
import Markdown from "react-markdown";

interface SearchResultsProps {
  term?: string,
  baseUrl?: unknown
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

interface SearchResultsItemData {
  url: string,
  name: string,
}

interface SearchResultsItemsProps {
  items: SearchResultsItemData[]
}

function SearchResultsItems({items}: SearchResultsItemsProps) {
  if (items.length === 0) {
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
              <a href={item.url} key={item.url}
                 className="rvo-link rvo-link--with-icon rvo-link--no-underline rvo-link--zwart rvo-link--normal"
                 target="_blank">
                <div>
                  <div
                    className="rvo-layout-row rvo-layout-align-items-start rvo-layout-align-content-start rvo-layout-justify-items-start rvo-layout-justify-content-start rvo-layout-gap--0">
                    <div className="rvo-margin--sm">
                      <FileTypeIcon fileName={item.name}/>
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

interface SearchResultsAIProps {
  value: string
}

function SearchResultsAI({value}: SearchResultsAIProps) {
  return (
    <div className="rvo-scrollable-content openbsw-search-scrollable-content">
      <Markdown>{value}</Markdown>
    </div>
  );
}

function SearchResults({term, baseUrl}: SearchResultsProps) {
  const [error, setError] = useState(new Error());
  const [isLoaded, setIsLoaded] = useState(false);
  const [items, setItems] = useState([]);
  const [aiResult, setAiResult] = useState('');
  const [isSearchQuery, setIsSearchQuery] = useState(false);
  const [storedTerm, setStoredTerm] = useState('');

  const keycloakContext = useContext(KeycloakContext);

  useEffect(() => {
    if (term && (term != storedTerm) && keycloakContext.authenticated) {
      setStoredTerm(term);
      const newIsSearchQuery = term.split(' ').length < 4;
      setIsSearchQuery(newIsSearchQuery);
      if (newIsSearchQuery) {
        fetch(baseUrl + "/v1/nextcloud/search?term=" + term, {
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
      } else {
        fetch(baseUrl + "/v1/ai/chat/completions", {
          method: "POST",
          mode: "cors",
          headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": `Bearer ${keycloak.token}`,
          },
          body: JSON.stringify({prompt: term})
        })
          .then(res => res.json())
          .then(
            (result) => {
              setIsLoaded(true);
              if (result.detail) {
                setError(result.detail)
              } else {
                setAiResult(result);
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
    }
  }, [keycloakContext, term, storedTerm, baseUrl]);

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
  } else if (error.message) {
    return (
      <>
        Foutmelding: {error.message}
      </>
    );
  } else if (isSearchQuery) {
    return (
      <SearchResultsItems items={items}></SearchResultsItems>
    );
  } else {
    console.log(aiResult);
    return (
      <SearchResultsAI value={aiResult}></SearchResultsAI>
    )
  }
}

interface SearchProps {
  baseUrl: string
}

export default function Search({baseUrl}: SearchProps) {
  const [query, setQuery] = useState("");
  const [isVisible, setIsVisible] = useState(false); // Manages the visibility state of the popover
  const popoverRef: RefObject<HTMLDivElement | null> = useRef(null); // Reference to the popover element
  const triggerRef: RefObject<HTMLButtonElement | null> = useRef(null); // Reference to the button element that triggers the popover
  const inputRef: RefObject<HTMLInputElement | null> = useRef(null);

  const handleOnClick = () => {
    setIsVisible(true);
    if (inputRef.current) {
      setQuery(inputRef.current.value);
    }
  };

  function handleKeyUp(e: React.KeyboardEvent<HTMLInputElement>) {
    if (e.key === "Enter") {
      handleOnClick();
    }
  }

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        popoverRef.current && !popoverRef.current.contains(event.target as Node) &&
        triggerRef.current && !triggerRef.current.contains(event.target as Node) &&
        inputRef.current && !inputRef.current.contains(event.target as Node)
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
          <SearchResults baseUrl={baseUrl} term={query}></SearchResults>
        </div>
      )}
    </div>
  )
}
