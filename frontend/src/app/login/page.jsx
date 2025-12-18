"use client";
import ErrorResult from "../Common/ErrorResult";
import { useSearchParams } from "next/navigation";
import { useTranslations } from "../../i18n/TranslationsProvider";

function Page() {
  const searchParams = useSearchParams();
  const errorParam = searchParams.get("error");

  const isAuthError = errorParam === "authentication_failed";
  const t = useTranslations("LoginPage");
  return (
    <ErrorResult
      errorStatus={isAuthError ? "error" : "info"}
      title={isAuthError ? t("failedTitle") : t("loginButton")}
      subTitle={isAuthError ? t("failedMessage") : t("loginMessage")}
      btnTitle={t("loginButton")}
      btnLink={`/api/v1/auth/login`}
    />
  );
}

export default Page;
