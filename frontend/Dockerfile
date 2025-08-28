#  Build React App 
FROM node:18-alpine AS builder

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install --legacy-peer-deps

# Copy all source files 
COPY . .

# EXPOSE the PORT
EXPOSE 5173

# Run the Application

CMD ["npm", "start"]


