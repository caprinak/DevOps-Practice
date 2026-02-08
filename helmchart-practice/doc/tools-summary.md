# Kubernetes & Helm Development Environment Setup
## Summary of Tools, Their Purposes, and Installation Steps

---

## 🔧 TOOLS INSTALLED & WHY WE NEED THEM

### 1. kubectl (Kubernetes Control)
**Status:** ✅ Already installed (v1.30.5)

**What it is:**
The official command-line tool for Kubernetes. It's the primary way to interact with Kubernetes clusters.

**Why we need it:**
- Deploy and manage applications on Kubernetes
- Inspect cluster resources (pods, services, deployments)
- View logs from running containers
- Execute commands inside containers
- Manage cluster configuration

**Example commands:**
```bash
kubectl get pods                    # List all pods
kubectl apply -f deployment.yaml    # Deploy from YAML file
kubectl logs my-pod                 # View pod logs
kubectl exec -it my-pod -- /bin/sh  # Enter container shell
```

---

### 2. Helm (Kubernetes Package Manager)
**Status:** ✅ Installed (v3.20.0)

**What it is:**
The package manager for Kubernetes. Think of it like `apt` for Ubuntu or `npm` for Node.js, but for Kubernetes applications.

**Why we need it:**
- **Package management:** Install complex applications (like databases, monitoring tools) with one command
- **Templating:** Generate Kubernetes YAML dynamically using variables and logic
- **Version control:** Track every deployment as a "release" with automatic versioning
- **Rollback:** Instantly rollback to any previous version
- **Dependency management:** Automatically install required services (e.g., app needs Redis? Helm installs both)

**Without Helm:**
- Write 500+ lines of YAML manually for each app
- Hardcode values (replicas, images, configs) in YAML
- No easy way to rollback when something breaks
- Manually track what version is deployed where

**With Helm:**
- Install complex apps: `helm install my-db bitnami/postgresql`
- Use variables: `{{ .Values.replicaCount }}` instead of hardcoded `replicas: 3`
- Rollback instantly: `helm rollback my-app 2`
- Track releases: `helm history my-app`

---

### 3. k3d (Local Kubernetes Cluster)
**Status:** ✅ Installed (v5.8.3)

**What it is:**
A tool to create lightweight Kubernetes clusters locally using Docker containers. Based on Rancher's k3s (lightweight Kubernetes distribution).

**Why we need it:**
- **Local development:** Test Kubernetes deployments on your machine before production
- **Fast startup:** Creates clusters in seconds (vs minutes for full Kubernetes)
- **Lightweight:** Uses minimal resources
- **Safe experimentation:** Throwaway clusters - break things without consequences
- **Multi-node:** Can simulate production clusters with multiple nodes

**Without k3d:**
- No way to test Kubernetes locally
- Have to use cloud providers (expensive, slow)
- Can't experiment safely

**With k3d:**
```bash
k3d cluster create my-cluster    # Create cluster in 30 seconds
k3d cluster delete my-cluster    # Delete when done
```

---

## 📝 WHAT WAS DONE

### Step 1: Checked Existing Tools
```bash
kubectl version --client    # ✅ Found v1.30.5
helm version                # ❌ Not found
k3d version                 # ❌ Not found
```

### Step 2: Downloaded & Installed Helm
- Downloaded: `helm-v3.20.0-windows-amd64.zip`
- Extracted to: `~/bin/helm.exe`
- Verified: `helm.exe version` → v3.20.0

### Step 3: Downloaded & Installed k3d
- Downloaded: Latest k3d release for Windows
- Installed to: `~/bin/k3d.exe`
- Verified: `k3d.exe version` → v5.8.3

### Step 4: Created Setup Script
Created `~/helmchart-practice/setup-env.sh` to:
- Add `~/bin` to PATH
- Verify all tool versions

### Step 5: Created Documentation
1. **stage1-understanding-helm.md** - Step-by-step Helm learning guide
2. **vscode-setup-guide.md** - Complete VSCode extension setup
3. **tools-summary.md** (this file) - Why we need each tool

---

## 🎯 HOW TO USE THESE TOOLS

### Quick Start Commands:

**1. Set up environment:**
```bash
export PATH="$HOME/bin:$PATH"
```

**2. Create local cluster:**
```bash
k3d.exe cluster create helm-practice
```

**3. Verify cluster:**
```bash
kubectl cluster-info
kubectl get nodes
```

**4. Install something with Helm:**
```bash
helm.exe repo add bitnami https://charts.bitnami.com/bitnami
helm.exe install my-nginx bitnami/nginx
```

**5. Check what's running:**
```bash
kubectl get pods,svc
helm.exe list
```

**6. Clean up:**
```bash
helm.exe uninstall my-nginx
k3d.exe cluster delete helm-practice
```

---

## 📦 NEXT STEPS

### For VSCode Integration:
1. Install 3 extensions:
   - Kubernetes (by Microsoft)
   - Helm Intellisense (by Tim Koehler)
   - YAML (by Red Hat)

2. Open Kubernetes panel:
   - Press `Ctrl+Shift+P`
   - Type: "View: Toggle Kubernetes"
   - Or click Kubernetes icon in left sidebar

### For Helm Practice:
1. Create cluster: `k3d.exe cluster create helm-practice`
2. Follow Stage 1 guide: `~/helmchart-practice/doc/stage1-understanding-helm.md`
3. Practice manual vs Helm deployments

---

## 🔍 VERIFICATION CHECKLIST

Run these to confirm everything works:

```bash
# Check kubectl
kubectl version --client
# Expected: v1.30.5

# Check Helm
~/bin/helm.exe version
# Expected: v3.20.0

# Check k3d
~/bin/k3d.exe version
# Expected: v5.8.3

# Check cluster (after creating it)
kubectl cluster-info
# Expected: Kubernetes control plane is running at...
```

---

## 💡 KEY CONCEPTS TO REMEMBER

| Tool | Purpose | Analogy |
|------|---------|---------|
| **kubectl** | Talk to Kubernetes | Like SSH for servers |
| **Helm** | Package & template manager | Like apt/yarn for K8s |
| **k3d** | Local test cluster | Like VirtualBox for VMs |

**The workflow:**
1. **k3d** creates a local Kubernetes cluster
2. **kubectl** lets you inspect and manage the cluster
3. **Helm** makes deploying complex applications easy

---

**Created:** 2026-02-08  
**Location:** `~/helmchart-practice/doc/tools-summary.md`
