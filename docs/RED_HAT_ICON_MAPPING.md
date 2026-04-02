# Red Hat Technology Icon Mapping for Baseline Diagrams

This document maps components in the baseline diagrams to Red Hat Technology icons from the `custom_icons/Technology icons/` directory.

## Icon Usage Convention

All Red Hat icons use the Standard-RGB variant with Large_icon_transparent size:
```python
Custom("Component Name", "custom_icons/Technology icons/{Category}/{Icon}-Standard-RGB.Large_icon_transparent.png")
```

## Component-to-Icon Mappings

### OpenShift Core Components

| Component | Icon Category | Icon Name | Usage |
|-----------|--------------|-----------|--------|
| Red Hat OpenShift AI Operator | Red Hat AI | Technology_icon-Red_Hat-AI | RHOAI main operator |
| GitOps Operator / ArgoCD | Red Hat OpenShift GitOps | Technology_icon-Red_Hat-OpenShift_GitOps | GitOps components |
| Pipelines Operator / Tekton | Red Hat OpenShift Pipelines | Technology_icon-Red_Hat-OpenShift_Pipelines | Pipeline components |
| Keycloak Operator / Keycloak Server | Red Hat build of Keycloak | Technology_icon-Red_Hat-Keycloak | Identity management |
| Service Mesh Operator / Istiod | Red Hat OpenShift Service Mesh | Technology_icon-Red_Hat-OpenShift_Service_Mesh | Service mesh components |
| Builds Operator | Builds for Red Hat OpenShift | Technology_icon-Red_Hat-OpenShift_Builds | Shipwright builds |
| OpenTelemetry Operator | Red Hat build of OpenTelemetry | Technology_icon-Red_Hat-OpenTelemetry | OTel collector |
| Cluster Observability Operator | Cluster observability | Technology_icon-Red_Hat-Cluster_observability_operator | Observability operator |
| Connectivity Link / Skupper | Red Hat Connectivity Link | Technology_icon-Red_Hat-Connectivity_Link | Hybrid connectivity |

### RHOAI Components

| Component | Icon Category | Icon Name | Usage |
|-----------|--------------|-----------|--------|
| RHOAI Operator | Red Hat AI | Technology_icon-Red_Hat-AI | Main RHOAI operator |
| AI model components | AI model | Technology_icon-Red_Hat-AI_model | Model registry, serving |
| Data Science Pipelines Operator | operator | Technology_icon-Red_Hat-operator | DSP operator |
| KServe Operator | operator | Technology_icon-Red_Hat-operator | KServe controller |
| TrustyAI Operator | operator | Technology_icon-Red_Hat-operator | TrustyAI operator |
| Model Registry Operator | operator | Technology_icon-Red_Hat-operator | Model registry operator |
| Notebook Controller | operator | Technology_icon-Red_Hat-operator | Notebook controller |
| KubeRay Operator | operator | Technology_icon-Red_Hat-operator | Ray operator |
| Training Operator | operator | Technology_icon-Red_Hat-operator | Kubeflow training |
| Kueue Operator | operator | Technology_icon-Red_Hat-operator | Kueue operator |

### Generic Operators

| Component | Icon Category | Icon Name | Usage |
|-----------|--------------|-----------|--------|
| Generic operators | operator | Technology_icon-Red_Hat-operator | OLM, DNS, Network operators |
| ODF Operator | operator | Technology_icon-Red_Hat-operator | Storage operator |
| GPU Operator | operator | Technology_icon-Red_Hat-operator | NVIDIA GPU operator |
| NFD Operator | operator | Technology_icon-Red_Hat-operator | Node Feature Discovery |
| Logging Operator | operator | Technology_icon-Red_Hat-operator | Logging operator |
| Tempo Operator | operator | Technology_icon-Red_Hat-operator | Tempo operator |
| Grafana Operator | operator | Technology_icon-Red_Hat-operator | Grafana operator |
| Network Observability Operator | operator | Technology_icon-Red_Hat-operator | Network observability |
| cert-manager Operator | operator | Technology_icon-Red_Hat-operator | Certificate management |
| Limitador Operator | operator | Technology_icon-Red_Hat-operator | Rate limiting |
| Authorino Operator | operator | Technology_icon-Red_Hat-operator | API authorization |
| DevWorkspace Operator | operator | Technology_icon-Red_Hat-operator | Developer workspace |
| Web Terminal Operator | operator | Technology_icon-Red_Hat-operator | Web terminal |

## Icons to Keep (Non-Red Hat)

These components use standard diagrams library icons as there are no Red Hat equivalents or they represent external/infrastructure components:

### Kubernetes Control Plane
- APIServer (diagrams.k8s.controlplane)
- ControllerManager (diagrams.k8s.controlplane)
- Scheduler (diagrams.k8s.controlplane)
- Etcd (diagrams.onprem.network)

### Infrastructure
- Ceph storage components (diagrams.onprem.storage.Ceph)
- PostgreSQL / MariaDB (diagrams.onprem.database.PostgreSQL)
- Nginx load balancer (diagrams.onprem.network.Nginx)
- Node / Server compute (diagrams.onprem.compute.Server or diagrams.k8s.infra.Node)

### Monitoring & Observability
- Prometheus (diagrams.onprem.monitoring.Prometheus)
- Grafana (diagrams.onprem.monitoring.Grafana)
- Loki (diagrams.onprem.logging.Loki)
- Jaeger / Tempo (diagrams.onprem.tracing.Jaeger)
- Clickhouse (diagrams.onprem.database.Clickhouse)

### External Systems
- Github / Gitlab (diagrams.onprem.vcs)
- Vault (diagrams.onprem.security.Vault) - for generic secret management
- Users personas (diagrams.onprem.client.Users)
- Python (diagrams.programming.language.Python) - for workbenches, notebooks

### OpenShift Platform
- Ingress / Router (diagrams.k8s.network.Ingress)

## Icon File Paths

All Red Hat technology icons follow this structure:
```
custom_icons/Technology icons/{Category}/Technology_icon-Red_Hat-{Name}-Standard-RGB.Large_icon_transparent.png
```

Examples:
```
custom_icons/Technology icons/Red Hat AI/Technology_icon-Red_Hat-AI-Standard-RGB.Large_icon_transparent.png
custom_icons/Technology icons/Red Hat OpenShift GitOps/Technology_icon-Red_Hat-OpenShift_GitOps-Standard-RGB.Large_icon_transparent.png
custom_icons/Technology icons/operator/Technology_icon-Red_Hat-operator-Standard-RGB.Large_icon_transparent.png
custom_icons/Technology icons/AI model/Technology_icon-Red_Hat-AI_model-Standard-RGB.Large_icon_transparent.png
```

## Import Statement

Add this import to diagrams using custom icons:
```python
from diagrams.custom import Custom
```

## Notes

- Use Standard-RGB variants for consistent color scheme
- Large_icon_transparent provides best visibility in diagrams
- Operators without specific Red Hat product icons use the generic "operator" icon
- External systems and infrastructure components retain original icons for clarity
