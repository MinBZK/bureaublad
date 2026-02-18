"use client";
import { useTranslations } from "../../i18n/TranslationsProvider";
import ErrorResult from "../Common/ErrorResult";

function NotFoundPage() {
  const t = useTranslations("NotFoundPage");
  return (
    <ErrorResult
      errorStatus="500"
      title="500"
      subTitle={t("subTitle")}
      btnTitle={t("backToHome")}
      btnLink={`/`}
    />
  );
}

export default NotFoundPage;
