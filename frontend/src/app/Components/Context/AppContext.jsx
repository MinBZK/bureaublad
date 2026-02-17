"use client";
import { createContext, useContext, useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import api from "@/lib/axios";
import { useSearchParams } from "next/navigation";
import StartLoading from "../../Common/StartLoading";

const AppContext = createContext();

export function AppProvider({ children }) {
  const [appConfig, setAppConfig] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const router = useRouter();
  const searchParams = useSearchParams();

  useEffect(() => {
    const fetchConfig = async () => {
      try {
        const res = await api.get("/config");
        setAppConfig(res?.data);
      } catch (err) {
        setError(err?.response);
        // Redirect based on error
        if (err?.response?.status === 401) {
          const params = searchParams.toString();
          const redirectUrl = params ? `/login?${params}` : "/login";
          router.push(redirectUrl);
        } else if (err?.response?.status === 500) {
          router.push("/500");
        } else {
          router.push("/404");
        }
      } finally {
        setLoading(false);
      }
    };
    fetchConfig();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <StartLoading loading={loading}>
      <AppContext.Provider value={{ appConfig, error }}>
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
