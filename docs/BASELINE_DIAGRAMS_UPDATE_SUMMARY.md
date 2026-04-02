# Baseline Diagrams Update Summary

## Overview

All 5 baseline diagrams have been successfully updated to use Red Hat Technology icons from the `custom_icons/Technology icons/` directory.

## Updated Diagrams

### OpenShift Container Platform Baseline Diagrams

1. **01-core-infrastructure.py** - Core Infrastructure Layer
   - Updated 6 operator icons to use Red Hat custom icons
   - Kept K8s control plane, etcd, storage, and compute icons

2. **02-observability-stack.py** - Observability Stack
   - Updated 7 operator icons to use Red Hat custom icons
   - Kept Prometheus, Grafana, Loki, Jaeger, and Clickhouse icons

3. **03-developer-cicd-stack.py** - Developer & CI/CD Stack
   - Updated 6 operator icons to use Red Hat custom icons
   - Kept Github, Gitlab, Python, and User icons

4. **04-security-servicemesh-stack.py** - Security & Service Mesh Stack
   - Updated 8 operator icons to use Red Hat custom icons
   - Kept Vault, Users, and Ingress icons

### RHOAI Baseline Diagram

5. **functional-components.py** - RHOAI Functional Components
   - Updated 10 operator icons to use Red Hat custom icons
   - Updated model registry to use AI model icon
   - Kept PostgreSQL, Github, Ceph, Python, Users, and Prometheus icons

## Red Hat Icons Used

### Product-Specific Icons

| Icon | Path | Components |
|------|------|------------|
| Red Hat AI | `Red Hat AI/Technology_icon-Red_Hat-AI-Standard-RGB.Large_icon_transparent.png` | RHOAI Operator |
| Red Hat OpenShift GitOps | `Red Hat OpenShift GitOps/Technology_icon-Red_Hat-OpenShift_GitOps-Standard-RGB.Large_icon_transparent.png` | GitOps Operator, ArgoCD Server |
| Red Hat OpenShift Pipelines | `Red Hat OpenShift Pipelines/Technology_icon-Red_Hat-OpenShift_Pipelines-Standard-RGB.Large_icon_transparent.png` | Pipelines Operator, Tekton Pipeline |
| Red Hat build of Keycloak | `Red Hat build of Keycloak/Technology_icon-Red_Hat-Keycloak-Standard-RGB.Large_icon_transparent.png` | Keycloak Operator, Keycloak Server |
| Red Hat OpenShift Service Mesh | `Red Hat OpenShift Service Mesh/Technology_icon-Red_Hat-OpenShift_Service_Mesh-Standard-RGB.Large_icon_transparent.png` | Service Mesh Operator, Istiod |
| Builds for Red Hat OpenShift | `Builds for Red Hat OpenShift/Technology_icon-Red_Hat-OpenShift_Builds-Standard-RGB.Large_icon_transparent.png` | Builds Operator |
| Red Hat build of OpenTelemetry | `Red Hat build of OpenTelemetry/Technology_icon-Red_Hat-OpenTelemetry-Standard-RGB.Large_icon_transparent.png` | OpenTelemetry Operator |
| Cluster observability | `Cluster observability/Technology_icon-Red_Hat-Cluster_observability_operator-Standard-RGB.Large_icon_transparent.png` | Cluster Observability Operator |
| Red Hat Connectivity Link | `Red Hat Connectivity Link/Technology_icon-Red_Hat-Connectivity_Link-Standard-RGB.Large_icon_transparent.png` | Connectivity Link Operator, Skupper |
| AI model | `AI model/Technology_icon-Red_Hat-AI_model-Standard-RGB.Large_icon_transparent.png` | Model Registry |

### Generic Operator Icon

| Icon | Path | Components |
|------|------|------------|
| operator | `operator/Technology_icon-Red_Hat-operator-Standard-RGB.Large_icon_transparent.png` | All generic operators: OLM, DNS, GPU, NFD, ODF, Logging, Tempo, Grafana, Network Observability, cert-manager, Limitador, Authorino, DevWorkspace, Web Terminal, DSP, KServe, TrustyAI, Model Registry Operator, Notebook Controller, KubeRay, Training Operator, Kueue |

## Total Icon Updates

- **OCP Core Infrastructure**: 6 custom icons
- **OCP Observability Stack**: 7 custom icons
- **OCP Developer & CI/CD Stack**: 6 custom icons
- **OCP Security & Service Mesh Stack**: 8 custom icons
- **RHOAI Functional Components**: 10 custom icons

**Total**: 37 components now using Red Hat Technology custom icons

## Icons Retained (Non-Red Hat)

The following icons were intentionally kept as standard diagrams library icons:

### Kubernetes Components
- APIServer, ControllerManager, Scheduler, Etcd
- Node, Ingress

### Infrastructure
- Ceph (storage), PostgreSQL/MariaDB (databases)
- Nginx (load balancer), Server (generic compute)

### Monitoring & Observability
- Prometheus, Grafana, Loki, Jaeger, Tempo, Clickhouse

### External Systems
- Github, Gitlab (version control)
- Vault (generic security, kept for non-Keycloak uses)

### User Representations
- Users (personas)
- Python (for workbenches, notebooks, scripts)

## Testing Results

All 5 baseline diagrams were successfully generated:

```
✓ baseline-ocp-01-core-infrastructure.png (434K)
✓ baseline-ocp-02-observability-stack.png (318K)
✓ baseline-ocp-03-developer-cicd-stack.png (355K)
✓ baseline-ocp-04-security-servicemesh-stack.png (376K)
✓ baseline-rhoai-functional-components.png (422K)
```

File sizes increased compared to previous versions, confirming that PNG custom icons are being used instead of simple SVG shapes.

## Code Changes

Each updated diagram now includes:

```python
from diagrams.custom import Custom
```

And operators use the Custom() function:

```python
operator = Custom("Operator Name", "custom_icons/Technology icons/{Category}/{Icon}-Standard-RGB.Large_icon_transparent.png")
```

## Documentation

Created two reference documents:

1. **RED_HAT_ICON_MAPPING.md** - Complete mapping of components to Red Hat icons
2. **BASELINE_DIAGRAMS_UPDATE_SUMMARY.md** - This summary document

## Next Steps

For future diagram updates or new diagrams:

1. Refer to `docs/RED_HAT_ICON_MAPPING.md` for icon mappings
2. Use Standard-RGB variant with Large_icon_transparent size for consistency
3. Use product-specific icons where available
4. Fall back to generic "operator" icon for operators without specific Red Hat product icons
5. Keep infrastructure, external systems, and K8s control plane icons as standard diagrams library icons
