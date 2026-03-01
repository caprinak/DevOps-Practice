# Detailed Report: Docker & Kubernetes Auto-start Investigation

**Date:** 2026-03-01
**Location:** `e:\KHOA\HAPPY_CODING\CODER THAN THANH\microservices&devops`

## 1. Executive Summary
This report documents the investigation into why Docker containers and Kubernetes pods are automatically running on Windows startup. We have identified several active deployments and system configurations that cause this behavior and proposed a plan to transition to an "on-demand" usage model.

## 2. Technical Findings

### 2.1 Active Docker Compose Projects
One active Docker Compose project was detected running in the background:
- **Project Name:** `fully-completed-microservices-java-springboot`
- **Location:** `E:\KHOA\HAPPY_CODING\CODER THAN THANH\microservices&devops\fully-completed-microservices-Java-Springboot\docker-compose.yml`
- **Status:** Running (3 containers)

### 2.2 Active Kubernetes Deployments
The following deployments are active in the Local Kubernetes cluster (Docker Desktop):
- `client-depl`: 1/1 replicas
- `currency-conversion`: 1/1 replicas
- `currency-exchange`: 1/1 replicas

These deployments are set to keep their pods running. Because Docker Desktop's Kubernetes cluster persists its state, these pods are automatically restarted whenever the cluster starts.

### 2.3 System Services & Startup
The primary "trigger" for these containers is **Docker Desktop**.
- **Windows Startup:** Docker Desktop is likely configured to start automatically upon user login.
- **Service Dependency:** When Docker Desktop starts, it initializes the Docker Engine and the Kubernetes cluster (if enabled). 
- **Persistence:** These engines then resume the previous state, starting all containers and pods that were running when the system last shut down.

---

## 3. Investigation Steps & Commands Used

To identify the root cause, I performed the following steps from the terminal:

### Step A: Check for All Docker Containers
I first checked if any containers (running or stopped) existed on the system to see if something was trying to restart.
**Command:**
```powershell
docker ps -a
```
*Result:* Most containers were in `Exited` status, but it confirmed Docker was active.

### Step B: Identify Running Kubernetes Pods
Since Docker Desktop often runs Kubernetes, I checked for pods across all namespaces.
**Command:**
```powershell
kubectl get pods -A
```
*Result:* Found several pods in the `default` namespace with `Running` status and recent restart times (~3 minutes ago), confirming they auto-started with the system.

### Step C: Identify the Controlling Deployments
Pods in K8s are usually managed by Deployments. I listed them to see which ones governed the auto-starting pods.
**Command:**
```powershell
kubectl get deployments -A
```
*Result:* Identified `client-depl`, `currency-conversion`, and `currency-exchange` as the active controllers.

### Step D: Identify Docker Compose Projects
I checked if any higher-level Docker Compose projects were managing groups of containers.
**Command:**
```powershell
docker compose ls
```
*Result:* Identified the `fully-completed-microservices-java-springboot` project as "running".

### Step E: Verify Environment Setup Scripts
I checked existing shell scripts (like `setup-env.sh`) to see if any local automation was triggering these starts.
**Command:**
```powershell
view_file setup-env.sh
```
*Result:* The script only configures the PATH and verifies versions; it does not trigger the services.

---

---

## 4. Recommended Resolution (Original Plan)

To achieve an "on-demand" only workflow, we recommend the following four-step approach:

### Step 1: Manual Configuration (One-time)
Disable the automatic startup of the Docker Desktop application itself:
1. Open **Docker Desktop Settings**.
2. **General** > Uncheck **"Start Docker Desktop when you log in"**.

### Step 2: Resource Cleanup
Stop currently running resources so they don't "resume" automatically next time:
- Stop the Docker Compose project.
- Scale down K8s deployments to `0` replicas using:
  ```powershell
  kubectl scale deployment client-depl --replicas=0
  kubectl scale deployment currency-conversion --replicas=0
  kubectl scale deployment currency-exchange --replicas=0
  ```

### Step 3: Automation Scripts
Create simple `.ps1` or `.sh` scripts in this folder to start/stop the environment with a single click.

### Step 4: Verification
Confirm that no containers are running after a system reboot until manually triggered.

---

## 5. Implementation & Results

As of 2026-03-01, I have executed the following actions to transition the environment to on-demand:

### 4.1. Immediate Resource Cleanup
I ran the following commands to stop current background activity:
- **Kubernetes Scale down**:
  ```powershell
  kubectl scale deployment client-depl --replicas=0
  kubectl scale deployment currency-conversion --replicas=0
  kubectl scale deployment currency-exchange --replicas=0
  ```
- **Docker Compose Stop**:
  ```powershell
  docker compose -f "E:\KHOA\HAPPY_CODING\CODER THAN THANH\microservices&devops\fully-completed-microservices-Java-Springboot\docker-compose.yml" stop
  ```

### 4.2. On-Demand Automation Scripts
I created two utility scripts in this directory (`e:\KHOA\HAPPY_CODING\CODER THAN THANH\microservices&devops\`) for quick control:
- **`start-microservices.ps1`**: Re-activates the Docker Compose project and scales K8s deployments back to 1 replica.
- **`stop-microservices.ps1`**: Stops the Docker Compose project and scales deployments back to 0.

---

## 6. Professional Advice for On-Demand Development

To keep your Windows environment fast and clean while working with microservices and DevOps tools, I recommend the following:

### 5.1. Manage Docker Desktop Startup
The most effective way to prevent auto-start is to disable the application itself from Windows startup:
- **Action**: Go to **Docker Desktop Settings** > **General** and uncheck **"Start Docker Desktop when you log in"**. Only open Docker Desktop when you are actually about to start development.

### 5.2. Kubernetes Resource Management
Kubernetes clusters in Docker Desktop use a significant amount of RAM (often ~2GB+ just to stay idle).
- **Advice**: If you are only working on Docker projects (without K8s), consider disabling Kubernetes in **Settings** > **Kubernetes** to free up memory. You can toggle it back on whenever you need it.

### 5.3. WSL2 Memory Limit
If you use WSL2 (highly recommended for Docker on Windows), it can sometimes consume all available system RAM.
- **Advice**: Create a `.wslconfig` file in your `%UserProfile%` directory to limit how much RAM WSL2 can use (e.g., `memory=4GB`).

### 5.4. Use "Profiles" in Docker Compose
If your project grows, you might not want *every* service to start even when you run `up`.
- **Advice**: Use the `profiles` feature in `docker-compose.yml` to group services (e.g., `profiles: ["backend"]`, `profiles: ["monitoring"]`). You can then start specific groups with `docker compose --profile backend up`.

---

## 7. Conclusion
The environment is now configured for manual, on-demand use. By following the "Next Action" in Section 6.1, you will ensure a completely silent system on startup with no hidden container overhead.
