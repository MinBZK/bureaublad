"use client";

import React, { useEffect } from "react";
import { useAppContext } from "../../Context/AppContext";

export default function ThemeLoader() {
  const { items } = useAppContext();
  useEffect(() => {
    if (!items?.theme_css) return;

    // Check if we already added this link (avoid duplicates)
    if (document.querySelector(`link[href="${items.theme_css}"]`)) return;

    // Create a new <link> element for the user’s custom stylesheet
    const link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = items.theme_css;
    link.type = "text/css";
    link.setAttribute("precedence", "default");

    document.head.appendChild(link);

    return () => {
      if (link.parentNode) link.parentNode.removeChild(link);
    };
  }, [items?.theme_css]);

  return null;
}
