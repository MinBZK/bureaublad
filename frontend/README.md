# Mijn portaal - Frontend

## Getting Started

Make sure you install [bun](https://bun.sh/)

Create a .env folder with configuration for the Keycloak server:

```
NEXT_PUBLIC_KEYCLOAK_URL=https://id.la-suite.apps.digilab.network/
NEXT_PUBLIC_KEYCLOAK_REALM=lasuite
NEXT_PUBLIC_KEYCLOAK_CLIENT=bureaublad-frontend
```

Run the development server:

```bash
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.