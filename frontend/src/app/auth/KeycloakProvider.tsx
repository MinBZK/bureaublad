'use client'

import React, { createContext, useContext, useEffect, useState } from 'react';
import { initKeycloak, keycloak, logout } from '@/app/auth/keycloak';

export const KeycloakContext = createContext({
    initialized: false,
    authenticated: false,
    user: {name: "Loading.", email: "Loading."},
    logout: () => {},
});

export const KeycloakProvider = ({ children }) => {
    const [initialized, setInitialized] = useState(false);
    const [authenticated, setAuthenticated] = useState(false);
    const [user, setUser] = useState({name: "Loading...", email: "Loading..."});

    useEffect(() => {
        if (typeof window !== 'undefined') {
            console.log('initKeycloak');
            initKeycloak()
                .then(auth => {
                    console.log(auth);
                    setAuthenticated(auth);
                    if (keycloak && auth) {
                        console.log(keycloak.tokenParsed?.name);
                        setUser({
                            name: keycloak.tokenParsed?.name,
                            email: keycloak.tokenParsed?.email,
                        });
                    }
                    setInitialized(true);
                })
                .catch(err => console.error('Failed to initialize Keycloak', err));
        }
    }, []);

    return (
        <KeycloakContext.Provider value={{ initialized, authenticated, user, logout }}>
            {children}
        </KeycloakContext.Provider>
    );
};

export const useKeycloak = () => useContext(KeycloakContext);