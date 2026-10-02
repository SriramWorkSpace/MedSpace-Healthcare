# --- dev: Vite with HMR (used by docker-compose.yml) -------------------------
FROM node:22-alpine AS dev
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

# --- build: static production bundle -----------------------------------------
FROM dev AS build
RUN npm run build

# --- prod: nginx serves the SPA and reverse-proxies /api (same-origin cookies) --
FROM nginx:1.27-alpine AS prod
ENV API_UPSTREAM=http://api:8000
COPY deploy/nginx.conf.template /etc/nginx/templates/default.conf.template
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
