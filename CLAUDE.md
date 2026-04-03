# OpenShift Architecture Diagrams - Standards & Conventions

## 🤖 AI Assistant Instructions (Claude Code)

* **Context check:** Read this document carefully before creating or modifying any diagram.
* **Meta-Rule:** Proactively update this `CLAUDE.md` file under the appropriate section if we make a new architectural decision, establish a new naming convention, or solve a recurring bug.
* **Autonomy:** Do not ask for permission to run standard bash commands (like `mkdir`, `touch`, `python`) when scaffolding diagram files, reading the workspace, or running utilities.
* **Code Standard:** Always calculate absolute paths for custom icons using `os.path.abspath(__file__)` at the top of each diagram file.
* **Python Execution:** ALWAYS use `./venv/bin/python3` for ALL Python commands (scripts, one-liners, etc.). NEVER use `source venv/bin/activate && python3` as it triggers security prompts. Examples:
  - Run script: `./venv/bin/python3 diagrams/foo.py`
  - One-liner: `./venv/bin/python3 -c "import diagrams; print(diagrams.__version__)"`
  - Module execution: `./venv/bin/python3 -m pip list`

---

This document defines the standards for creating and maintaining OpenShift and RHOAI architecture diagrams in this repository.

## Diagram Philosophy

### Purpose

These diagrams serve consulting engagements for AI platform deployments. They must:
- Be **adaptable** to different customer contexts
- Show **integration points** with external systems
- Use **namespace-based organization** for customer clarity
- Maintain **visual consistency** across all diagrams

### Guiding Principles

1. **Flexibility Over Prescription** - Provide reference patterns that adapt to customer needs (budget, compliance, team structure), not rigid prescriptions
2. **Namespace-Based Organization** - Group components by actual OpenShift namespaces for customer understanding
3. **Layered Architecture** - Use clear vertical layers (Management → Execution → Infrastructure)
4. **Integration Focus** - Highlight integration points with external systems, not internal implementation details

---

## Diagram Standards

### Representation Rules

**NO pod-level representation** - Focus on:
- Operators (deployed via OLM)
- Logical services and components
- Integration points
- Data flows

**Why:** Pod details clutter diagrams and shift focus from architecture to deployment specifics.

---

## Diagram Organization

### Baseline Reference Diagrams

Location: `diagrams/baseline-reference/`

**OpenShift Container Platform (4 layered diagrams):**

1. **`ocp/01-core-infrastructure.py`**
   - Control plane (openshift-kube-apiserver, openshift-etcd, etc.)
   - Compute (CPU workers, GPU workers)
   - Storage (OpenShift Data Foundation)
   - Networking (DNS, Ingress)

2. **`ocp/02-observability-stack.py`**
   - Embedded: Cluster Monitoring, User Defined Workload Monitoring (UDWM)
   - Add-ons: Logging, OpenTelemetry, Tempo, Network Observability, Grafana

3. **`ocp/03-developer-cicd-stack.py`**
   - GitOps (openshift-gitops)
   - Pipelines (openshift-pipelines)
   - Builds (openshift-builds)
   - Developer Workspaces

4. **`ocp/04-security-servicemesh-stack.py`**
   - Identity: Keycloak, Authorino
   - Certificates: cert-manager
   - Service Mesh: Istio
   - Rate Limiting: Limitador

**Red Hat OpenShift AI (1 comprehensive diagram):**

5. **`rhoai/functional-components.py`**
   - All DataScienceCluster CR components
   - Organized by namespace (redhat-ods-operator, redhat-ods-applications, AI Projects)
   - Shows full ML/AI workflow

**Why layered for OCP?** 22+ operators would be overwhelming in one diagram. Functional layers serve different stakeholder audiences.

**Why comprehensive for RHOAI?** RHOAI is more cohesive as a single product; one diagram shows the complete AI platform capability.

### Engagement-Specific Diagrams

Location: `diagrams/engagement-ai-platform/`

These are **TEMPLATES** to be customized per customer:

```
engagement-ai-platform/
├── 00-overview/               # Environment landscape & cluster topology
├── 01-production/             # Production functional & infrastructure
├── 02-preproduction/          # Pre-prod functional & infrastructure
├── 03-sandbox/                # Sandbox functional & infrastructure
└── common/                    # Shared services & integration patterns
```

**Customization approach:**
- Copy structure: `cp -r diagrams/engagement-ai-platform diagrams/customer-name`
- Adapt to customer specifics: environments, cluster count, sizing, integrations
- Reference baseline diagrams where appropriate (avoid duplication)

**Process diagrams:** Create separately when requested. Do NOT include workflow/pipeline diagrams in baseline architecture work.

---

## Required Component Lists

### OCP Operator Stack (22 operators)

All OCP baseline diagrams must include:

**Security & Identity:**
- cert-manager for Red Hat OpenShift
- Authorino Operator
- Red Hat build of Keycloak

**Service Mesh & Networking:**
- OpenShift Service Mesh
- Red Hat Connectivity Link
- Network Observability
- DNS Operator

**CI/CD & GitOps:**
- OpenShift GitOps
- OpenShift Pipelines
- Builds for Red Hat OpenShift

**Observability:**
- OpenShift Logging
- Red Hat build of OpenTelemetry
- Cluster Observability Operator
- Tempo Operator
- Grafana Operator

**Storage:**
- OpenShift Data Foundation

**Compute & Scheduling (AI/ML):**
- Red Hat build of Kueue
- Red Hat build of Leader Worker Set
- Node Feature Discovery Operator
- NVIDIA GPU Operator

**Developer Experience:**
- DevWorkspace Operator
- Web Terminal

**Rate Limiting:**
- Limitador Operator

**Embedded (Built-in):**
- Cluster Monitoring (Prometheus, Alertmanager)
- User Defined Workload Monitoring (UDWM)

### RHOAI DataScienceCluster Components

All RHOAI diagrams must include components from the DataScienceCluster CR:

**Core:**
- Dashboard (UI)
- Workbenches (JupyterLab, VSCode, RStudio)

**Pipelines & Workflows:**
- Data Science Pipelines (Kubeflow)
- Training Operator (PyTorch, TensorFlow, XGBoost, MPI)

**Distributed Computing:**
- Ray
- CodeFlare

**Resource Management:**
- Kueue (job queuing)

**Model Lifecycle:**
- KServe (single-model serving)
- ModelMesh (multi-model serving)
- Model Registry

**Governance:**
- TrustyAI (explainability, fairness, monitoring)

**Accelerators:**
- Accelerator Profiles (GPU/TPU configuration)

---

## Namespace-Based Organization

**Always organize by actual OpenShift namespaces**, not generic groupings.

### Example: OCP Core Infrastructure

```python
with Cluster("LAYER 1: Control Plane"):
    with Cluster("openshift-kube-apiserver"):
        api = APIServer("API Server")
    
    with Cluster("openshift-etcd"):
        etcd = Etcd("etcd Cluster")
```

### Example: RHOAI

```python
with Cluster("redhat-ods-operator"):
    rhoai_operator = Helm("RHOAI Operator")

with Cluster("redhat-ods-applications"):
    dashboard = Python("Dashboard")
    kserve = Helm("KServe Controller")
```

**Why?** Namespace organization matches how customers actually deploy and manage OpenShift, making diagrams immediately understandable.

---

## Layered Architecture Pattern

Use clear vertical layers inspired by PlantUML conventions:

```python
# LAYER 1: Management & Operators
with Cluster("LAYER 1: Management"):
    operators = ...

# LAYER 2: User Workloads / Execution
with Cluster("LAYER 2: Execution Layer"):
    workloads = ...

# LAYER 3: Infrastructure Dependencies
with Cluster("LAYER 3: Infrastructure"):
    external_systems = ...

# SIDE: Observability (orthogonal concern)
with Cluster("Observability"):
    monitoring = ...
```

**Why?** Clear layers show architectural hierarchy and separation of concerns.

---

## Personas & Actors

Include user personas to show who interacts with what:

```python
from diagrams.onprem.client import Users

data_scientist = Users("Data Scientist")
mlops_engineer = Users("MLOps Engineer")

data_scientist >> Edge(color="green") >> dashboard
mlops_engineer >> Edge(color="green") >> model_registry
```

**Why?** Consulting engagements need to show value for different user roles.

---

## Generating Diagrams

### Quick Start

```bash
# Setup (first time)
./setup.sh

# Generate all diagrams
make generate-all

# Generate single diagram
./venv/bin/python3 diagrams/baseline-reference/ocp/01-core-infrastructure.py
```

### Output Location

All diagrams generate to: `output/*.png`

**Note:** `output/` is gitignored. Diagrams are generated from source code, not stored in git.

---

## Best Practices for Consulting Engagements

### Environment Strategy

Common patterns (adapt to customer):
- **Production**: Strict isolation, HA/DR, business-critical workloads
- **Pre-production**: May share resources (QA + Test), production-like validation
- **Sandbox**: MUST be isolated from prod and non-prod, self-service for data scientists

**Critical principle:** Sandbox environments must NOT impact production OR non-production capabilities.

### Cluster Topology Decisions

Depends on customer context:
- **Budget**: Shared clusters reduce costs
- **Compliance**: Separate clusters for data isolation
- **Team structure**: Dedicated clusters per team
- **Data sensitivity**: Air-gapped production clusters

**Do NOT prescribe** a specific number of clusters. Present options and tradeoffs.

### Customer-Specific Adaptations

When creating engagement diagrams:
1. Use customer's terminology for systems and zones
2. Add customer-specific integration points (their IDP, storage vendor, monitoring tools)
3. Adjust sizing annotations to match their infrastructure
4. Include customer's security/compliance requirements
5. Match their network topology and zones

---

## File Naming Conventions

- **Directories**: `kebab-case` (e.g., `baseline-reference`, `engagement-ai-platform`)
- **Python files**: `kebab-case.py` (e.g., `core-infrastructure.py`, `ml-workflow.py`)
- **Output files**: Match source filename (e.g., `core-infrastructure.py` → `output/core-infrastructure.png`)
- **Namespaces in code**: Use actual OpenShift namespace names (e.g., `openshift-monitoring`, `redhat-ods-operator`)

---

## Code Style

### Diagram Structure Template

```python
"""
Diagram Title

Brief description of what this diagram shows.

Namespace organization: list key namespaces
Color coding: explain color scheme used

Note: Any special considerations
"""

from diagrams import Diagram, Cluster, Edge
# ... imports

graph_attr = {
    "fontsize": "14-16",
    "bgcolor": "white",
    "pad": "0.5",
    "nodesep": "0.8-1.0",
    "ranksep": "1.5-1.8"
}

with Diagram(
    "Diagram Title",
    show=False,
    direction="TB or LR",
    filename="output/diagram-name",
    graph_attr=graph_attr
):
    # Diagram code with clear sections
    pass

print("✓ Generated: output/diagram-name.png")
print("  → Additional context about the diagram")
```

### Import Organization

```python
# Standard diagrams imports
from diagrams import Diagram, Cluster, Edge

# Kubernetes components
from diagrams.k8s.controlplane import APIServer
from diagrams.k8s.ecosystem import Helm

# On-premise/generic components
from diagrams.onprem.monitoring import Prometheus
from diagrams.onprem.compute import Server

# Users/personas
from diagrams.onprem.client import Users
```

### Using Custom Icons

**CRITICAL: Custom icons require absolute paths**

When using Red Hat Technology icons via `Custom()`, always use absolute paths calculated from `__file__`:

```python
import os
from diagrams.custom import Custom

# Calculate absolute paths at the top of the file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(BASE_DIR, '../../..')
OPERATOR_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Technology icons/operator/Technology_icon-Red_Hat-operator-Standard-RGB.Large_icon_transparent.png")
AI_MODEL_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Technology icons/AI model/Technology_icon-Red_Hat-AI_model-Standard-RGB.Large_icon_transparent.png")

# Use in diagram with leading newline for proper spacing
with Diagram(...):
    operator = Custom("\nMy Operator", OPERATOR_ICON)
    model = Custom("\nAI Model", AI_MODEL_ICON)
```

**Why absolute paths:** Relative paths don't resolve correctly from nested diagram directories. Icons won't render (only text labels appear) when using relative paths like `"custom_icons/..."`.

**Symptom if broken:** Diagrams generate without errors, but Custom icons don't appear - only text labels show.

**IMPORTANT: Add leading newline to all labels**

Always prefix labels with `\n` to create vertical spacing between icon images and label text:

```python
# CORRECT - has leading newline for spacing
dashboard = Custom("\nDashboard", DASHBOARD_ICON)
operator = Custom("\nRed Hat\nOpenShift AI\nOperator", OPERATOR_ICON)

# WRONG - label text touches icon bottom edge
dashboard = Custom("Dashboard", DASHBOARD_ICON)
operator = Custom("Red Hat\nOpenShift AI\nOperator", OPERATOR_ICON)
```

**Why:** The `node_attr` margin parameter controls padding around the entire node, not internal spacing between the icon image and label text. Without the leading newline, labels touch the bottom of icons.

**Also applies to standard library icons** (Prometheus, Tempo, etc.) when spacing is needed:

```python
prometheus = Prometheus("\nPrometheus\nData Science\nMonitoring Stack")
tempo = Tempo("\nTempo\nData Science\nTempoMonolithic")
```

---

## Version Control

### What to Commit

✅ Commit:
- Python diagram source files (`.py`)
- Documentation (README, CLAUDE.md)
- Templates
- Configuration files (Makefile, requirements.txt, .gitignore)
- Utility scripts (`utils/`)

❌ Do NOT commit:
- Generated images (`output/*.png`) - gitignored
- Virtual environment (`venv/`) - gitignored
- Python cache (`__pycache__/`) - gitignored

**Why?** Diagrams are code. Generate images from source, don't store binaries in git.

### Commit Message Format

```
Verb: brief description

- Key point about the change
- Why this change was made
- Impact on diagrams

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

Examples:
```
Add baseline OCP observability stack diagram

- Includes embedded monitoring (Cluster + UDWM)
- Add-on operators: Logging, Tempo, OpenTelemetry
- Color-coded connections for clarity
```

---

## Maintenance & Updates

### When to Update Baseline Diagrams

- New OpenShift operator becomes GA and relevant for AI/ML platforms
- RHOAI DataScienceCluster adds new component
- Customer feedback reveals missing integration points
- OpenShift namespace names change (rare)

### When to Create New Diagrams

- Customer requests specific architecture scenario
- New reference pattern emerges from multiple engagements
- Significant OpenShift feature warrants dedicated diagram

### Deprecated Components

When components are deprecated:
- Comment in code why removed
- Update README to note deprecation
- Keep in git history for reference

---

## Related Resources

### Internal References

- `diagrams/baseline-reference/README.md` - Detailed baseline diagram documentation
- `diagrams/engagement-ai-platform/README.md` - Engagement template documentation
- `docs/EXAMPLES.md` - Diagram code examples and patterns
- `CONTRIBUTING.md` - Contribution guidelines

### External References

- [Diagrams Documentation](https://diagrams.mingrammer.com/) - Python Diagrams library
- [OpenShift Documentation](https://docs.openshift.com/) - OpenShift Container Platform
- [RHOAI Documentation](https://access.redhat.com/documentation/en-us/red_hat_openshift_ai/) - Red Hat OpenShift AI
- [PlantUML Reference](https://plantuml.com/) - Inspiration for layered architecture patterns

---

## Questions?

For questions about:
- **Diagram standards**: See this file (CLAUDE.md)
- **Technical implementation**: See `diagrams/baseline-reference/README.md`
- **Contribution process**: See `CONTRIBUTING.md`
- **Specific examples**: See `docs/EXAMPLES.md`
