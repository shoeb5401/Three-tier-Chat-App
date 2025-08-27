# ---------- Build Stage ----------
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm ci --only=production

# Copy app source
COPY . .

# ---------- Runtime Stage ----------
FROM node:18-alpine

WORKDIR /app

# Copy only built app from builder stage
COPY --from=builder /app ./

# Set non-root user for security
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Give appuser ownership of files 
RUN chown -R appuser:appgroup /app
# Switch to non-root user
USER appuser

# Expose app port
EXPOSE 5000

# Run app
CMD ["npm", "start"]
