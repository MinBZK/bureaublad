"use client";
import { useTranslations } from "../../i18n/TranslationsProvider";
import ErrorResult from "../Common/ErrorResult";

function NotFoundPage() {
  const t = useTranslations("NotFoundPage");
  return (
    <ErrorResult
      errorStatus="404"
      title="404"
      subTitle={t("subTitle")}
      btnTitle={t("backToHome")}
      btnLink={`/`}
    />
  );
}

export default NotFoundPage;
