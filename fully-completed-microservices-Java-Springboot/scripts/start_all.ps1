<#
.SYNOPSIS
    Starts all microservices in separate PowerShell windows.
    Can be run from anywhere.

.DESCRIPTION
    This script launches each microservice in a new window using absolute paths.
#>

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

Write-Host "🚀 Starting Microservices Ecosystem (Robust Pathing)..." -ForegroundColor Cyan

# Define services and their relative paths
$ServicesMap = @{
    "Config Server"        = "services/config-server"
    "Discovery Service"    = "services/discovery"
    "Gateway Service"      = "services/gateway"
    "Customer Service"     = "services/customer"
    "Product Service"      = "services/product"
    "Order Service"        = "services/order"
    "Payment Service"      = "services/payment"
    "Notification Service" = "services/notification"
}

# 1. Start Config Server first
$Name = "Config Server"
$RelPath = $ServicesMap[$Name]
$AbsPath = Join-Path $ProjectRoot $RelPath
Write-Host "   [1/8] Starting $Name..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& {HOST_TITLE='$Name'; `$host.ui.RawUI.WindowTitle = '$Name'; cd '$AbsPath'; mvn spring-boot:run}"
Start-Sleep -Seconds 15

# 2. Start Discovery Service
$Name = "Discovery Service"
$RelPath = $ServicesMap[$Name]
$AbsPath = Join-Path $ProjectRoot $RelPath
Write-Host "   [2/8] Starting $Name..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& {HOST_TITLE='$Name'; `$host.ui.RawUI.WindowTitle = '$Name'; cd '$AbsPath'; mvn spring-boot:run}"
Start-Sleep -Seconds 10

# 3. Start remaining services in parallel
$index = 3
foreach ($Name in ("Gateway Service", "Customer Service", "Product Service", "Order Service", "Payment Service", "Notification Service")) {
    $RelPath = $ServicesMap[$Name]
    $AbsPath = Join-Path $ProjectRoot $RelPath
    $Color = if ($index -eq 3) { "Cyan" } else { "Green" }
    
    Write-Host "   [$index/8] Starting $Name..." -ForegroundColor $Color
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "& {HOST_TITLE='$Name'; `$host.ui.RawUI.WindowTitle = '$Name'; cd '$AbsPath'; mvn spring-boot:run}"
    $index++
}

Write-Host "`n✅ All services have been triggered! Check the individual windows for logs." -ForegroundColor Cyan
Write-Host "⏳ Please allow 1-2 minutes for all services to register with Eureka." -ForegroundColor Gray
