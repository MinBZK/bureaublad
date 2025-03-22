FROM --platform=$BUILDPLATFORM node:23-alpine3.21 AS build

WORKDIR /app

COPY package.json package-lock.json next.config.ts tsconfig.json /app/
COPY src /app/src
COPY src/public /app/public

RUN npm ci && npm run build

FROM --platform=$BUILDPLATFORM nginx:1.27.4-alpine

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

VOLUME [ "/usr/share/nginx/html" ]