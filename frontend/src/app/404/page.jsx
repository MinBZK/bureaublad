"use client";
import ErrorResult from "../Common/ErrorResult";

function NotFoundPage() {
  return (
    <ErrorResult
      errorStatus="404"
      title="404"
      subTitle="Er is iets mis gegaan"
      btnTitle={"Terug naar homepagina"}
      btnLink={`/`}
    />
  );
}

export default NotFoundPage;
