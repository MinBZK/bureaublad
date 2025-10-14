"use client";

import React, { createContext, useContext, useEffect, useState } from "react";
import { initKeycloak, keycloak, logout } from "./keycloak";

export const KeycloakContext = createContext({
  initialized: false,
  authenticated: false,
  user: { name: "Loading.", email: "Loading." },
  logout: () => {},
});

export const KeycloakProvider = ({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) => {
  const [initialized, setInitialized] = useState(false);
  const [authenticated, setAuthenticated] = useState(false);
  const [user, setUser] = useState({ name: "Loading...", email: "Loading..." });

  useEffect(() => {
    if (typeof window !== "undefined") {
      initKeycloak()
        .then((auth) => {
          setAuthenticated(auth);
          if (keycloak && auth) {
            setUser({
              name: keycloak.tokenParsed?.name,
              email: keycloak.tokenParsed?.email,
            });
          }
          setInitialized(true);

          // Set up token refresh
          const refreshInterval = setInterval(() => {
            if (keycloak && keycloak.token) {
              keycloak
                .updateToken(30)
                .then((refreshed) => {
                  if (refreshed) {
                    setUser({
                      name: keycloak.tokenParsed?.name,
                      email: keycloak.tokenParsed?.email,
                    });
                  }
                })
                .catch((err) => {
                  console.error("Failed to refresh token", err);
                  logout();
                });
            }
          }, 60000);

          return () => clearInterval(refreshInterval);
        })
        .catch((err) => console.error("Failed to initialize Keycloak", err));
    }
  }, []);

  return (
    <KeycloakContext.Provider
      value={{ initialized, authenticated, user, logout }}
    >
      {children}
    </KeycloakContext.Provider>
  );
};

export const useKeycloak = () => useContext(KeycloakContext);
