FROM --platform=$BUILDPLATFORM node:22-alpine3.21 AS dev

WORKDIR /app

# Install required build dependencies for sharp and other native modules related to 22-alpine3.21
RUN apk add --no-cache \
  python3 \
  make \
  g++ \
  libc6-compat \
  vips-dev

# Set build arguments
ARG NEXT_PUBLIC_BACKEND_BASE_URL

# Set environment variables for Next.js
ENV NEXT_PUBLIC_BACKEND_BASE_URL=$NEXT_PUBLIC_BACKEND_BASE_URL

COPY package.json package-lock.json next.config.ts tsconfig.json /app/
COPY src /app/src
COPY public /app/public

# --no-audit --no-fund --prefer-offline --progress=false set otherwise will take too long in the dev
RUN npm ci --no-audit --no-fund --prefer-offline --progress=false

CMD ["npm", "run", "dev"]

FROM dev AS build

RUN npm run build

FROM --platform=$BUILDPLATFORM nginx:1.27.4-alpine AS prod

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
