# 💬 Real-Time Chat Application

A modern, scalable real-time chat application built with React, Node.js, and MongoDB, featuring complete containerization with Docker and production-ready Kubernetes deployment with monitoring.


## 🚀 Features

- **Real-time messaging** with Socket.io
- **User authentication** with JWT tokens
- **File uploads** with Cloudinary integration
- **Responsive design** with Tailwind CSS
- **Containerized** with Docker
- **Kubernetes-ready** with full manifest files
- **Monitoring** with Prometheus and Grafana
- **SSL/TLS** security with self-signed certificates
- **Auto-scaling** with Horizontal Pod Autoscaler (HPA)

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Database      │
│   (React)       │◄──►│   (Node.js)     │◄──►│   (MongoDB)     │
│   Port: 80      │    │   Port: 5001    │    │   Port: 27017   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Ingress       │
                    │   (Nginx)       │
                    └─────────────────┘
```

## 📋 Prerequisites

- Docker and Docker Compose
- Kubernetes cluster (minikube, kind, or cloud provider)
- kubectl configured
- Helm 3.x
- Node.js 18+ (for local development)

## 🐳 Step 1: Docker Configuration

### Frontend Dockerfile
```dockerfile
# Multi-stage build for optimized production image
FROM node:18-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Backend Dockerfile
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 5001
CMD ["npm", "start"]
```

## 🐳 Step 2: Local Development with Docker Compose

### docker-compose.yml
```yaml
version: '3.8'
services:
  mongodb:
    image: mongo:7
    container_name: chat-mongodb
    restart: unless-stopped
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: password123
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
    networks:
      - chat-network

  backend:
    build: ./backend
    container_name: chat-backend
    restart: unless-stopped
    ports:
      - "5001:5001"
    environment:
      - NODE_ENV=development
      - MONGODB_URI=mongodb://admin:password123@mongodb:27017/chat-app?authSource=admin
      - JWT_SECRET=your-super-secret-jwt-key
      - CLOUDINARY_CLOUD_NAME=your-cloud-name
      - CLOUDINARY_API_KEY=your-api-key
      - CLOUDINARY_API_SECRET=your-api-secret
    depends_on:
      - mongodb
    networks:
      - chat-network

  frontend:
    build: ./frontend
    container_name: chat-frontend
    restart: unless-stopped
    ports:
      - "80:80"
    depends_on:
      - backend
    networks:
      - chat-network

volumes:
  mongodb_data:

networks:
  chat-network:
    driver: bridge
```

### Running Locally
```bash
# Clone the repository
git clone <your-repo-url>
cd chat-application

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 📦 Step 3: Docker Hub Deployment

### Build and Push Images
```bash
# Build and tag images
docker build -t yourusername/chat-frontend:latest ./frontend
docker build -t yourusername/chat-backend:latest ./backend

# Push to Docker Hub
docker push yourusername/chat-frontend:latest
docker push yourusername/chat-backend:latest

# Tag specific versions
docker tag yourusername/chat-frontend:latest yourusername/chat-frontend:v1.0.0
docker tag yourusername/chat-backend:latest yourusername/chat-backend:v1.0.0

docker push yourusername/chat-frontend:v1.0.0
docker push yourusername/chat-backend:v1.0.0
```

## ☸️ Step 4: Kubernetes Deployment

### Create Namespace and Secrets
```bash
# Apply namespace
kubectl apply -f k8s/namespace.yml

# Create secrets (update with your values)
kubectl apply -f k8s/secret.yml
```

### namespace.yml
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: chat-app
  labels:
    name: chat-app
    purpose: real-time-chat-application
```

### secret.yml
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: chat-app-secrets
  namespace: chat-app
type: Opaque
stringData:
  mongodb-username: admin
  mongodb-password: password123
  jwt-secret: your-super-secret-jwt-key
  cloudinary-cloud-name: your-cloud-name
  cloudinary-api-key: your-api-key
  cloudinary-api-secret: your-api-secret
```

## 🗄️ Step 5: Database Configuration

### Deploy MongoDB
```bash
kubectl apply -f k8s/db/mongodb-pv.yml
kubectl apply -f k8s/db/mongodb-pvc.yml
kubectl apply -f k8s/db/mongodb-deployment.yml
kubectl apply -f k8s/db/mongodb-service.yml
```

### Key MongoDB Manifests
- **Persistent Volume**: 10Gi storage for data persistence
- **Persistent Volume Claim**: Dynamic storage allocation
- **Deployment**: StatefulSet-like deployment with 1 replica
- **Service**: ClusterIP service for internal communication

## 🔧 Step 6: Backend Deployment

### Deploy Backend Services
```bash
kubectl apply -f k8s/backend/backend-deployment.yml
kubectl apply -f k8s/backend/backend-service.yml
kubectl apply -f k8s/backend/backend-hpa.yml
```

### Backend Features
- **Deployment**: 3 replicas with rolling updates
- **Service**: ClusterIP service exposing port 5001
- **HPA**: Auto-scaling from 2-10 pods based on CPU (70%)
- **Health Checks**: Readiness and liveness probes
- **Resource Limits**: CPU and memory constraints

## 🎨 Step 7: Frontend Deployment

### Deploy Frontend Services
```bash
kubectl apply -f k8s/frontend/frontend-deployment.yml
kubectl apply -f k8s/frontend/frontend-service.yml
kubectl apply -f k8s/frontend/frontend-hpa.yml
```

### Frontend Features
- **Nginx-based**: Optimized static file serving
- **Auto-scaling**: 2-8 pods based on CPU usage
- **Resource Optimization**: Efficient memory and CPU usage
- **Health Endpoints**: Custom health check routes

## 🌐 Step 8: Ingress Configuration

### Deploy Ingress
```bash
# Install Nginx Ingress Controller (if not already installed)
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.1/deploy/static/provider/cloud/deploy.yaml

# Apply ingress configuration
kubectl apply -f k8s/ingress/ingress.yml
```

### Ingress Features
- **Path-based routing**: `/api/*` → Backend, `/*` → Frontend
- **TLS termination**: SSL certificate management
- **Load balancing**: Automatic traffic distribution

## 🔒 Step 9: SSL/TLS Configuration

### Create Self-Signed Certificate
```bash
# Generate self-signed certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout tls.key -out tls.crt \
  -subj "/CN=chat-app.local/O=chat-app"

# Create TLS secret
kubectl create secret tls chat-app-tls \
  --cert=tls.crt --key=tls.key -n chat-app

# Or apply the manifest
kubectl apply -f k8s/chat-app-tls.yml
```

## 📊 Step 10: Monitoring with Prometheus & Grafana

### Install Monitoring Stack
```bash
# Add Helm repositories
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

# Install Prometheus
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring --create-namespace \
  --set grafana.adminPassword=admin123

# Port forward to access services
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80 &
kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-prometheus 9090:9090 &
```

### Access Monitoring
- **Grafana**: http://localhost:3000 (admin/admin123)
- **Prometheus**: http://localhost:9090

## 📈 Step 11: Backend Metrics Implementation

### Add Metrics Endpoint to Backend
```javascript
// Add to backend/src/index.js
const promClient = require('prom-client');

// Create a Registry
const register = new promClient.Registry();

// Add default metrics
promClient.collectDefaultMetrics({ register });

// Custom metrics
const httpDuration = new promClient.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status_code'],
});

const httpRequestsTotal = new promClient.Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'route', 'status_code'],
});

register.registerMetric(httpDuration);
register.registerMetric(httpRequestsTotal);

// Metrics endpoint
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', register.contentType);
  res.end(await register.metrics());
});
```

## 🚀 Deployment Commands

### Complete Deployment
```bash
# 1. Build and push Docker images
docker build -t yourusername/chat-frontend:v1.0.0 ./frontend
docker build -t yourusername/chat-backend:v1.0.0 ./backend
docker push yourusername/chat-frontend:v1.0.0
docker push yourusername/chat-backend:v1.0.0

# 2. Deploy to Kubernetes
kubectl apply -f k8s/namespace.yml
kubectl apply -f k8s/secret.yml

# 3. Deploy database
kubectl apply -f k8s/db/

# 4. Deploy backend
kubectl apply -f k8s/backend/

# 5. Deploy frontend
kubectl apply -f k8s/frontend/

# 6. Configure ingress and TLS
kubectl apply -f k8s/ingress/
kubectl apply -f k8s/chat-app-tls.yml

# 7. Install monitoring
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring --create-namespace

# 8. Verify deployment
kubectl get pods -n chat-app
kubectl get svc -n chat-app
kubectl get ingress -n chat-app
```

### Useful Commands
```bash
# Check application status
kubectl get all -n chat-app

# View logs
kubectl logs -f deployment/chat-backend -n chat-app
kubectl logs -f deployment/chat-frontend -n chat-app

# Scale manually
kubectl scale deployment chat-backend --replicas=5 -n chat-app

# Check HPA status
kubectl get hpa -n chat-app

# Port forward for local testing
kubectl port-forward svc/chat-frontend-service 8080:80 -n chat-app
```

## 🧪 Load Testing

### Using Locust
```bash
# Install Locust
pip install locust

# Run load test
cd k8s
locust -f locust.py --host=http://your-app-url
```

## 🔍 Monitoring & Observability

### Key Metrics to Monitor
- **Application Metrics**: Response time, error rate, throughput
- **Infrastructure Metrics**: CPU, memory, disk usage
- **Custom Metrics**: Active users, messages per second
- **Business Metrics**: User engagement, feature usage

## 📊 DevOps Monitoring Dashboard

### **Key Performance Indicators (KPIs)**
```bash
# Application Health Metrics
- API Success Rate: 99.5%+
- WebSocket Connection Stability: 99.8%+
- Database Query Performance: <20ms avg
- Container Resource Utilization: 60-80%

# Infrastructure Metrics
- Pod Restart Rate: <1% per day
- Node Resource Consumption: <70%
- Storage I/O Performance: <5ms latency
- Network Throughput: 1Gbps+

# Deployment Metrics
- Deployment Frequency: On-demand
- Lead Time for Changes: <30 minutes
- Mean Time to Recovery: <5 minutes
- Change Failure Rate: <2%
```

### **Grafana Dashboard Components**
- **Application Performance Monitoring (APM)**
- **Kubernetes Cluster Overview**
- **MongoDB Performance Metrics**
- **Ingress Traffic Analytics**
- **Custom Business Metrics**

## 📁 Project Structure

```
chat-application/
├── backend/                 # Node.js API server
├── frontend/               # React application
├── k8s/                   # Kubernetes manifests
│   ├── backend/           # Backend K8s resources
│   ├── frontend/          # Frontend K8s resources
│   ├── db/               # Database K8s resources
│   └── ingress/          # Ingress configuration
└── docker-compose.yml    # Local development setup
```

## 🐛 Troubleshooting

### Common Issues
```bash
# Pod not starting
kubectl describe pod <pod-name> -n chat-app

# Service not accessible
kubectl get endpoints -n chat-app

# Ingress issues
kubectl describe ingress chat-app-ingress -n chat-app

# Check secrets
kubectl get secrets -n chat-app
kubectl describe secret chat-app-secrets -n chat-app
```

## 📁 Project Structure

```
chat-application/
├── backend/                 # Node.js API server
├── frontend/               # React application
├── k8s/                   # Kubernetes manifests
│   ├── backend/           # Backend K8s resources
│   ├── frontend/          # Frontend K8s resources
│   ├── db/               # Database K8s resources
│   └── ingress/          # Ingress configuration
└── docker-compose.yml    # Local development setup
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


**Built with ❤️ using modern DevOps practices**