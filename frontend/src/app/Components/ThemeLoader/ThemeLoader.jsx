"use client";
import { useEffect } from "react";
import { useAppContext } from "../Context/AppContext";

export default function ThemeLoader() {
  const { appConfig } = useAppContext();
  useEffect(() => {
    if (!appConfig?.theme_css) return;

    // Check if we already added this link (avoid duplicates)
    if (document.querySelector(`link[href="${appConfig.theme_css}"]`)) return;

    // Create a new <link> element for the user's custom stylesheet
    const link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = appConfig.theme_css;
    link.type = "text/css";
    link.setAttribute("precedence", "default");

    document.head.appendChild(link);

    return () => {
      if (link.parentNode) link.parentNode.removeChild(link);
    };
  }, [appConfig?.theme_css]);

  return null;
}
