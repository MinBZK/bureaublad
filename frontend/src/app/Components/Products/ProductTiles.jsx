"use client";

import Link from "next/link";
import { ExportOutlined, StarFilled, StarOutlined } from "@ant-design/icons";
import { useTranslations } from "../../../i18n/TranslationsProvider";
import { appIcon } from "../../Common/appMeta";

function ProductTiles({
  applications = [],
  favoriteApplicationIds = [],
  onToggleFavorite,
}) {
  const t = useTranslations("Products");

  if (applications.length === 0) {
    return <p className="rh-empty">{t("empty")}</p>;
  }

  return (
    <div className="rh-product-grid">
      {applications.map((app) => {
        const Icon = appIcon(app);
        const isFavorite = favoriteApplicationIds.includes(app.id);
        const translatedDescription = t(app.id);
        const description =
          translatedDescription === app.id
            ? t("default")
            : translatedDescription;

        return (
          <div key={app.id} className="rh-product-tile">
            {!app.beta && (
              <button
                aria-label={
                  isFavorite ? t("removeFromFavorites") : t("addToFavorites")
                }
                className={`rh-favorite-button ${isFavorite ? "is-active" : ""}`}
                onClick={() => onToggleFavorite?.(app.id)}
                type="button"
              >
                {isFavorite ? <StarFilled /> : <StarOutlined />}
              </button>
            )}
            <Link
              href={app.url || "#"}
              target="_blank"
              rel="noopener noreferrer"
              className="rh-product-tile-link"
            >
              <span className="rh-product-icon" aria-hidden="true">
                <Icon />
              </span>
              <span className="rh-product-body">
                <span className="rh-product-title-wrap">
                  <span className="rh-product-title">
                    {app.title || app.id}
                  </span>
                  {app.beta && (
                    <span className="rh-product-beta">{t("beta")}</span>
                  )}
                </span>
                <span className="rh-product-desc">{description}</span>
              </span>
              <ExportOutlined className="rh-product-arrow" aria-hidden="true" />
              <span className="rh-sr-only">{t("opensInNewTab")}</span>
            </Link>
          </div>
        );
      })}
    </div>
  );
}

export default ProductTiles;
