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

**Red Hat OpenShift AI (2 diagrams):**

5. **`rhoai/functional-components.py`**
   - All DataScienceCluster CR components
   - Organized by namespace (redhat-ods-operator, redhat-ods-applications, AI Projects)
   - Shows full ML/AI workflow

6. **`integration/rhoai-ocp-integration.py`**
   - RHOAI platform running on OCP with dependencies on OCP services
   - 6 OCP service categories: Compute & Acceleration, Observability, Security & Identity Services, Developer Services, Storage Services, Core Components
   - Shows which OCP platform operators RHOAI requires (GPU, Kueue, LWS, ODF, RHCL)
   - 4-row layout: RHOAI platform (row 1) + OCP Compute/Observability (row 2) + OCP Security/Developer/Storage (row 3) + Core Components (row 4 in 2-row grid)
   - 11 RHOAI namespaces: redhat-ods-applications, redhat-ods-monitoring, rhods-notebooks (Jupyter + Code Server workbenches), ai-project-A through ai-project-H
   - 20 Core Components (simplified): Control Plane (5), Networking (4), Management (4), Storage/Registry (2), Infrastructure (3), Security (2)
   - Core Components use OpenShift icon only (no namespace rectangles) in 2-row grid (10 + 10) for compact display
   - OCP Services (rows 2-3) use white rounded rectangles with specific operator/component icons
   - Simplified from 50 namespaces to 20 essential components for integration diagram clarity

**Why layered for OCP?** 22+ operators would be overwhelming in one diagram. Functional layers serve different stakeholder audiences.

**Why comprehensive for RHOAI functional?** RHOAI is more cohesive as a single product; one diagram shows the complete AI platform capability.

**Why integration diagram?** Shows how RHOAI depends on OCP platform services, critical for understanding deployment prerequisites and operator dependencies.

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

## Complex Multi-Cluster Layouts

### Two-Area Vertical Stacking

For diagrams with distinct logical areas (e.g., Platform Components vs User Workloads), use **separate top-level clusters** and **distributed anchor points** to force clean vertical alignment.

#### Architecture

```python
with Diagram(...):
    # TOP AREA: Platform/Infrastructure
    with Cluster("Platform Components", graph_attr={"bgcolor": "lightblue"}):
        # Multiple namespaces at same level
        with Cluster("namespace-1"):
            component_a = ...
        with Cluster("namespace-2"):
            component_b = ...
    
    # BOTTOM AREA: User Workloads (separate cluster, NOT nested)
    with Cluster("User Workloads", graph_attr={"bgcolor": "honeydew"}):
        with Cluster("project-1"):
            workload_a = ...
        with Cluster("project-2"):
            workload_b = ...
    
    # CRITICAL: Distributed anchor points to force vertical stacking
    # Connect bottom nodes from top area to top nodes in bottom area
    # Use 6-8 connections distributed across the full width
    component_a >> Edge(style="invis") >> workload_a
    component_b >> Edge(style="invis") >> workload_b
    # ... add more anchors across the width
```

**Why this works:**
- Separate top-level clusters prevent Graphviz from mixing areas
- Multiple invisible edges create a "vertical constraint grid"
- Distribution across full width prevents staircase placement
- Each anchor pulls its local region into vertical alignment

**Common mistake:** Using only 1-2 anchor points creates staircase effect. Need 6-8 distributed anchors.

#### Graph Attributes for Multi-Cluster

```python
graph_attr = {
    "ranksep": "1.0",    # Vertical spacing between ranks
    "nodesep": "1.0",    # Horizontal spacing between nodes
    "dpi": "300",        # High resolution for presentations
    "direction": "TB"    # Top-to-bottom flow
}
```

**Avoid:**
- `newrank="true"` - Can cause instability with many clusters
- Small `ranksep` (<0.8) - Clusters overlap
- Horizontal edges between top-level clusters - Creates staircase

### Grid Layouts (5x3, 4x4, etc.)

Use **vertical-only edges** to create clean grids. Horizontal edges cause diagonal staircase layouts.

```python
with Cluster("Components Grid"):
    # Define all nodes
    row1_col1 = Custom("Component 1", icon)
    row1_col2 = Custom("Component 2", icon)
    row2_col1 = Custom("Component 3", icon)
    row2_col2 = Custom("Component 4", icon)
    
    # ONLY vertical edges - Graphviz places columns side-by-side naturally
    # Column 1
    row1_col1 >> Edge(style="invis") >> row2_col1
    
    # Column 2
    row1_col2 >> Edge(style="invis") >> row2_col2
    
    # DO NOT add horizontal edges (row1_col1 - row1_col2)
```

**Why:** Graphviz's ranking algorithm places unconnected vertical chains side-by-side. Horizontal edges confuse this and create staircase layouts.

### Vertical Stacking to Save Space

Stack components vertically within a namespace to reduce diagram width:

```python
with Cluster("my-namespace"):
    component_a = Custom("Service A", icon)
    component_b = Custom("Service B", icon)
    component_c = Custom("Service C", icon)
    
    # Stack vertically
    component_a >> Edge(style="invis") >> component_b >> Edge(style="invis") >> component_c
```

**Use case:** When a namespace has many independent components that don't need to show relationships.

### What to Avoid

❌ **Invisible wrapper clusters** - Don't wrap related clusters in invisible containers. This breaks Graphviz's layout algorithm.

```python
# DON'T DO THIS
with Cluster("", graph_attr={"style": "invis"}):
    with Cluster("namespace-1"):
        ...
    with Cluster("namespace-2"):
        ...
```

❌ **Horizontal edges between clusters** - Creates staircase placement instead of vertical stacking.

```python
# DON'T DO THIS
cluster_a_node - Edge(style="invis") - cluster_b_node  # Staircase!
```

❌ **Mixed horizontal + vertical edges in grids** - Pick one direction (vertical) and stick to it.

```python
# DON'T DO THIS
row1_col1 - row1_col2  # Horizontal
row1_col1 >> row2_col1  # Vertical
# Results in diagonal staircase
```

### Icon Centering Solution (Apr 2026)

**RESOLVED:** All baseline diagrams now use direct Graphviz with HTML table labels for perfect icon centering, regardless of cluster label length.

**Historical context:** The Python `diagrams` library had a limitation where long cluster labels (e.g., "openshift-apiserver-operator") caused icons to appear left-aligned within namespace rectangles. This was a Graphviz LP (Linear Programming) constraint solver limitation, not a configuration error.

**Solution implemented:** Stephen North (Graphviz maintainer) provided a workaround in [GitLab issue #2832](https://gitlab.com/graphviz/graphviz/-/work_items/2832): Use HTML table labels instead of plain text labels. This bypasses the LP solver's centering algorithm and provides pixel-perfect centering.

**Implementation:** All 6 baseline diagrams converted from `diagrams` library to direct `graphviz.Digraph()` with HTML table labels:

```python
from graphviz import Digraph

def html_node(icon_path, label_text):
    """Create HTML table label for perfect centering"""
    return f'''<<table border="0">
<tr><td><img src="{icon_path}"/></td></tr>
<tr><td>{label_text}</td></tr>
</table>>'''

# Usage
dot.node('my_node', label=html_node(ICON_PATH, 'My Label'), shape='none')
```

**Benefits:**
- ✅ Perfect icon centering with any cluster label length
- ✅ Full control over Graphviz DOT attributes
- ✅ Accurate OpenShift namespace names preserved
- ✅ No trade-offs between accuracy and aesthetics

### Real-World Examples

All baseline diagrams now use direct Graphviz with HTML table labels:

**RHOAI Functional Components** - `diagrams/baseline-reference/rhoai/functional-components.py`:
- Two areas: Platform Components (top) + AI Projects (bottom)
- 5×3 grid in applications namespace using vertical-only edges
- 8 distributed anchor points for clean vertical stacking
- Vertical stacking within namespaces to save space
- Perfect icon centering with HTML table labels

**RHOAI-OCP Integration** - `diagrams/baseline-reference/integration/rhoai-ocp-integration.py`:
- 4-row layout: RHOAI platform (row 1) + OCP Compute/Observability (row 2) + OCP Security/Developer/Storage (row 3) + Core Components (row 4)
- Distributed anchor points (8 from Row 3→Core Components) for clean vertical stacking
- 11 RHOAI namespaces in Row 1: redhat-ods-applications, redhat-ods-monitoring, rhods-notebooks (Jupyter + Code Server workbenches), ai-project-A through ai-project-H
- 20 Core Components (simplified): Control Plane (5), Networking (4), Management (4), Storage/Registry (2), Infrastructure (3), Security (2)
- Core Components use 2-row grid layout (10 + 10) with internal vertical edges for compact display
- Row 4.1 (10): Control Plane + Networking + Console
- Row 4.2 (10): Management + Storage + Infrastructure + Security
- Core Components use OpenShift icon only (no namespace rectangles) for visual simplicity
- OCP Services (rows 2-3) use white rounded rectangles with specific operator/component icons
- Row 3 ordered largest to smallest: Security & Identity (6), Developer (3), Storage (1)
- Simplified from 50 namespaces to 20 essential components for integration diagram clarity

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

**IMPORTANT:** All baseline diagrams use direct Graphviz with HTML table labels for perfect icon centering.

```python
"""
Diagram Title (Direct Graphviz)

Brief description of what this diagram shows.

Namespace organization: list key namespaces
Color coding: explain color scheme used

Note: Uses direct Graphviz with HTML table labels for perfect icon centering
"""

from graphviz import Digraph
import os

# Get absolute paths for icons
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(BASE_DIR, '../../..')
ICON_PATH = os.path.join(PROJECT_ROOT, "custom_icons/...")

# Helper function
def html_node(icon_path, label_text):
    """Create HTML table label for perfect centering"""
    return f'''<<table border="0">
<tr><td><img src="{icon_path}"/></td></tr>
<tr><td>{label_text}</td></tr>
</table>>'''

# Create diagram
dot = Digraph("Diagram_Name", filename="output/diagram-name")
dot.attr(rankdir="TB")  # or "LR"
dot.attr(fontsize="14-16", bgcolor="white", pad="0.5", nodesep="0.8-1.0", ranksep="1.5-1.8")

# Diagram code with clear sections
dot.node('node_id', label=html_node(ICON_PATH, 'Label<br/>Text'), shape='none')

# Render diagram
dot.render(format='png', view=False, quiet=True)

print("✓ Generated: output/diagram-name.png (Direct Graphviz with HTML tables)")
print("  → Additional context about the diagram")
```

### Import Organization

**All baseline diagrams use direct Graphviz:**

```python
# Direct Graphviz for perfect icon centering
from graphviz import Digraph
import os

# Get absolute icon paths (CRITICAL for custom icons)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(BASE_DIR, '../../..')

# Icon paths
OPERATOR_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Technology icons/operator/...")
OPENSHIFT_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Technology icons/Red Hat OpenShift/...")
# ... other icons
```

### Using Custom Icons with Graphviz

**CRITICAL: Icons require absolute paths and HTML table labels**

All baseline diagrams use direct Graphviz with HTML table labels for perfect icon centering:

```python
import os
from graphviz import Digraph

# Calculate absolute paths at the top of the file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(BASE_DIR, '../../..')
OPERATOR_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Technology icons/operator/Technology_icon-Red_Hat-operator-Standard-RGB.Large_icon_transparent.png")
AI_MODEL_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Technology icons/AI model/Technology_icon-Red_Hat-AI_model-Standard-RGB.Large_icon_transparent.png")

# Helper function for HTML table labels
def html_node(icon_path, label_text):
    """Create HTML table label for perfect centering"""
    return f'''<<table border="0">
<tr><td><img src="{icon_path}"/></td></tr>
<tr><td>{label_text}</td></tr>
</table>>'''

# Use in diagram
dot = Digraph(...)
dot.node('operator', label=html_node(OPERATOR_ICON, 'My Operator'), shape='none')
dot.node('model', label=html_node(AI_MODEL_ICON, 'AI Model'), shape='none')
```

**Why absolute paths:** Relative paths don't resolve correctly from nested diagram directories. Icons won't render when using relative paths like `"custom_icons/..."`.

**Why HTML table labels:** Provides pixel-perfect icon centering regardless of cluster label length. See [Icon Centering Solution](#icon-centering-solution-apr-2026) for details.

**HTML label formatting:** Use `<br/>` for line breaks in label text:

```python
# Multi-line label
operator = html_node(OPERATOR_ICON, 'Red Hat<br/>OpenShift AI<br/>Operator')

# Single line
dashboard = html_node(DASHBOARD_ICON, 'Dashboard')
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
