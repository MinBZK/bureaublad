"use client";
import ErrorResult from "../Common/ErrorResult";
import { useSearchParams } from "next/navigation";

function Page() {
  const searchParams = useSearchParams();
  const errorParam = searchParams.get("error");

  const isAuthError = errorParam === "authentication_failed";

  return (
    <ErrorResult
      errorStatus={isAuthError ? "error" : "info"}
      title={isAuthError ? "Inloggen mislukt" : "Inloggen"}
      subTitle={
        isAuthError
          ? "Authenticatie is mislukt. Probeer het opnieuw."
          : "Meld u aan om toegang te krijgen tot deze applicatie."
      }
      btnTitle={"Inloggen"}
      btnLink={`/api/v1/auth/login`}
    />
  );
}

export default Page;
