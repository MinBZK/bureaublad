import { useState, useCallback, useMemo } from "react";
import axios from "axios";
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
  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      const res = await axios.get(fullUrl);
      setData(res.data);
      setError("");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [fullUrl]);

  // Auto-refresh every specified interval
  useAutoRefresh(fetchData, 30000);

  return {
    data,
    loading,
    error,
    onRefresh: fetchData,
  };
}
