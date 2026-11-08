"use client";
import { useEffect, useState } from "react";
import { useAppContext } from "./Components/Context/AppContext";
import { useTranslations } from "../i18n/TranslationsProvider";
import ProductTiles from "./Components/Products/ProductTiles";

const FAVORITE_APPLICATIONS_STORAGE_KEY = "favorite-applications";

function getStoredStringArray(key) {
  if (typeof window === "undefined") {
    return [];
  }
  const value = localStorage.getItem(key);
  if (!value) {
    return [];
  }
  try {
    const parsed = JSON.parse(value);
    if (Array.isArray(parsed)) {
      return parsed.filter((item) => typeof item === "string");
    }
  } catch {
    return [];
  }
  return [];
}

export default function Home() {
  const { appConfig } = useAppContext();
  const tHome = useTranslations("HomePage");
  const [favoriteApplicationIds, setFavoriteApplicationIds] = useState(() =>
    getStoredStringArray(FAVORITE_APPLICATIONS_STORAGE_KEY),
  );

  useEffect(() => {
    localStorage.setItem(
      FAVORITE_APPLICATIONS_STORAGE_KEY,
      JSON.stringify(favoriteApplicationIds),
    );
  }, [favoriteApplicationIds]);

  const applications =
    appConfig?.applications?.filter((app) => app?.url && app?.title) || [];
  const sortedApplications = [...applications].sort((a, b) => {
    const aIsBeta = Boolean(a?.beta);
    const bIsBeta = Boolean(b?.beta);
    if (aIsBeta !== bIsBeta) {
      return aIsBeta ? 1 : -1;
    }
    const aLabel = a?.title || a?.id || "";
    const bLabel = b?.title || b?.id || "";
    return aLabel.localeCompare(bLabel, undefined, { sensitivity: "base" });
  });
  const visibleApplications = sortedApplications;
  const favoriteApplications = visibleApplications.filter(
    (app) => !app?.beta && favoriteApplicationIds.includes(app.id),
  );
  const regularApplications = visibleApplications.filter(
    (app) => app?.beta || !favoriteApplicationIds.includes(app.id),
  );

  const handleToggleFavorite = (appId) => {
    setFavoriteApplicationIds((currentIds) => {
      if (currentIds.includes(appId)) {
        return currentIds.filter((id) => id !== appId);
      }
      return [...currentIds, appId];
    });
  };
  return (
    <>
      <section className="rh-hero">
        <div className="rh-hero-inner">
          <h1 className="rh-hero-title">{tHome("heading")}</h1>
          <p className="rh-hero-text">{tHome("intro")}</p>
        </div>
      </section>

      <div className="rh-page">
        <section className="rh-section" aria-labelledby="products-heading">
          {favoriteApplications.length > 0 && (
            <div className="rh-apps-group">
              <div className="rh-section-header">
                <h2>{tHome("favoritesHeading")}</h2>
                <p>{tHome("favoritesIntro")}</p>
              </div>
              <ProductTiles
                applications={favoriteApplications}
                favoriteApplicationIds={favoriteApplicationIds}
                onToggleFavorite={handleToggleFavorite}
              />
            </div>
          )}

          <div className="rh-apps-group">
            <div className="rh-section-header">
              <h2 id="products-heading">{tHome("products")}</h2>
              <p>{tHome("productsIntro")}</p>
            </div>
            <ProductTiles
              applications={regularApplications}
              favoriteApplicationIds={favoriteApplicationIds}
              onToggleFavorite={handleToggleFavorite}
            />
          </div>
        </section>
      </div>
    </>
  );
}
