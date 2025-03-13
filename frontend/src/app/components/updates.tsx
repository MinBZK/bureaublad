'use client'

import {useEffect, useState} from "react";

function UpdatesItems() {
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [items, setItems] = useState([]);

  useEffect(() => {
    fetch("https://developer.overheid.nl/blog/rss.xml", {
      method: "GET",
      headers: {
        "Accept": "application/rss+xml",
      }
    })
      .then(res => res.text())
      .then(
        (result) => {
          setIsLoaded(true);
          const parser = new DOMParser();
          const xmlDoc = parser.parseFromString(result, 'text/xml');
          const items = xmlDoc.getElementsByTagName('item');
          const feedItems = [];

          const dateOptions: DateTimeFormatOptions = {
            year: "numeric",
            month: "short",
            day: "numeric",
          };

          for (let i = 0; i < items.length; i++) {
            const title = items[i].getElementsByTagName('title')[0].textContent;
            const link = items[i].getElementsByTagName('link')[0].textContent;
            const guid = items[i].getElementsByTagName('guid')[0].textContent;
            const pubDate = new Date(items[i].getElementsByTagName('pubDate')[0]?.textContent).toLocaleDateString("nl-NL", dateOptions);
            const hostname = new URL(link).hostname;
            feedItems.push({ title, link, guid, hostname, pubDate });
          }
          setItems(feedItems);
        },
        // Note: it's important to handle errors here
        // instead of a catch() block so that we don't swallow
        // exceptions from actual bugs in components.
        (error) => {
          setIsLoaded(true);
          setError(error);
        }
      )
  }, [])

  if (error) {
    return <div>Error: {error.message}</div>;
  } else if (!isLoaded) {
    return <div>Loading...</div>;
  } else {
    return (
      <div className="rvo-layout-column rvo-layout-gap--0">
        {items.map(item => (
          <div key={item.guid} className="openbsw-updates-item">
            <a href={item.link} className="rvo-link rvo-link--with-icon rvo-link--no-underline rvo-link--zwart rvo-link--normal" target="_blank">
              <div>
                <div
                  className="rvo-layout-row rvo-layout-align-items-start rvo-layout-align-content-start rvo-layout-justify-items-start rvo-layout-justify-content-start rvo-layout-gap--0">
                  <div>
                    <span className="openbsw-document-titel">{item.title}</span><br/>
                    <span className="openbsw-document-categorie">{item.hostname} </span>
                    <span className="openbsw-document-datum"> {item.pubDate}</span>
                  </div>
                </div>
              </div>
            </a>
          </div>
        ))}
      </div>
    );
  }
}

export default function Updates() {
  return (
    <div className="openbsw-panel">
      <h4>Updates</h4>
      <div className="rvo-scrollable-content openbsw-panel-scrollable-content">
        <UpdatesItems></UpdatesItems>
      </div>
      <p>
        <a
          className="rvo-link rvo-link--with-icon rvo-link--hemelblauw rvo-link--normal"
          href="#"
        >
          Meer updates
        </a>
      </p>
    </div>
  )
}