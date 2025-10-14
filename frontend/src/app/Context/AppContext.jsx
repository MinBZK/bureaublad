"use client";

import React, { createContext, useContext, useState, useEffect } from "react";
import { baseUrl } from "../Common/pageConfig";

const AppContext = createContext();

export function AppProvider({ children }) {
  const [items, setitems] = useState(null);

  useEffect(() => {
    fetch(baseUrl + "/api/v1/config", {
      method: "GET",
      mode: "cors",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        // Authorization: `Bearer ${keycloak.token}`,
      },
    })
      .then((res) => res.json())
      .then((json) => setitems(json))
      .catch((err) => console.error("Fetch error:", err));
  }, []);

  return (
    <AppContext.Provider value={{ items }}>{children}</AppContext.Provider>
  );
}

export function useAppContext() {
  const ctx = useContext(AppContext);
  if (!ctx) throw new Error("useAppContext must be used within AppProvider");
  return ctx;
}
