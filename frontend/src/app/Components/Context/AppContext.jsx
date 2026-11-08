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
    try {
      const res = await api.get("/config");
      setAppConfig(res?.data);
      setError(null);
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

  const retryConfig = useCallback(() => {
    setLoading(true);
    setError(null);
    fetchConfig();
  }, [fetchConfig]);

  useEffect(() => {
    // Fetch the application config once on mount.
    // eslint-disable-next-line react-hooks/set-state-in-effect
    fetchConfig();
  }, [fetchConfig]);

  return (
    <StartLoading loading={loading}>
      <AppContext.Provider value={{ appConfig, error, retryConfig }}>
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
