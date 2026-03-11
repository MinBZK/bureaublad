"use client";
import { useEffect } from "react";
import ErrorResult from "../Common/ErrorResult";
import { useSearchParams } from "next/navigation";
import { useTranslations } from "../../i18n/TranslationsProvider";
import { attemptSilentLogin } from "@/lib/silentLogin";
import { useRouter } from "next/navigation";

function Page() {
  const searchParams = useSearchParams();
  const errorParam = searchParams.get("error");
  const router = useRouter();

  const isAuthError = errorParam === "authentication_failed";
  const t = useTranslations("LoginPage");

  useEffect(() => {
    const tryLogin = async () => {
      const success = await attemptSilentLogin();
      if (success) {
        // Auth succeeded, redirect or refresh app state
        router.push("/");
      }
    };

    tryLogin();
    const timer = setInterval(tryLogin, 30_000);

    return () => clearInterval(timer);
  }, [router]);

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
