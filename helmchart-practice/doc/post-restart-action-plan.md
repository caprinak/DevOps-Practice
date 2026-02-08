# Post-IDE Restart Action Plan
## What To Do After Restarting VSCode (Antigravity)

---

## ✅ STEP 1: Verify Extensions Are Installed

After VSCode restarts, check if these 3 extensions are installed:

### Check Method:
1. Press `Ctrl+Shift+X` (Extensions panel)
2. Look for these in "INSTALLED" section:

**Required Extensions:**
- [ ] **Kubernetes** by Microsoft (ID: ms-kubernetes-tools.vscode-kubernetes-tools)
- [ ] **Helm Intellisense** by Tim Koehler (ID: tim-koehler.helm-intellisense)
- [ ] **YAML** by Red Hat (ID: redhat.vscode-yaml)

### If NOT installed:
**Install them one by one:**
1. In Extensions panel search box, type: `Kubernetes`
2. Find "Kubernetes" by Microsoft → Click **Install**
3. Search: `Helm Intellisense`
4. Find "Helm Intellisense" by Tim Koehler → Click **Install**
5. Search: `YAML`
6. Find "YAML" by Red Hat → Click **Install**

---

## ✅ STEP 2: Open Terminal in VSCode

### Method:
1. Press `` Ctrl+` `` (backtick) - This opens integrated terminal
   OR
2. Menu: Terminal → New Terminal

### What you should see:
- Terminal opens at bottom of VSCode
- Shows your current directory
- Ready to accept commands

---

## ✅ STEP 3: Verify Tools Work in VSCode Terminal

### Run these commands ONE BY ONE:

```bash
# 1. Check kubectl
kubectl version --client
```
**Expected:** Client Version: v1.30.5

```bash
# 2. Check Helm (use full path first)
~/bin/helm.exe version
```
**Expected:** version.BuildInfo{Version:"v3.20.0"...}

```bash
# 3. Check k3d
~/bin/k3d.exe version
```
**Expected:** k3d version v5.8.3

### If commands work → ✅ Proceed to Step 4

### If "command not found" errors:
**Fix PATH in VSCode:**
```bash
# Add to your shell profile
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

Then retry the commands.

---

## ✅ STEP 4: Create Local Kubernetes Cluster

### Command:
```bash
~/bin/k3d.exe cluster create helm-practice
```

### Expected Output:
```
INFO[0000] Prep: Network
INFO[0000] Created network 'k3d-helm-practice'
INFO[0000] Created image volume...
INFO[0001] Creating node...
INFO[0012] Creating LoadBalancer...
INFO[0013] Using the k3d-helm-practice cluster
INFO[0013] You can now use it like this:
kubectl cluster-info
```

### Verify cluster is running:
```bash
kubectl cluster-info
```
**Expected:**
```
Kubernetes control plane is running at https://0.0.0.0:xxxxx
CoreDNS is running at...
```

```bash
kubectl get nodes
```
**Expected:**
```
NAME                      STATUS   ROLES                  AGE   VERSION
k3d-helm-practice-server-0   Ready    control-plane,master   30s   v1.31.5+k3s1
```

---

## ✅ STEP 5: Check VSCode Kubernetes Panel

### Open Kubernetes View:
1. Look at **left sidebar** (Activity Bar)
2. Find **Kubernetes icon** (looks like a ship wheel ⚓)
3. **Click it**

### What you should see:
```
⚓ KUBERNETES
└── k3d-helm-practice
    ├── Cluster
    ├── Workloads
    │   ├── Deployments
    │   ├── Pods
    │   └── Replica Sets
    ├── Network
    │   ├── Services
    │   └── Ingresses
    ├── Storage
    ├── Configuration
    │   ├── ConfigMaps
    │   └── Secrets
    └── Helm Releases
```

### If you DON'T see the Kubernetes icon:
1. Press `Ctrl+Shift+P` (Command Palette)
2. Type: `View: Toggle Kubernetes`
3. Press Enter
4. Icon should appear in left sidebar

---

## ✅ STEP 6: Start Stage 1 - Manual vs Helm Comparison

### 6.1 Deploy Manually (The Old Way)

**Navigate to practice folder:**
```bash
cd ~/helmchart-practice
```

**Check the manual deployment file exists:**
```bash
ls -la manual-deployment.yaml
```

**Deploy it:**
```bash
kubectl apply -f manual-deployment.yaml
```

**Verify in VSCode:**
- Look at Kubernetes panel
- Expand: k3d-helm-practice → Workloads → Pods
- You should see: `manual-nginx-xxxxxxxxxx-xxxxx` pod

**Check from terminal:**
```bash
kubectl get pods,svc
```

### 6.2 Try to Rollback (Show the Problem!)

**Attempt rollback:**
```bash
kubectl rollout history deployment/manual-nginx
```

**What you see:** Limited history, no easy rollback to specific configs.

**The PROBLEM:** No clean way to rollback changes!

### 6.3 Delete Manual Deployment

```bash
kubectl delete -f manual-deployment.yaml
```

**Verify in VSCode:**
- Pod should disappear from Kubernetes panel

---

## ✅ STEP 7: Deploy with Helm (The Right Way)

### 7.1 Add Helm Repository

```bash
~/bin/helm.exe repo add bitnami https://charts.bitnami.com/bitnami
~/bin/helm.exe repo update
```

### 7.2 Install with Helm

```bash
~/bin/helm.exe install my-nginx bitnami/nginx
```

### 7.3 Check in VSCode

**In Kubernetes Panel:**
- Look under "Helm Releases"
- You should see: `my-nginx` release

**In Terminal:**
```bash
~/bin/helm.exe list
```
**Expected:**
```
NAME       NAMESPACE  REVISION  STATUS    CHART       APP VERSION
my-nginx   default    1         deployed  nginx-xx.x  x.x.x
```

### 7.4 Check History

```bash
~/bin/helm.exe history my-nginx
```
**Expected:**
```
REVISION  UPDATED                   STATUS     CHART       DESCRIPTION
1         [timestamp]               deployed   nginx-xx.x  Install complete
```

### 7.5 Upgrade the Deployment

```bash
~/bin/helm.exe upgrade my-nginx bitnami/nginx --set replicaCount=3
```

**Check history again:**
```bash
~/bin/helm.exe history my-nginx
```
**Now you see:**
```
REVISION  STATUS
1         superseded
2         deployed   ← Current version
```

**Check pods in VSCode:**
- You should now see 3 nginx pods instead of 1!

### 7.6 Rollback Magic

```bash
~/bin/helm.exe rollback my-nginx 1
```

**Check history:**
```bash
~/bin/helm.exe history my-nginx
```
**Now you see:**
```
REVISION  STATUS
1         superseded
2         superseded
3         deployed   ← Rolled back to version 1!
```

**Check in VSCode:**
- Pods reduced back to 1!

---

## ✅ STEP 8: See What Helm Actually Does

```bash
~/bin/helm.exe template my-nginx bitnami/nginx
```

**This outputs:** Pages of generated Kubernetes YAML!

**Key Insight:** Helm is just a YAML generator + release tracker.

---

## ✅ STEP 9: Cleanup

```bash
# Remove Helm release
~/bin/helm.exe uninstall my-nginx

# Verify nothing left
kubectl get all
```

**In VSCode:**
- All pods should disappear

---

## ✅ STEP 10: Delete Cluster (Optional)

When done practicing:
```bash
~/bin/k3d.exe cluster delete helm-practice
```

---

## 📋 CHECKLIST SUMMARY

After IDE restart, complete these:

- [ ] Extensions installed (Kubernetes, Helm Intellisense, YAML)
- [ ] Terminal opens with `` Ctrl+` ``
- [ ] kubectl works: `kubectl version --client`
- [ ] Helm works: `~/bin/helm.exe version`
- [ ] k3d works: `~/bin/k3d.exe version`
- [ ] Cluster created: `~/bin/k3d.exe cluster create helm-practice`
- [ ] Kubernetes panel visible in VSCode sidebar
- [ ] Manual deployment tested
- [ ] Helm deployment tested
- [ ] Rollback demonstrated
- [ ] Cleanup completed

---

## 🆘 TROUBLESHOOTING

### Problem: "command not found" for helm or k3d
**Solution:**
```bash
export PATH="$HOME/bin:$PATH"
# Add to ~/.bashrc for permanent fix
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Problem: Kubernetes panel not showing
**Solution:**
```bash
# In VSCode Command Palette (Ctrl+Shift+P)
View: Toggle Kubernetes
```

### Problem: Cluster creation fails
**Solution:**
```bash
# Check if Docker is running
docker ps

# If Docker not running, start Docker Desktop first

# Check existing clusters
~/bin/k3d.exe cluster list

# Delete if exists
~/bin/k3d.exe cluster delete helm-practice

# Recreate
~/bin/k3d.exe cluster create helm-practice
```

### Problem: kubectl can't connect to cluster
**Solution:**
```bash
# Check current context
kubectl config current-context

# Should show: k3d-helm-practice

# If not, switch context
kubectl config use-context k3d-helm-practice
```

---

## 🎯 SUCCESS CRITERIA

You'll know everything is working when:
1. ✅ You can see the Kubernetes icon in VSCode sidebar
2. ✅ You can see your cluster and pods in the Kubernetes panel
3. ✅ `helm list` shows releases with versions
4. ✅ `helm rollback` actually changes the number of pods
5. ✅ You understand: **Helm = YAML generator + release tracker**

---

**Ready to restart?** 

After restart, we'll:
1. Install extensions (if not done)
2. Create cluster
3. Run through Stage 1 step by step
4. You'll see manual vs Helm difference firsthand!

**Tell me when your IDE is restarted!**
