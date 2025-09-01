# ---------- Stage 1: Build React App ----------
FROM node:18-alpine AS builder
WORKDIR /app

COPY package*.json ./
RUN npm install --legacy-peer-deps

COPY . .
RUN npm run build

# ---------- Stage 2: Nginx Production ----------
FROM nginx:alpine

# Copy build output
COPY --from=builder /app/dist /usr/share/nginx/html

# Fix permissions so Nginx (non-root user) can read files
RUN chmod -R 755 /usr/share/nginx/html

# Copy nginx template instead of conf
COPY nginx.conf /etc/nginx/templates/default.conf.template

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]