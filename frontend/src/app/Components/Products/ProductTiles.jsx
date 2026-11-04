"use client";

import Link from "next/link";
import { ExportOutlined } from "@ant-design/icons";
import { useTranslations } from "../../../i18n/TranslationsProvider";
import { appIcon } from "../../Common/appMeta";

function ProductTiles({ applications = [] }) {
  const t = useTranslations("Products");

  if (applications.length === 0) {
    return <p className="rh-empty">{t("empty")}</p>;
  }

  return (
    <div className="rh-product-grid">
      {applications.map((app) => {
        const Icon = appIcon(app);
        const translatedDescription = t(app.id);
        const description =
          translatedDescription === app.id
            ? t("default")
            : translatedDescription;

        return (
          <Link
            key={app.id}
            href={app.url || "#"}
            target="_blank"
            rel="noopener noreferrer"
            className="rh-product-tile"
          >
            <span className="rh-product-icon" aria-hidden="true">
              <Icon />
            </span>
            <span className="rh-product-body">
              <span className="rh-product-title">{app.title || app.id}</span>
              <span className="rh-product-desc">{description}</span>
            </span>
            <ExportOutlined className="rh-product-arrow" aria-hidden="true" />
            <span className="rh-sr-only">{t("opensInNewTab")}</span>
          </Link>
        );
      })}
    </div>
  );
}

export default ProductTiles;
