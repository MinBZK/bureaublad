"use client";
import {
  createContext,
  useCallback,
  useContext,
  useState,
  useEffect,
} from "react";
import api from "@/lib/axios";
import StartLoading from "../../Common/StartLoading";
import { attemptSilentLogin } from "../../../lib/silentLogin";

const AppContext = createContext();

export function AppProvider({ children }) {
  const [appConfig, setAppConfig] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchConfig = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const res = await api.get("/config");
      setAppConfig(res?.data);
    } catch (err) {
      setError(err?.response ?? { status: 0 });
      // If the session is gone, try silent SSO once. If that is not
      // possible, the welcome page offers a manual login button.
      if (err?.response?.status === 401) {
        attemptSilentLogin(
          300,
          window.location.pathname + window.location.search,
        );
      }
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchConfig();
  }, [fetchConfig]);

  return (
    <StartLoading loading={loading}>
      <AppContext.Provider
        value={{ appConfig, error, retryConfig: fetchConfig }}
      >
        {children}
      </AppContext.Provider>
    </StartLoading>
  );
}

export function useAppContext() {
  const ctx = useContext(AppContext);
  if (!ctx) throw new Error("useAppContext must be used within AppProvider");
  return ctx;
}
