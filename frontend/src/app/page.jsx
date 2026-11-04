"use client";
import { useAppContext } from "./Components/Context/AppContext";
import { useTranslations } from "../i18n/TranslationsProvider";
import ProductTiles from "./Components/Products/ProductTiles";

export default function Home() {
  const { appConfig } = useAppContext();
  const tHome = useTranslations("HomePage");

  const applications =
    appConfig?.applications?.filter(
      (app) => app?.enabled && app?.url && app?.title,
    ) || [];

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
          <div className="rh-section-header">
            <h2 id="products-heading">{tHome("products")}</h2>
            <p>{tHome("productsIntro")}</p>
          </div>
          <ProductTiles applications={applications} />
        </section>
      </div>
    </>
  );
}
