"use client";

import React, { createContext, useContext, useState, useEffect } from "react";
import { baseUrl } from "../Common/pageConfig";
import axios from "axios";
import Loading from "../Common/Loading";
import { useRouter } from "next/navigation";
// axios.defaults.withCredentials = true;

const AppContext = createContext();

export function AppProvider({ children }) {
  const [items, setitems] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const router = useRouter();
  useEffect(() => {
    setLoading(true);
    const fetchConfig = async () => {
      try {
        const res = await axios.get(baseUrl + "/api/v1/config");
        setitems(res?.data);
      } catch (err) {
        if (err?.response?.state === 401) {
          router.push("/login");
        }
        setError(err);
      } finally {
        setLoading(false);
      }
    };
    fetchConfig();
  }, []);

  return (
    <Loading loading={loading}>
      <AppContext.Provider value={{ items, error }}>
        {children}
      </AppContext.Provider>
    </Loading>
  );
}

export function useAppContext() {
  const ctx = useContext(AppContext);
  if (!ctx) throw new Error("useAppContext must be used within AppProvider");
  return ctx;
}
