# Baseline Reference Diagrams

These diagrams serve as **reusable building blocks** for customer engagements. They show the complete component stack without customer-specific customizations.

## Purpose

- **Reference architecture** - Shows all available components and operators
- **Learning tool** - Helps understand the full platform capabilities
- **Starting point** - Copy and adapt for customer-specific diagrams
- **Documentation** - Component relationships and integration points

## Structure

### OpenShift Container Platform (OCP) - 4 Layered Diagrams

#### 01 - Core Infrastructure
**File:** `ocp/01-core-infrastructure.py`
**Shows:**
- Control Plane (API Server, Scheduler, Controller Manager, etcd)
- Worker Nodes (Standard CPU and GPU compute)
- OpenShift Data Foundation (ODF) with storage classes
- Node Feature Discovery and NVIDIA GPU Operator
- Machine API and autoscaling
- Integration points: Load Balancer, DNS, External Storage

**Use when:** Discussing cluster architecture, compute resources, storage strategy

#### 02 - Observability Stack
**File:** `ocp/02-observability-stack.py`
**Shows:**
- **Embedded Monitoring:** Cluster Monitoring, User Defined Workload Monitoring (UDWM)
- **Add-on Operators:** Logging, OpenTelemetry, Tempo, Network Observability, Grafana
- Metrics, logs, and traces data flows
- Integration with external SIEM and storage

**Use when:** Discussing monitoring, logging, compliance, observability requirements

#### 03 - Developer & CI/CD Stack
**File:** `ocp/03-developer-cicd-stack.py`
**Shows:**
- OpenShift GitOps (ArgoCD) for continuous delivery
- OpenShift Pipelines (Tekton) for continuous integration
- Builds for OpenShift (Shipwright) - S2I, Buildah, Buildpacks
- Developer Workspaces (DevWorkspace Operator, Web Terminal)
- Internal and external image registries
- Git integration and image promotion flows

**Use when:** Discussing developer experience, CI/CD pipelines, GitOps, build strategies

#### 04 - Security & Service Mesh Stack
**File:** `ocp/04-security-servicemesh-stack.py`
**Shows:**
- Identity & Access: Keycloak (SSO), Authorino (API security)
- Certificate Management: cert-manager with CA and ACME issuers
- Service Mesh: Istio-based mesh with mTLS, traffic management, observability
- Rate Limiting: Limitador Operator
- Connectivity: Red Hat Connectivity Link for hybrid cloud
- Integration with external IDP and PKI

**Use when:** Discussing security, zero-trust architecture, service mesh, hybrid connectivity

### Red Hat OpenShift AI (RHOAI) - Single Comprehensive Diagram

#### RHOAI Functional Components
**File:** `rhoai/functional-components.py`
**Shows all DataScienceCluster CR components:**
- **UI:** RHOAI Dashboard
- **Development:** Workbenches (JupyterLab, VSCode, RStudio)
- **Pipelines:** Data Science Pipelines (Kubeflow, Elyra)
- **Training:** Training Operator (PyTorch, TensorFlow, XGBoost, MPI)
- **Distributed Computing:** Ray, CodeFlare
- **Scheduling:** Kueue (job queuing and resource management)
- **Serving:** KServe (single model), ModelMesh (multi-model)
- **Registry:** Model Registry for versioning and artifacts
- **Governance:** TrustyAI (explainability, fairness, monitoring)
- **Accelerators:** GPU/TPU profiles
- Integration points: IDP, Git, S3, Databases, Monitoring

**Use when:** Explaining RHOAI platform capabilities, ML workflows, AI/ML architecture

## How to Use These Diagrams

### 1. As Reference Material
Review these diagrams to understand the complete platform stack:
```bash
# Generate all baseline diagrams
./venv/bin/python3 diagrams/baseline-reference/ocp/01-core-infrastructure.py
./venv/bin/python3 diagrams/baseline-reference/ocp/02-observability-stack.py
./venv/bin/python3 diagrams/baseline-reference/ocp/03-developer-cicd-stack.py
./venv/bin/python3 diagrams/baseline-reference/ocp/04-security-servicemesh-stack.py
./venv/bin/python3 diagrams/baseline-reference/rhoai/functional-components.py
```

### 2. As Starting Points for Custom Diagrams
Copy a baseline diagram and adapt for customer needs:
```bash
# Example: Create customer-specific observability diagram
cp diagrams/baseline-reference/ocp/02-observability-stack.py \
   diagrams/engagement-ai-platform/01-production/observability-prod.py

# Edit to add customer-specific integrations
vim diagrams/engagement-ai-platform/01-production/observability-prod.py
```

### 3. For Customer Presentations
These diagrams can be used directly in customer presentations to:
- Explain platform capabilities
- Show component relationships
- Discuss architecture options
- Demonstrate best practices

### 4. In Documentation
Reference these diagrams in architecture decision records (ADRs), runbooks, or technical documentation.

## Key Principles

1. **No Pod-level representation** - Focus on operators, services, and logical components
2. **Integration-focused** - Highlight integration points with external systems
3. **Generic and adaptable** - No customer-specific configurations
4. **Complete platform view** - Show all available components

## Customization Guidance

When adapting for customer engagements:

- **Remove components** the customer won't use
- **Add customer-specific** integration points (specific IDP, storage vendor, etc.)
- **Adjust sizing** annotations (HA configurations, node counts)
- **Change labels** to match customer terminology
- **Add security zones** if customer has specific network segmentation
- **Include compliance** annotations if required

## Notes

- These diagrams represent the **complete platform capability**
- Not all components may be deployed in every environment
- Use the engagement-specific diagrams to show actual customer deployments
- Update these baselines as new operators/features become available

## Related Documentation

- **Engagement Diagrams:** `../engagement-ai-platform/` - Customer-specific adaptations
- **Examples:** `../openshift/`, `../rhoai/` - Original example diagrams
- **Templates:** `../../templates/` - Blank diagram templates
