import Keycloak from 'keycloak-js';

let keycloak: Keycloak;

if (typeof window !== 'undefined') {
    keycloak = new Keycloak({
        url: process.env.NEXT_PUBLIC_KEYCLOAK_URL,
        realm: process.env.NEXT_PUBLIC_KEYCLOAK_REALM,
        clientId: process.env.NEXT_PUBLIC_KEYCLOAK_CLIENT,
    });
}

let isInitialized = false;

export const initKeycloak = async () => {
    if (!isInitialized && keycloak) {
        isInitialized = true;
        try {
            return await keycloak
              .init({onLoad: 'login-required', checkLoginIframe: false});
        } catch (err) {
            isInitialized = false;
            console.error('Failed to initialize Keycloak', err);
            throw err;
        }
    }
    return Promise.resolve(keycloak?.authenticated ?? false);
};

export const logout = () => {
    if (keycloak) {
        keycloak.logout();
    }
};

export const getToken = async () => {
    if (keycloak) {
        if (keycloak.isTokenExpired()) {
            try {
                await keycloak.updateToken(30);
            } catch (error) {
                console.error('Failed to refresh the token', error);
                keycloak.logout();
                return null;
            }
        }
        return keycloak.token ?? null;
    }
    return null;
};

export { keycloak };
