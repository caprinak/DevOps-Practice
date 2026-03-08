# Start Microservices (Docker Compose and Kubernetes)
Write-Host "Ensuring Kubernetes is Enabled in Docker Settings..." -ForegroundColor Cyan
$settingsPath = "$env:APPDATA\Docker\settings-store.json"
if (Test-Path $settingsPath) {
    $settings = Get-Content $settingsPath | ConvertFrom-Json
    if ($settings.KubernetesEnabled -ne $true) {
        $settings.KubernetesEnabled = $true
        $settings | ConvertTo-Json | Set-Content $settingsPath
        Write-Host "Kubernetes has been enabled in settings. Please ensure Docker Desktop is running." -ForegroundColor Yellow
    }
}

Write-Host "Starting Docker Compose Project..." -ForegroundColor Cyan
docker compose -f "E:\KHOA\HAPPY_CODING\CODER THAN THANH\microservices&devops\fully-completed-microservices-Java-Springboot\docker-compose.yml" up -d

Write-Host "Waiting for Kubernetes API Server (this may take 1-2 minutes)..." -ForegroundColor Cyan
while (!(kubectl get nodes 2>$null)) { Start-Sleep -Seconds 5 }

Write-Host "Scaling up Kubernetes Deployments..." -ForegroundColor Cyan
kubectl scale deployment client-depl --replicas=1
kubectl scale deployment currency-conversion --replicas=1
kubectl scale deployment currency-exchange --replicas=1

Write-Host "Environment Started!" -ForegroundColor Green
Write-Host "Next Steps: Access your services using port-forwarding as described in the report." -ForegroundColor White
