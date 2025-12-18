import { useState, useCallback, useMemo } from "react";
import api from '@/lib/axios';
import { useAutoRefresh } from "./useAutoRefresh";

export function useFetchWithRefresh(url, params = {}) {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Build URL with query parameters
  const fullUrl = useMemo(() => {
    if (!params || Object.keys(params).length === 0) {
      return url;
    }

    const queryString = Object.entries(params)
      .filter(
        ([, value]) => value !== undefined && value !== null && value !== "",
      )
      .map(([key, value]) => `${key}=${encodeURIComponent(value)}`)
      .join("&");

    return queryString ? `${url}?${queryString}` : url;
  }, [url, params]);

  // Fetch function
  const fetchData = useCallback(
    async (isAutoRefresh = false) => {
      setLoading(true);
      try {
        const res = await api.get(fullUrl);
        setData(res.data);
        setError("");
      } catch (err) {
        // Only set error if it's NOT an auto-refresh
        if (!isAutoRefresh) {
          setError(err.message);
        }
      } finally {
        setLoading(false);
      }
    },
    [fullUrl],
  );

  // Auto-refresh fetch that doesn't set errors
  const autoRefreshFetch = useCallback(() => {
    fetchData(true);
  }, [fetchData]);

  // Auto-refresh every specified interval
  useAutoRefresh(autoRefreshFetch, 30000);

  return {
    data,
    loading,
    error,
    onRefresh: fetchData,
  };
}
