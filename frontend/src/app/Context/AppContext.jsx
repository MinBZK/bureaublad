"use client";

import React, { createContext, useContext, useState, useEffect } from "react";
import { baseUrl } from "../Common/pageConfig";
import axios from "axios";
import { Button, Flex, Result, Spin } from "antd";
import HeaderLayout from "../Components/Layout/Components/HeaderLayout";
import Loading from "../Common/Loading";
// axios.defaults.withCredentials = true;

const AppContext = createContext();

export function AppProvider({ children }) {
  const [items, setitems] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  useEffect(() => {
    setLoading(true);
    const fetchConfig = async () => {
      try {
        const res = await axios.get(baseUrl + "/api/v1/config");
        console.log(res)
        setitems(res);
      } catch (err) {
        console.log(err)
        setError(err);
      } finally {
        setLoading(false);
      }
    };
    fetchConfig();
  }, []);

  return (
    <Loading loading={loading}>
      {error?.response?.status === 401 ? (
        <React.Fragment>
          <HeaderLayout isProfile={false} />
          <Result
            status="403"
            title="403"
            subTitle="Helaas, u bent niet bevoegd om deze pagina te bezoeken."
            extra={
              <Button
                type="primary"
                href={`${baseUrl}/api/v1/auth/login`}
              >
                Inloggen
              </Button>
            }
          />
        </React.Fragment>
      ) : (
        items && (
          <AppContext.Provider value={{ items }}>
            {children}
          </AppContext.Provider>
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
