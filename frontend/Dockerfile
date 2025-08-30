# Build React App
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install --legacy-peer-deps
COPY . .
RUN npm run build

# Production Nginx image
FROM nginx:alpine

# Copy React build
COPY --from=builder /app/dist /usr/share/nginx/html


# Copy nginx template instead of conf
COPY nginx.conf /etc/nginx/templates/default.conf.template


# Expose port
EXPOSE 80
