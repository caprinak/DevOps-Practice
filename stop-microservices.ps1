# Stop Microservices (Docker Compose and Kubernetes)
Write-Host "Scaling down Kubernetes Deployments..." -ForegroundColor Cyan
kubectl scale deployment client-depl --replicas=0
kubectl scale deployment currency-conversion --replicas=0
kubectl scale deployment currency-exchange --replicas=0

Write-Host "Stopping Docker Compose Project..." -ForegroundColor Cyan
docker compose -f "E:\KHOA\HAPPY_CODING\CODER THAN THANH\microservices&devops\fully-completed-microservices-Java-Springboot\docker-compose.yml" stop

Write-Host "Disabling Kubernetes to save resources..." -ForegroundColor Cyan
$settingsPath = "$env:APPDATA\Docker\settings-store.json"
if (Test-Path $settingsPath) {
    $settings = Get-Content $settingsPath | ConvertFrom-Json
    if ($settings.KubernetesEnabled -ne $false) {
        $settings.KubernetesEnabled = $false
        $settings | ConvertTo-Json | Set-Content $settingsPath
        Write-Host "Kubernetes has been disabled. It will stay off until you run the start script again." -ForegroundColor Yellow
    }
}

Write-Host "Environment Stopped!" -ForegroundColor Green
