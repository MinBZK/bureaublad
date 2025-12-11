import { useEffect, useRef } from "react";

export function useAutoRefresh(fetchFunction, interval = 300000000) {
  // Store refs for cleanup
  const timeoutIdRef = useRef(null);
  const intervalIdRef = useRef(null);
  const initialDelayRef = useRef(null);

  useEffect(() => {
    // Generate random delay only once, on first effect run
    if (initialDelayRef.current === null) {
      initialDelayRef.current = Math.floor(Math.random() * interval);
    }

    // Fetch immediately on mount or when dependencies change
    fetchFunction();

    // Set up the first delayed interval to stagger API calls
    timeoutIdRef.current = setTimeout(() => {
      // After the random delay, start the regular interval
      fetchFunction();

      intervalIdRef.current = setInterval(() => {
        fetchFunction();
      }, interval);
    }, initialDelayRef.current);

    // Cleanup: clear both timeout and interval when component unmounts or dependencies change
    return () => {
      if (timeoutIdRef.current) {
        clearTimeout(timeoutIdRef.current);
      }
      if (intervalIdRef.current) {
        clearInterval(intervalIdRef.current);
      }
    };
  }, [fetchFunction, interval]);
}
