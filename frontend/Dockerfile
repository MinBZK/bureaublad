FROM --platform=$BUILDPLATFORM node:23-alpine3.21 AS build

WORKDIR /app

# Set build arguments
ARG NEXT_PUBLIC_KEYCLOAK_URL
ARG NEXT_PUBLIC_KEYCLOAK_REALM
ARG NEXT_PUBLIC_KEYCLOAK_CLIENT
ARG NEXT_PUBLIC_BACKEND_BASE_URL

# Set environment variables for Next.js
ENV NEXT_PUBLIC_KEYCLOAK_URL=$NEXT_PUBLIC_KEYCLOAK_URL
ENV NEXT_PUBLIC_KEYCLOAK_REALM=$NEXT_PUBLIC_KEYCLOAK_REALM
ENV NEXT_PUBLIC_KEYCLOAK_CLIENT=$NEXT_PUBLIC_KEYCLOAK_CLIENT
ENV NEXT_PUBLIC_BACKEND_BASE_URL=$NEXT_PUBLIC_BACKEND_BASE_URL

COPY package.json package-lock.json next.config.ts tsconfig.json /app/
COPY src /app/src
COPY src/public /app/public

RUN npm ci && npm run build

FROM --platform=$BUILDPLATFORM nginx:1.27.4-alpine

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]