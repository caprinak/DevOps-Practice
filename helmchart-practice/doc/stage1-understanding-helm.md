# Helm Practice - Stage 1: Understanding What Helm Actually Is

## Overview
This guide will show you the fundamental difference between manual kubectl deployments and Helm deployments. You'll see why Helm is essential for production environments.

---

## Step 1: Create Manual Deployment File

**What we're doing:** Creating a standard Kubernetes deployment YAML file manually.

**File created:** `manual-deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: manual-nginx
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.27
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: manual-nginx-service
spec:
  selector:
    app: nginx
  ports:
  - port: 80
    targetPort: 80
  type: ClusterIP
```

**What to check:** Look at the file structure and understand it defines:
- A Deployment with 1 nginx replica
- A Service to expose the deployment

---

## Step 2: Deploy Manually

**Command:**
```bash
kubectl apply -f manual-deployment.yaml
```

**Expected output:**
```
deployment.apps/manual-nginx created
service/manual-nginx-service created
```

**What happened:** Kubernetes created your deployment and service.

**Check command:**
```bash
kubectl get pods,svc
```

**Expected output:**
```
NAME                                READY   STATUS    RESTARTS   AGE
pod/manual-nginx-xxxxxxxxxx-xxxxx   1/1     Running   0          10s

NAME                         TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE
service/manual-nginx-service ClusterIP   10.43.xxx.xxx  <none>        80/TCP    10s
```

---

## Step 3: Try to Track Changes (The Problem!)

**Try to see deployment history:**
```bash
kubectl rollout history deployment/manual-nginx
```

**What you see:** Limited rollout history, no easy rollback mechanism.

**The problem:** Kubernetes tracks rollouts for the deployment itself, but:
- No easy way to rollback to specific previous states
- No tracking of WHAT changed (values, configs, etc.)
- If you delete it, history is gone

---

## Step 4: Delete Manual Deployment

**Command:**
```bash
kubectl delete -f manual-deployment.yaml
```

**Expected output:**
```
deployment.apps "manual-nginx" deleted
service "manual-nginx-service" deleted
```

**Try to rollback now:**
```bash
kubectl rollout undo deployment/manual-nginx
```

**Expected output:**
```
Error from server (NotFound): deployments.apps "manual-nginx" not found
```

**🚨 THE PROBLEM:** Once deleted, you CANNOT rollback. You have to manually recreate everything!

---

## Step 5: Install with Helm (The Solution!)

**Command:**
```bash
helm install my-nginx bitnami/nginx
```

**Expected output:**
```
NAME: my-nginx
LAST DEPLOYED: [timestamp]
NAMESPACE: default
STATUS: deployed
REVISION: 1
NOTES: ...
```

**What happened:**
- Helm created a "Release" called `my-nginx`
- It tracks this release with REVISION: 1
- It stores the state of this deployment

**Check what Helm knows:**
```bash
helm list
```

**Expected output:**
```
NAME       NAMESPACE  REVISION  UPDATED                   STATUS    CHART         APP VERSION
my-nginx   default    1         [timestamp]               deployed  nginx-xx.x.x  x.x.x
```

**🎯 KEY INSIGHT:** Helm is now TRACKING your deployment!

---

## Step 6: Check Helm History

**Command:**
```bash
helm history my-nginx
```

**Expected output:**
```
REVISION  UPDATED                   STATUS      CHART          APP VERSION  DESCRIPTION
1         [timestamp]               deployed    nginx-xx.x.x   x.x.x        Install complete
```

**What this shows:**
- You have 1 revision (the initial install)
- Helm remembers the state, chart version, and what happened

---

## Step 7: Upgrade with Helm

**Command:**
```bash
helm upgrade my-nginx bitnami/nginx --set replicaCount=3
```

**Expected output:**
```
Release "my-nginx" has been upgraded. Happy Helming!
NAME: my-nginx
LAST DEPLOYED: [timestamp]
NAMESPACE: default
STATUS: deployed
REVISION: 2
```

**Notice:** REVISION is now 2!

**Verify the upgrade:**
```bash
kubectl get pods
```

**Expected output:** 3 nginx pods running (instead of 1)

---

## Step 8: Check History After Upgrade

**Command:**
```bash
helm history my-nginx
```

**Expected output:**
```
REVISION  UPDATED                   STATUS      CHART          APP VERSION  DESCRIPTION
1         [timestamp]               superseded  nginx-xx.x.x   x.x.x        Install complete
2         [timestamp]               deployed    nginx-xx.x.x   x.x.x        Upgrade complete
```

**🎯 KEY INSIGHT:** 
- You have TWO tracked versions
- Revision 1 = original install (1 replica)
- Revision 2 = upgrade (3 replicas)
- You can go back to ANY version!

---

## Step 9: Rollback Instantly

**Command:**
```bash
helm rollback my-nginx 1
```

**Expected output:**
```
Rollback was a success! Happy Helming!
```

**Check history:**
```bash
helm history my-nginx
```

**Expected output:**
```
REVISION  UPDATED                   STATUS      CHART          APP VERSION  DESCRIPTION
1         [timestamp]               superseded  nginx-xx.x.x   x.x.x        Install complete
2         [timestamp]               superseded  nginx-xx.x.x   x.x.x        Upgrade complete
3         [timestamp]               deployed    nginx-xx.x.x   x.x.x        Rollback to 1
```

**🎯 MAGIC MOMENT:** 
- Revision 3 = your rollback (which is Revision 1's state)
- You're back to 1 replica!
- Verify: `kubectl get pods` should show 1 pod

---

## Step 10: See What Helm Actually Does

**Command:**
```bash
helm template my-nginx bitnami/nginx
```

**What you see:** Pages of generated Kubernetes YAML!

**Key observation:** Helm generates:
- Deployment
- Service
- ConfigMaps
- Secrets
- And more...

**🎯 THE BIG SECRET:**
**90% of what Helm does is just generate YAML!**

Helm is a template engine + release tracker. That's it!

---

## Step 11: Clean Up

**Command:**
```bash
helm uninstall my-nginx
```

**Expected output:**
```
release "my-nginx" uninstalled
```

**Verify nothing left:**
```bash
kubectl get all
```

**Expected output:** No nginx pods or services remaining.

---

## Summary: What You Learned in Stage 1

### Manual kubectl approach:
- ❌ No release tracking
- ❌ No easy rollback
- ❌ No history
- ❌ Manual cleanup required
- ❌ Hard to reproduce

### Helm approach:
- ✅ Every deployment is a tracked "release"
- ✅ Automatic versioning (REVISION 1, 2, 3...)
- ✅ Instant rollback to any version
- ✅ One command cleanup
- ✅ Reproducible deployments
- ✅ Template generation

### Key Commands You Learned:
```bash
helm install <name> <chart>          # Install a chart
helm upgrade <name> <chart>          # Upgrade a release
helm rollback <name> <revision>      # Rollback to a revision
helm list                            # List all releases
helm history <name>                  # Show release history
helm uninstall <name>                # Remove a release
helm template <name> <chart>         # Generate YAML only
```

---

## Next Steps

Ready for **Stage 2: Write Your First Chart from Scratch**?

You'll create:
- Chart.yaml
- values.yaml
- templates/deployment.yaml

And see how templating works!
