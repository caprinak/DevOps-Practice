# Helm Practice - Stage 2: Writing Your First Custom Chart

## Overview
In Stage 1, you learned what Helm is (YAML generator + release tracker). Now you'll create your own Helm chart from scratch and understand how templating works.

**What you'll create:**
- A complete Helm chart with templates
- Reusable configuration via values.yaml
- Dynamic name generation
- Proper Kubernetes labels

**Time:** ~30 minutes  
**Prerequisites:** Stage 1 completed (Helm installed, cluster running)

---

## What is a Helm Chart?

A Helm chart is a collection of files that describe a set of Kubernetes resources. Think of it as a "package" for Kubernetes applications.

**Analogy:** Like a `.zip` file containing:
- Configuration (values.yaml)
- Templates (Kubernetes YAML with variables)
- Metadata (Chart.yaml)

---

## Chart Directory Structure

```
my-chart/                    # Root folder (chart name)
├── Chart.yaml               # Chart metadata (name, version, etc.)
├── values.yaml              # Default configuration values
└── templates/               # Kubernetes resource templates
    ├── _helpers.tpl         # Reusable template snippets
    ├── deployment.yaml      # Deployment template
    └── service.yaml         # Service template
```

**Why this structure?**
- **Chart.yaml**: Identifies your chart
- **values.yaml**: Separates config from templates (easy to customize)
- **templates/**: Contains Go templates that generate Kubernetes YAML

---

## Step-by-Step: Create Your First Chart

### Step 1: Create Directory Structure

**Command:**
```bash
mkdir -p my-first-chart/templates
```

**Result:**
```
my-first-chart/
└── templates/
```

**Why:** The `templates/` folder is required. Helm looks here for Kubernetes resource definitions.

---

### Step 2: Create Chart.yaml (Chart Metadata)

**File:** `my-first-chart/Chart.yaml`

```yaml
apiVersion: v2
name: my-first-chart
description: A simple Helm chart for learning
type: application
version: 0.1.0
appVersion: "1.0.0"
```

**Field Explanations:**

| Field | Description | Example |
|-------|-------------|---------|
| `apiVersion` | Helm API version (v2 = Helm 3) | `v2` |
| `name` | Chart name (used in commands) | `my-first-chart` |
| `description` | What this chart does | Human-readable text |
| `type` | Chart type: application or library | `application` |
| `version` | **Chart version** (semantic versioning) | `0.1.0` |
| `appVersion` | **Application version** being deployed | `"1.0.0"` |

**Key Distinction:**
- `version` = Chart package version (changes when you update templates)
- `appVersion` = The actual software version (e.g., nginx 1.27)

**Example:**
```yaml
version: 0.2.0      # You updated the chart templates
appVersion: "1.27"  # Still deploying nginx 1.27
```

---

### Step 3: Create values.yaml (Default Configuration)

**File:** `my-first-chart/values.yaml`

```yaml
# Default values for my-first-chart
# This is a YAML-formatted file.

# Application configuration
replicaCount: 1

image:
  repository: nginx
  tag: "1.27"
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 80

# Resource limits (optional)
resources: {}
  # limits:
  #   cpu: 100m
  #   memory: 128Mi
  # requests:
  #   cpu: 100m
  #   memory: 128Mi
```

**What each value does:**

| Value Path | Default | Purpose |
|------------|---------|---------|
| `replicaCount` | 1 | Number of pod replicas |
| `image.repository` | nginx | Docker image name |
| `image.tag` | "1.27" | Image version |
| `image.pullPolicy` | IfNotPresent | When to pull image |
| `service.type` | ClusterIP | Service exposure type |
| `service.port` | 80 | Service port |

**Why use values.yaml?**
- ✅ **Customization**: Users can override without editing templates
- ✅ **Reusability**: Same chart, different values = different deployments
- ✅ **Environment separation**: dev/values.yaml, prod/values.yaml

**Override examples:**
```bash
# Override single value
helm install myapp . --set replicaCount=3

# Override nested value
helm install myapp . --set image.tag="1.28"

# Use custom values file
helm install myapp . -f prod-values.yaml
```

---

### Step 4: Create _helpers.tpl (Template Helpers)

**File:** `my-first-chart/templates/_helpers.tpl`

```yaml
{{/*
Expand the name of the chart.
*/}}
{{- define "my-first-chart.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "my-first-chart.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "my-first-chart.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "my-first-chart.labels" -}}
helm.sh/chart: {{ include "my-first-chart.chart" . }}
{{ include "my-first-chart.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "my-first-chart.selectorLabels" -}}
app.kubernetes.io/name: {{ include "my-first-chart.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
```

**Why _helpers.tpl?**
- Starts with `_` so Helm doesn't render it as a Kubernetes resource
- Contains reusable "template functions"
- Ensures consistent naming and labeling

**Template Functions Explained:**

| Function | Purpose | Example Output |
|----------|---------|----------------|
| `my-first-chart.name` | Chart name | `my-first-chart` |
| `my-first-chart.fullname` | Full release name (release + chart) | `myapp-my-first-chart` |
| `my-first-chart.chart` | Chart name and version | `my-first-chart-0.1.0` |
| `my-first-chart.labels` | All standard K8s labels | Label set |
| `my-first-chart.selectorLabels` | Labels for pod selection | Selector set |

**Built-in Objects Available in Templates:**

| Object | Contains | Example |
|--------|----------|---------|
| `.Chart` | Chart.yaml values | `.Chart.Name`, `.Chart.Version` |
| `.Values` | values.yaml values | `.Values.replicaCount` |
| `.Release` | Release info | `.Release.Name`, `.Release.Namespace` |
| `.Template` | Template info | `.Template.Name` |

**Template Syntax:**

```yaml
{{/* This is a comment */}}

{{- define "name" -}}     # Define a reusable template
  template content
{{- end }}                 # End definition

{{ include "name" . }}    # Call a template (pass context ".")

{{ .Values.key }}         # Access a value

{{ .Chart.Name }}         # Access chart metadata

{{ .Release.Name }}       # Access release name

{{- ... }}                # {{- trims whitespace BEFORE
{{ ... -}}                # -}} trims whitespace AFTER

{{ value | quote }}       # Pipe to filter (add quotes)
{{ value | trunc 63 }}    # Truncate to 63 characters
{{ value | nindent 4 }}   # Add newline + 4 spaces indent
```

**The Magic of fullname:**

When you install:
```bash
helm install my-web-app .
```

The fullname helper generates:
```
my-web-app-my-first-chart
```

If you install again with different name:
```bash
helm install my-api .
```

It generates:
```
my-api-my-first-chart
```

**This ensures unique resource names for each release!**

---

### Step 5: Create deployment.yaml (Main Template)

**File:** `my-first-chart/templates/deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "my-first-chart.fullname" . }}
  labels:
    {{- include "my-first-chart.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "my-first-chart.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "my-first-chart.selectorLabels" . | nindent 8 }}
    spec:
      containers:
      - name: {{ .Chart.Name }}
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
        imagePullPolicy: {{ .Values.image.pullPolicy }}
        ports:
        - name: http
          containerPort: 80
          protocol: TCP
```

**Line-by-Line Breakdown:**

```yaml
name: {{ include "my-first-chart.fullname" . }}
```
- Calls the helper template
- Generates unique name based on release name
- Example: `myapp-my-first-chart`

```yaml
labels:
  {{- include "my-first-chart.labels" . | nindent 4 }}
```
- Includes all standard labels
- `nindent 4` = Add newline + 4 spaces (proper YAML indentation)

```yaml
replicas: {{ .Values.replicaCount }}
```
- Reads from values.yaml
- Generates: `replicas: 1` (or whatever value you set)

```yaml
selector:
  matchLabels:
    {{- include "my-first-chart.selectorLabels" . | nindent 6 }}
```
- Tells Deployment which pods it manages
- Must match the pod template labels!

```yaml
image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
```
- Combines repository and tag
- Generates: `nginx:1.27`

**⚠️ VSCode may show red errors:** This is normal! YAML validators don't understand Go template syntax (`{{ }}`). Helm processes this correctly.

---

### Step 6: Create service.yaml (Service Template)

**File:** `my-first-chart/templates/service.yaml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ include "my-first-chart.fullname" . }}
  labels:
    {{- include "my-first-chart.labels" . | nindent 4 }}
spec:
  type: {{ .Values.service.type }}
  ports:
  - port: {{ .Values.service.port }}
    targetPort: http
    protocol: TCP
    name: http
  selector:
    {{- include "my-first-chart.selectorLabels" . | nindent 4 }}
```

**Key Points:**

```yaml
name: {{ include "my-first-chart.fullname" . }}
```
- Uses same name as Deployment
- Creates: `myapp-my-first-chart`

```yaml
selector:
  {{- include "my-first-chart.selectorLabels" . | nindent 4 }}
```
- **CRITICAL:** Must match Deployment's selector labels
- This connects the Service to the Pods

**How it works:**
```
┌─────────────────┐
│ Service         │  Port 80
│  (ClusterIP)    │
└────────┬────────┘
         │ selector labels
         ▼
┌─────────────────┐
│ Deployment      │  Manages pods with these labels
│                 │
└────────┬────────┘
         │ creates
         ▼
┌─────────────────┐
│ Pods            │  nginx containers
│                 │
└─────────────────┘
```

---

## Complete Chart Structure

```
my-first-chart/
├── Chart.yaml                 # Chart metadata
├── values.yaml                # Default configuration
└── templates/
    ├── _helpers.tpl           # Reusable template functions
    ├── deployment.yaml        # Deployment resource
    └── service.yaml           # Service resource
```

---

## Testing Your Chart

### Step 1: Lint (Check for Errors)

```bash
cd my-first-chart
~/bin/helm.exe lint
```

**Expected output:**
```
==> Linting .
[INFO] Chart.yaml: icon is recommended

1 chart(s) linted, 0 chart(s) failed
```

### Step 2: Dry Run (See Generated YAML)

```bash
~/bin/helm.exe template my-release .
```

**What it does:**
- Processes all templates
- Shows final Kubernetes YAML
- Does NOT deploy to cluster

**Example output:**
```yaml
---
# Source: my-first-chart/templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-release-my-first-chart
  labels:
    helm.sh/chart: my-first-chart-0.1.0
    app.kubernetes.io/name: my-first-chart
    app.kubernetes.io/instance: my-release
    ...
spec:
  replicas: 1
  selector:
    matchLabels:
      app.kubernetes.io/name: my-first-chart
      app.kubernetes.io/instance: my-release
  template:
    metadata:
      labels:
        app.kubernetes.io/name: my-first-chart
        app.kubernetes.io/instance: my-release
    spec:
      containers:
      - name: my-first-chart
        image: "nginx:1.27"
        imagePullPolicy: IfNotPresent
        ports:
        - name: http
          containerPort: 80
          protocol: TCP
```

### Step 3: Install the Chart

```bash
~/bin/helm.exe install myapp .
```

**What happens:**
- Creates a "release" named "myapp"
- Generates YAML from templates
- Applies to Kubernetes cluster
- Tracks as revision 1

**Expected output:**
```
NAME: myapp
LAST DEPLOYED: Sun Feb 8 10:45:00 2026
NAMESPACE: default
STATUS: deployed
REVISION: 1
```

### Step 4: Verify Installation

```bash
# Check Helm release
~/bin/helm.exe list

# Check Kubernetes resources
kubectl get all | grep myapp

# See generated values
~/bin/helm.exe get values myapp
```

### Step 5: Upgrade with Custom Values

```bash
# Upgrade with different replica count
~/bin/helm.exe upgrade myapp . --set replicaCount=3

# Or create a custom values file
cat > custom-values.yaml << EOF
replicaCount: 3
image:
  tag: "1.28"
service:
  type: NodePort
EOF

~/bin/helm.exe upgrade myapp . -f custom-values.yaml
```

### Step 6: Rollback

```bash
# See history
~/bin/helm.exe history myapp

# Rollback to revision 1
~/bin/helm.exe rollback myapp 1
```

### Step 7: Clean Up

```bash
# Uninstall release
~/bin/helm.exe uninstall myapp

# Verify cleanup
kubectl get all | grep myapp
```

---

## Advanced Templating Examples

### Example 1: Conditional Resources

```yaml
# In values.yaml
ingress:
  enabled: true
  host: myapp.example.com
```

```yaml
# In templates/ingress.yaml
{{- if .Values.ingress.enabled }}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{ include "my-first-chart.fullname" . }}
spec:
  rules:
  - host: {{ .Values.ingress.host }}
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: {{ include "my-first-chart.fullname" . }}
            port:
              number: 80
{{- end }}
```

### Example 2: Loops

```yaml
# In values.yaml
env:
  - name: DB_HOST
    value: postgres
  - name: DB_PORT
    value: "5432"
```

```yaml
# In templates/deployment.yaml
env:
{{- range .Values.env }}
  - name: {{ .name }}
    value: {{ .value | quote }}
{{- end }}
```

**Generates:**
```yaml
env:
  - name: DB_HOST
    value: "postgres"
  - name: DB_PORT
    value: "5432"
```

### Example 3: Default Values

```yaml
# Use default if value not set
replicas: {{ .Values.replicaCount | default 1 }}

# Use default with quote
name: {{ .Values.service.name | default "my-service" | quote }}
```

### Example 4: Variables

```yaml
{{- $fullname := include "my-first-chart.fullname" . -}}
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ $fullname }}-config
```

---

## Best Practices

### 1. Always Use Helper Templates
- Ensures consistent naming
- Prevents name collisions
- Follows Kubernetes conventions

### 2. Structure Your values.yaml
```yaml
# Good: Hierarchical structure
image:
  repository: nginx
  tag: "1.27"
  pullPolicy: IfNotPresent

# Bad: Flat structure
imageRepository: nginx
imageTag: "1.27"
imagePullPolicy: IfNotPresent
```

### 3. Use Comments
```yaml
# Number of pod replicas
replicaCount: 1

# Image configuration
image:
  # Docker repository
  repository: nginx
  # Image tag
  tag: "1.27"
```

### 4. Validate Required Values
```yaml
{{- if not .Values.requiredValue }}
{{- fail ".Values.requiredValue is required" }}
{{- end }}
```

### 5. Use nindent Carefully
```yaml
# Good: nindent adds newline + spaces
labels:
  {{- include "labels" . | nindent 4 }}

# Result:
labels:
  app: myapp
  version: 1.0

# Bad: wrong indentation
labels:
  {{- include "labels" . }}

# Result (invalid YAML):
labels:  app: myapp
  version: 1.0
```

---

## Common Commands Reference

| Command | Purpose |
|---------|---------|
| `helm create mychart` | Create new chart skeleton |
| `helm lint ./mychart` | Check chart for errors |
| `helm template myrelease ./mychart` | Render templates (dry run) |
| `helm install myrelease ./mychart` | Install chart |
| `helm upgrade myrelease ./mychart` | Upgrade release |
| `helm rollback myrelease 1` | Rollback to revision 1 |
| `helm list` | Show all releases |
| `helm history myrelease` | Show release history |
| `helm get values myrelease` | Show deployed values |
| `helm get manifest myrelease` | Show deployed YAML |
| `helm uninstall myrelease` | Delete release |

---

## Troubleshooting

### Problem: "Error: failed to download chart"
**Solution:** Make sure you're in the chart directory or use full path:
```bash
cd my-first-chart
helm install myapp .
# OR
helm install myapp ./my-first-chart
```

### Problem: "Error: parse error"
**Solution:** Check template syntax:
- Ensure `{{` and `}}` are balanced
- Check for missing quotes around strings
- Verify indentation with `nindent`

### Problem: Generated YAML has wrong indentation
**Solution:**
- Use `nindent N` instead of `indent N` (adds newline)
- Check the number of spaces matches YAML structure

### Problem: Service can't find pods
**Solution:**
- Ensure Service selector matches Deployment labels
- Check that `selectorLabels` helper is used consistently

---

## What You Learned in Stage 2

✅ **Chart Structure:** Chart.yaml, values.yaml, templates/  
✅ **Templating:** Go template syntax with Helm functions  
✅ **Built-in Objects:** .Chart, .Values, .Release  
✅ **Helper Templates:** Reusable naming and labeling  
✅ **Testing:** lint, template, dry-run, install  
✅ **Customization:** Overriding values with --set and -f  
✅ **Best Practices:** Structure, comments, validation

---

## Next Steps

Ready for **Stage 3: Advanced Helm Features**?

You'll learn:
- Helm dependencies (subcharts)
- Helm hooks
- Chart packaging and repositories
- Advanced templating patterns

Or practice more by:
- Adding ConfigMap and Secret templates
- Creating an Ingress template
- Adding resource limits and probes
- Packaging your chart with `helm package`

---

**Created:** 2026-02-08  
**Location:** `doc/stage2-first-custom-chart.md`
