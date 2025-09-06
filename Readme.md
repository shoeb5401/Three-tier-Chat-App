# 🚀 Real-Time Chat Application - Complete DevOps Pipeline

A production-ready real-time chat application with full containerization, Kubernetes deployment, and comprehensive monitoring. This project demonstrates a complete DevOps workflow from development to production monitoring.

## 🏗️ Architecture Overview

![Architecture Diagram](/assets/three-tier-arch.png)

The architecture follows a microservices approach with containerized deployment and comprehensive monitoring:

### Development Phase

- **Source Control**: GitHub repository with React frontend and Node.js backend
- **Containerization**: Docker images built for each service
- **Registry**: Docker Hub for image storage and distribution

### Deployment Phase

- **Orchestration**: Kubernetes cluster with namespace isolation
- **Services**: React frontend, Node.js backend, MongoDB database
- **Auto-scaling**: Horizontal Pod Autoscalers for dynamic scaling
- **Networking**: Ingress controller for external access
- **Storage**: Persistent volumes for database persistence

### Monitoring Phase

- **Metrics**: Prometheus for metrics collection
- **Visualization**: Grafana for monitoring dashboards
- **Package Management**: Helm for streamlined deployments

## ✨ Features

- **Real-time messaging** with Socket.io
- **User authentication** with JWT tokens
- **File uploads** with Cloudinary integration
- **Responsive design** with Tailwind CSS
- **Complete containerization** with Docker
- **Production-ready Kubernetes** deployment
- **Auto-scaling** with HPA (Horizontal Pod Autoscaler)
- **Comprehensive monitoring** with Prometheus & Grafana
- **CI/CD pipeline** integration ready
- **SSL/TLS security** with certificate management
- **Persistent storage** for database

## 📋 Prerequisites

- Docker & Docker Compose
- Kubernetes cluster (minikube, kind, or cloud provider)
- kubectl configured and authenticated
- Helm 3.x for package management
- Node.js 18+ (for local development)
- Git for version control

## 🔄 DevOps Workflow

### 1. Development & Containerization

```bash
# Clone the repository
git clone https://github.com/shoeb5401/Three-tier-Chat-App.git
cd Three-tier-Chat-App

# Build Docker images
docker build -t chat-frontend:v2 ./frontend
docker build -t chat-backend:v2 ./backend
```

### 2. Docker Registry (Docker Hub)

```bash
# Tag images for Docker Hub
docker tag chat-frontend:latest yourusername/chat-frontend:v2
docker tag chat-backend:latest yourusername/chat-backend:v2

# Push to Docker Hub
docker push yourusername/chat-frontend:v2
docker push yourusername/chat-backend:v2
```

### 3. Kubernetes Deployment

#### Create Namespace and Setup

```bash
# Create dedicated namespace
kubectl create namespace chat-app
kubectl create -f k8s/namespace.yml

# Apply secrets and configurations
kubectl apply -f k8s/secrets.yml -n chat-app
```

#### Database Layer - MongoDB

```bash
# Deploy persistent storage
kubectl apply -f k8s/database/mongodb-pv.yml
kubectl apply -f k8s/database/mongodb-pvc.yml

# Deploy MongoDB
kubectl apply -f k8s/database/mongodb-deployment.yml
kubectl apply -f k8s/database/mongodb-service.yml
```

#### Backend Layer - Node.js API

```bash
# Deploy backend service
kubectl apply -f k8s/backend/nodejs-deployment.yml
kubectl apply -f k8s/backend/nodejs-service.yml

# Enable auto-scaling
kubectl apply -f k8s/backend/nodejs-hpa.yml
```

#### Frontend Layer - React App

```bash
# Deploy frontend service
kubectl apply -f k8s/frontend/react-deployment.yml
kubectl apply -f k8s/frontend/react-service.yml

# Enable auto-scaling
kubectl apply -f k8s/frontend/react-hpa.yml
```

#### Networking - Ingress

```bash
# Deploy ingress controller
kubectl apply -f k8s/ingress/ingress-deployment.yml

# Configure routing rules
kubectl apply -f k8s/ingress/ingress-rules.yml
```

## 📊 Monitoring Setup

### Deploy Prometheus & Grafana with Helm

```bash
# Add Helm repositories
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

# Create monitoring namespace
kubectl create namespace monitoring

# Install Prometheus
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --set grafana.adminPassword=admin123 \
  --set prometheus.prometheusSpec.retention=30d

# Verify deployment
kubectl get pods -n monitoring
```

### Access Monitoring Services

```bash
# Port forward Grafana
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80 &

# Port forward Prometheus
kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-prometheus 9090:9090 &
```

- **Grafana Dashboard**: http://localhost:3000 (admin/admin123)
- **Prometheus UI**: http://localhost:9090


### Monitoring Deployment Status

```bash
# Check all resources in chat-app namespace
kubectl get all -n chat-app

# Check pod status and logs
kubectl get pods -n chat-app -w
kubectl logs -f deployment/frontend-deployment -n chat-app
kubectl logs -f deployment/backend-deployment -n chat-app

# Check HPA status
kubectl get hpa -n chat-app

# Check ingress configuration
kubectl get ingress -n chat-app
kubectl describe ingress chat-app-ingress -n chat-app
```

## 📈 Performance Monitoring

### Key Metrics Tracked

#### Application Metrics

- HTTP request rate and response times
- WebSocket connection stability
- Database query performance
- Error rates and success ratios

#### Infrastructure Metrics

- Pod CPU and memory usage
- Node resource utilization
- Storage I/O performance
- Network throughput and latency

#### Business Metrics

- Active user count
- Messages per second
- Feature usage analytics
- User engagement metrics

### Grafana Dashboards

Pre-configured dashboards available:

- **Application Performance Monitoring (APM)**
- **Kubernetes Cluster Overview**
- **MongoDB Performance Metrics**
- **Ingress Traffic Analytics**
- **Custom Business Metrics**

## 🔧 Auto-Scaling Configuration

### Horizontal Pod Autoscaler (HPA) Settings

- **Frontend (React)**: 2-8 replicas based on 70% CPU utilization
- **Backend (Node.js)**: 3-10 replicas based on 70% CPU utilization
- **Database (MongoDB)**: Stateful deployment with 1 replica + backup strategy

## 🔒 Security Features

- **JWT-based authentication** with secure token management
- **TLS/SSL encryption** with automated certificate management
- **Network policies** for pod-to-pod communication
- **RBAC** (Role-Based Access Control) for Kubernetes resources
- **Secret management** using Kubernetes secrets
- **Container security** with non-root users and read-only filesystems

## 🧪 Testing & Quality Assurance

### Load Testing with Locust

```python
# locust.py
from locust import HttpUser, task, between

class ChatAppUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def load_homepage(self):
        self.client.get("/")

    @task
    def api_health_check(self):
        self.client.get("/api/health")
```

Run load testing:

```bash
pip install locust
locust -f locust.py --host=http://your-app-domain.com
```

## 📁 Project Structure

```
chat-application/
├── frontend/                   # React application
│   ├── src/
│   ├── public/
│   ├── Dockerfile
│   └── package.json
├── backend/                    # Node.js API server
│   ├── src/
│   ├── Dockerfile
│   └── package.json
├── k8s/                       # Kubernetes manifests
│   ├── namespace.yml
│   ├── secrets.yml
│   ├── database/              # MongoDB resources
│   ├── backend/               # Node.js resources
│   ├── frontend/              # React resources
│   └── ingress/               # Networking configuration
└── docker-compose.yml         # Local development
```

## 🛠️ Troubleshooting

### Common Issues and Solutions

#### Pods Not Starting

```bash
# Check pod status and events
kubectl describe pod <pod-name> -n chat-app
kubectl get events -n chat-app --sort-by='.lastTimestamp'
```

#### Service Discovery Issues

```bash
# Check service endpoints
kubectl get endpoints -n chat-app
kubectl describe service <service-name> -n chat-app
```

#### Ingress Connectivity Problems

```bash
# Verify ingress controller
kubectl get pods -n ingress-nginx
kubectl logs -f deployment/ingress-nginx-controller -n ingress-nginx
```

#### Database Connection Issues

```bash
# Check MongoDB logs
kubectl logs -f deployment/mongodb-deployment -n chat-app

# Test database connectivity
kubectl exec -it <backend-pod> -n chat-app -- npm run db:test
```
