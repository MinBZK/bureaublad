"use client";

import React, { createContext, useContext, useState, useEffect } from "react";
import axios from "axios";
import Loading from "../../Common/Loading";
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
        const res = await axios.get("/api/v1/config");
        setitems(res?.data);
      } catch (err) {
        if (err?.response?.status === 401) {
          console.log(err?.response?.status);
          router.push("/login");
        } else {
          router.push("/not-found");
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
