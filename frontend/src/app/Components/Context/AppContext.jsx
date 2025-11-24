"use client";
import { createContext, useContext, useState, useEffect } from "react";
import axios from "axios";
import Loading from "../../Common/Loading";
import ErrorResult from "../../Common/ErrorResult";

const AppContext = createContext();

export function AppProvider({ children }) {
  const [items, setitems] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  useEffect(() => {
    setLoading(true);
    const fetchConfig = async () => {
      try {
        const res = await axios.get("/api/v1/config");
        setitems(res?.data);
      } catch (err) {
        setError(err?.response);
      } finally {
        setLoading(false);
      }
    };
    fetchConfig();
  }, []);
  return (
    <Loading loading={loading}>
      {items ? (
        <AppContext.Provider value={{ items, error }}>
          {children}
        </AppContext.Provider>
      ) : error?.status === 401 ? (
        <ErrorResult
          errorStatus="info"
          title="Inloggen"
          subTitle="Meld u aan om toegang te krijgen tot deze applicatie."
          btnTitle={"Inloggen"}
          btnLink={`/api/v1/auth/login`}
        />
      ) : (
        error && (
          <ErrorResult
            errorStatus="404"
            title="404"
            subTitle="Er is iets mis gegaan"
            btnTitle={"Terug naar homepagina"}
            btnLink={`/`}
          />
        )
      )}
    </Loading>
  );
}

export function useAppContext() {
  const ctx = useContext(AppContext);
  if (!ctx) throw new Error("useAppContext must be used within AppProvider");
  return ctx;
}
