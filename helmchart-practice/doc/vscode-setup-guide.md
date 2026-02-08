# Kubernetes & Helm Development Setup for VSCode (Antigravity)

## Step 1: Install Helm

Helm is the package manager for Kubernetes. Let's install it.

### For Windows (using Chocolatey):
```powershell
choco install kubernetes-helm
```

### For Windows (manual):
1. Download from: https://github.com/helm/helm/releases/latest
2. Extract helm.exe to a folder (e.g., C:\Program Files\Helm)
3. Add that folder to your PATH environment variable

### Verify installation:
```bash
helm version
```

---

## Step 2: Install k3d (Local Kubernetes Cluster)

k3d creates a lightweight Kubernetes cluster locally using Docker.

### For Windows (using Chocolatey):
```powershell
choco install k3d
```

### Alternative - Install Docker Desktop first:
If you don't have Docker Desktop:
1. Download from: https://www.docker.com/products/docker-desktop
2. Install and enable Kubernetes in Docker Desktop settings
3. Or use k3d for a separate cluster

### Verify installation:
```bash
k3d version
```

---

## Step 3: Create Local Cluster with k3d

```bash
# Create a cluster named "helm-practice"
k3d cluster create helm-practice

# Verify cluster is running
kubectl cluster-info
kubectl get nodes
```

---

## Step 4: Install VSCode Extensions

Open VSCode (Antigravity) and install these extensions:

### Essential Extensions:

1. **Kubernetes** by Microsoft
   - ID: `ms-kubernetes-tools.vscode-kubernetes-tools`
   - Provides: Cluster explorer, resource management, Helm support

2. **Helm Intellisense** by Tim Koehler
   - ID: `tim-koehler.helm-intellisense`
   - Provides: Autocomplete for Helm templates

3. **YAML** by Red Hat
   - ID: `redhat.vscode-yaml`
   - Provides: YAML validation and autocomplete

4. **Kubernetes Support** (alternative)
   - ID: `ipedrazas.kubernetes-snippets`
   - Provides: Code snippets for K8s resources

### How to Install:

**Method 1 - Through VSCode UI:**
1. Open VSCode
2. Press `Ctrl+Shift+X` (or click Extensions icon in sidebar)
3. Search for each extension name above
4. Click "Install"

**Method 2 - Command Line:**
```bash
code --install-extension ms-kubernetes-tools.vscode-kubernetes-tools
code --install-extension tim-koehler.helm-intellisense
code --install-extension redhat.vscode-yaml
```

---

## Step 5: Configure VSCode Kubernetes Extension

After installing the Kubernetes extension:

1. **Open Command Palette**: Press `Ctrl+Shift+P`
2. Type: `Kubernetes: Set Kubeconfig`
3. Select your kubeconfig file (usually at `~/.kube/config`)
4. You should see the Kubernetes icon in the Activity Bar (left sidebar)

### If you don't see the Kubernetes panel:
1. Press `Ctrl+Shift+P`
2. Type: `View: Toggle Kubernetes`
3. Or look for the Kubernetes icon (looks like a ship wheel) in the left sidebar

---

## Step 6: Verify Everything Works

### Check CLI tools:
```bash
# Should show kubectl version
kubectl version --client

# Should show Helm version
helm version

# Should show k3d version
k3d version
```

### Check VSCode Integration:
1. Open VSCode
2. Look at the left sidebar - you should see:
   - Kubernetes icon (ship wheel)
   - Helm icon (anchor)
3. Click Kubernetes icon to see:
   - Your cluster name
   - Namespaces
   - Workloads (Pods, Deployments, Services)
   - Network (Services, Ingresses)
   - Configuration (ConfigMaps, Secrets)

---

## Step 7: Quick Test

Create a test deployment to verify everything works:

```bash
# Create a simple nginx deployment
kubectl create deployment test-nginx --image=nginx

# Expose it
kubectl expose deployment test-nginx --port=80 --type=NodePort

# Check in VSCode - you should see it in the Kubernetes panel!
```

Then delete it:
```bash
kubectl delete deployment test-nginx
kubectl delete service test-nginx
```

---

## Troubleshooting

### "kubectl not found" in VSCode terminal:
- Restart VSCode after installing kubectl
- Make sure kubectl is in your PATH

### Kubernetes panel not showing:
1. Press `Ctrl+Shift+P`
2. Type: `Developer: Reload Window`
3. Wait for extensions to load

### Can't connect to cluster:
```bash
# Check if cluster exists
k3d cluster list

# If not, create it
k3d cluster create helm-practice

# Set kubeconfig
kubectl config use-context k3d-helm-practice
```

---

## Summary - You Should Now Have:

✅ **kubectl** - Kubernetes CLI  
✅ **helm** - Package manager for Kubernetes  
✅ **k3d** - Local Kubernetes cluster tool  
✅ **VSCode Extensions**:
   - Kubernetes explorer
   - Helm intellisense
   - YAML support

**Next:** Go back to Stage 1 of Helm practice!
