# Start Microservices (Docker Compose and Kubernetes)
Write-Host "Starting Docker Compose Project..." -ForegroundColor Cyan
docker compose -f "E:\KHOA\HAPPY_CODING\CODER THAN THANH\microservices&devops\fully-completed-microservices-Java-Springboot\docker-compose.yml" up -d

Write-Host "Scaling up Kubernetes Deployments..." -ForegroundColor Cyan
kubectl scale deployment client-depl --replicas=1
kubectl scale deployment currency-conversion --replicas=1
kubectl scale deployment currency-exchange --replicas=1

Write-Host "Environment Started!" -ForegroundColor Green
