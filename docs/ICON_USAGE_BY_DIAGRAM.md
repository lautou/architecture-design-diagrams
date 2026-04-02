# Icon Usage by Diagram

This document provides a detailed breakdown of which Red Hat custom icons are used in each baseline diagram.

## 01-core-infrastructure.py

### Red Hat Custom Icons (6)
- DNS Operator → `operator/Technology_icon-Red_Hat-operator`
- OLM → `operator/Technology_icon-Red_Hat-operator`
- NFD Operator → `operator/Technology_icon-Red_Hat-operator`
- NVIDIA GPU Operator → `operator/Technology_icon-Red_Hat-operator`
- ODF Operator → `operator/Technology_icon-Red_Hat-operator`

### Standard Library Icons
- APIServer, ControllerManager, Scheduler (K8s control plane)
- Etcd (distributed storage)
- Nginx (load balancer)
- Ceph (storage)
- Server (DNS, network, registry, OAuth, machine API, GPU nodes)
- Ingress (router)
- Node (worker nodes)
- Users (users/developers)

## 02-observability-stack.py

### Red Hat Custom Icons (7)
- Logging Operator → `operator/Technology_icon-Red_Hat-operator`
- Tempo Operator → `operator/Technology_icon-Red_Hat-operator`
- OpenTelemetry Operator → `Red Hat build of OpenTelemetry/Technology_icon-Red_Hat-OpenTelemetry`
- Cluster Observability Operator → `Cluster observability/Technology_icon-Red_Hat-Cluster_observability_operator`
- Network Observability Operator → `operator/Technology_icon-Red_Hat-operator`
- Grafana Operator → `operator/Technology_icon-Red_Hat-operator`

### Standard Library Icons
- APIServer (OCP API)
- Prometheus (cluster & UDWM)
- Grafana (custom dashboards)
- Loki (log storage)
- Jaeger (OTel collector, Tempo)
- Clickhouse (flow collector)
- Server (platform apps, user apps, external storage, external SIEM)

## 03-developer-cicd-stack.py

### Red Hat Custom Icons (6)
- GitOps Operator → `Red Hat OpenShift GitOps/Technology_icon-Red_Hat-OpenShift_GitOps`
- ArgoCD Server → `Red Hat OpenShift GitOps/Technology_icon-Red_Hat-OpenShift_GitOps`
- Pipelines Operator → `Red Hat OpenShift Pipelines/Technology_icon-Red_Hat-OpenShift_Pipelines`
- Tekton Pipeline → `Red Hat OpenShift Pipelines/Technology_icon-Red_Hat-OpenShift_Pipelines`
- Builds Operator → `Builds for Red Hat OpenShift/Technology_icon-Red_Hat-OpenShift_Builds`
- DevWorkspace Operator → `operator/Technology_icon-Red_Hat-operator`
- Web Terminal Operator → `operator/Technology_icon-Red_Hat-operator`

### Standard Library Icons
- APIServer (OCP API)
- Users (developer, platform engineer)
- Github/Gitlab (source repos)
- Server (ArgoCD apps, event listener, pipeline runs, build strategies, registry, applications, external registry)
- Python (cloud IDE, web terminal)

## 04-security-servicemesh-stack.py

### Red Hat Custom Icons (8)
- Keycloak Operator → `Red Hat build of Keycloak/Technology_icon-Red_Hat-Keycloak`
- Keycloak Server → `Red Hat build of Keycloak/Technology_icon-Red_Hat-Keycloak`
- Authorino Operator → `operator/Technology_icon-Red_Hat-operator`
- cert-manager Operator → `operator/Technology_icon-Red_Hat-operator`
- Service Mesh Operator → `Red Hat OpenShift Service Mesh/Technology_icon-Red_Hat-OpenShift_Service_Mesh`
- Istiod → `Red Hat OpenShift Service Mesh/Technology_icon-Red_Hat-OpenShift_Service_Mesh`
- Limitador Operator → `operator/Technology_icon-Red_Hat-operator`
- Connectivity Link Operator → `Red Hat Connectivity Link/Technology_icon-Red_Hat-Connectivity_Link`
- Skupper → `Red Hat Connectivity Link/Technology_icon-Red_Hat-Connectivity_Link`

### Standard Library Icons
- APIServer (OCP API)
- Ingress (router)
- Users (end users)
- Vault (Keycloak realms, Authorino service, cert issuers, cert-manager controller, enterprise PKI)
- Server (corporate IDP, mesh features, Limitador service, applications, remote services, Tempo/Jaeger)

## rhoai/functional-components.py

### Red Hat Custom Icons (10)
- RHOAI Operator → `Red Hat AI/Technology_icon-Red_Hat-AI`
- Data Science Pipelines Operator → `operator/Technology_icon-Red_Hat-operator`
- KServe Operator → `operator/Technology_icon-Red_Hat-operator`
- TrustyAI Operator → `operator/Technology_icon-Red_Hat-operator`
- Model Registry Operator → `operator/Technology_icon-Red_Hat-operator`
- Notebook Controller → `operator/Technology_icon-Red_Hat-operator`
- KubeRay Operator → `operator/Technology_icon-Red_Hat-operator`
- Training Operator → `operator/Technology_icon-Red_Hat-operator`
- Kueue Operator → `operator/Technology_icon-Red_Hat-operator`
- Model Registry → `AI model/Technology_icon-Red_Hat-AI_model`

### Standard Library Icons
- APIServer (OCP API)
- Ingress (router)
- Users (data scientist, MLOps engineer)
- Github (Git repository)
- PostgreSQL (external DB)
- Ceph (S3 storage, PVCs)
- Python (dashboard, workbenches, TrustyAI service, pipeline runs, training jobs, Ray cluster)
- Server (corporate IDP, pipeline server, model serving, accelerator profiles, GPU nodes)
- Prometheus (data science monitoring stack)

## Icon Distribution Summary

### By Icon Type

| Icon Type | Count | Usage |
|-----------|-------|-------|
| Red Hat AI | 1 | RHOAI main operator |
| Red Hat OpenShift GitOps | 2 | GitOps operator, ArgoCD |
| Red Hat OpenShift Pipelines | 2 | Pipelines operator, Tekton |
| Red Hat build of Keycloak | 2 | Keycloak operator, server |
| Red Hat OpenShift Service Mesh | 2 | Service Mesh operator, Istiod |
| Builds for Red Hat OpenShift | 1 | Builds operator |
| Red Hat build of OpenTelemetry | 1 | OTel operator |
| Cluster observability | 1 | Cluster observability operator |
| Red Hat Connectivity Link | 2 | Connectivity operator, Skupper |
| AI model | 1 | Model registry |
| Generic operator | 22 | All other operators |

**Total Red Hat Icons**: 37 across all baseline diagrams

### By Diagram

| Diagram | Red Hat Icons | Standard Icons |
|---------|---------------|----------------|
| 01-core-infrastructure | 6 | 14 |
| 02-observability-stack | 7 | 11 |
| 03-developer-cicd-stack | 6 | 10 |
| 04-security-servicemesh-stack | 8 | 9 |
| rhoai/functional-components | 10 | 14 |

## Icon Path Format

All Red Hat custom icons follow this consistent path format:

```
custom_icons/Technology icons/{Category}/Technology_icon-Red_Hat-{Name}-Standard-RGB.Large_icon_transparent.png
```

Where:
- `{Category}` = Icon category directory name
- `{Name}` = Product/component name
- `Standard-RGB` = Color variant (using standard colors)
- `Large_icon_transparent` = Size variant (using large with transparent background)
