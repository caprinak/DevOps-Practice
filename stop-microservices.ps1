# Stop Microservices (Docker Compose and Kubernetes)
Write-Host "Stopping Docker Compose Project..." -ForegroundColor Yellow
docker compose -f "E:\KHOA\HAPPY_CODING\CODER THAN THANH\microservices&devops\fully-completed-microservices-Java-Springboot\docker-compose.yml" stop

Write-Host "Scaling down Kubernetes Deployments..." -ForegroundColor Yellow
kubectl scale deployment client-depl --replicas=0
kubectl scale deployment currency-conversion --replicas=0
kubectl scale deployment currency-exchange --replicas=0

Write-Host "Environment Stopped!" -ForegroundColor Green
