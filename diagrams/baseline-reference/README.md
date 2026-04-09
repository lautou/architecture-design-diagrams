# Baseline Reference Diagrams

These diagrams serve as **reusable building blocks** for customer engagements. They show the complete component stack without customer-specific customizations.

## Purpose

- **Reference architecture** - Shows all available components and operators
- **Learning tool** - Helps understand the full platform capabilities
- **Starting point** - Copy and adapt for customer-specific diagrams
- **Documentation** - Component relationships and integration points

## Structure

### Red Hat OpenShift AI (RHOAI) - 3 Diagrams

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

### RHOAI-OCP Integration Architecture

#### RHOAI on OCP Integration
**File:** `integration/rhoai-ocp-integration.py`
**Shows:**
- RHOAI platform running on OpenShift Container Platform (4-row layout)
- **Row 1 - RHOAI Platform namespaces (11):**
  - redhat-ods-applications: RHOAI operator
  - redhat-ods-monitoring: RHOAI monitoring stack
  - rhods-notebooks: Jupyter workbench, Code Server workbench
  - ai-project-A through ai-project-H: Sample AI workloads
- **Row 2 - OCP Compute & Observability:**
  - **Compute And Acceleration Services (4):** NVIDIA GPU Operator, Node Feature Discovery, Kueue, Leader Worker Set
  - **Observability Services (9):** Cluster Monitoring, UDWM, Grafana, Cluster Observability, Logging, Loki, OpenTelemetry, Tempo, Network Observability
- **Row 3 - OCP Security, Developer & Storage (ordered largest to smallest):**
  - **Security & Identity Services (6):** cert-manager, Authorino, Limitador, DNS, Red Hat Connectivity Link, OpenShift Service Mesh
  - **Developer Services (3):** Builds, Pipelines, GitOps
  - **Storage Services (1):** OpenShift Data Foundation
- **Row 4 - Core Components (20 essential components in 2-row grid):**
  - **Row 4.1 (10):** Control Plane (API Server, Authentication, Etcd, Controller, Scheduler) + Networking (DNS, Ingress, OVN, Multus) + Console
  - **Row 4.2 (10):** Management (OLM, Insights, Marketplace) + Storage/Registry (Image Registry, Cluster Storage) + Infrastructure (Machine API, Machine Config, Tuned) + Security (Service CA, Cloud Credential)

**Icons:** 
- RHOAI namespaces (Row 1) use white rounded rectangles with specific component icons
- OCP Services (Rows 2-3) use white rounded rectangles with specific operator/component icons
- Core Components (Row 4) use OpenShift icon only (no namespace rectangles) arranged in 2-row grid for compact display
- Simplified from 50 namespaces to 20 essential components for integration diagram clarity

**Use when:** Showing RHOAI platform dependencies on OCP services, discussing deployment prerequisites, understanding essential OCP components required for RHOAI

#### RHOAI External Integration
**File:** `integration/rhoai-external-integration.py`
**Shows:**
- Central AI Platform (Red Hat AI icon)
- **User Personas:** Data Scientists, MLOps Engineers, Developers
- **External Services:**
  - Identity Provider (authentication)
  - Database Services (training data)
  - Storage Services (models & artifacts)
- High-level integration points with external systems

**Use when:** Discussing external system integration, identity federation, data sources, model storage strategies

## How to Use These Diagrams

### 1. As Reference Material
Review these diagrams to understand the complete RHOAI platform:
```bash
# Generate all baseline diagrams
./venv/bin/python3 diagrams/baseline-reference/rhoai/functional-components.py
./venv/bin/python3 diagrams/baseline-reference/integration/rhoai-ocp-integration.py
./venv/bin/python3 diagrams/baseline-reference/integration/rhoai-external-integration.py
```

### 2. As Starting Points for Custom Diagrams
Copy a baseline diagram and adapt for customer needs:
```bash
# Example: Create customer-specific external integration diagram
cp diagrams/baseline-reference/integration/rhoai-external-integration.py \
   diagrams/engagement-ai-platform/01-production/external-integration-prod.py

# Edit to add customer-specific integrations (specific IDP, databases, storage vendors)
vim diagrams/engagement-ai-platform/01-production/external-integration-prod.py
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

### Implementation: Direct Graphviz with HTML Table Labels

All baseline diagrams use **direct Graphviz** with **HTML table labels** for perfect icon centering, regardless of cluster label length.

**Why this approach:**
- ✅ Perfect icon centering with any cluster label length (e.g., `openshift-cluster-observability-operator`)
- ✅ Full control over Graphviz DOT attributes
- ✅ Accurate OpenShift namespace names with dashes (e.g., `openshift-monitoring`, `redhat-ods-applications`, `rhods-notebooks`)
- ✅ Solves the Python `diagrams` library limitation documented in [GitLab issue #2832](https://gitlab.com/graphviz/graphviz/-/work_items/2832)

**Implementation pattern:**
```python
from graphviz import Digraph

def html_node(icon_path, label_text):
    return f'''<<table border="0">
<tr><td><img src="{icon_path}"/></td></tr>
<tr><td>{label_text}</td></tr>
</table>>'''

dot.node('node_id', label=html_node(ICON_PATH, 'Label<br/>Text'), shape='none')
```

See `CLAUDE.md` for complete code style guidelines and the "Icon Centering Solution" section for historical context.

## Related Documentation

- **Engagement Diagrams:** `../engagement-ai-platform/` - Customer-specific adaptations
- **Examples:** `../openshift/`, `../rhoai/` - Original example diagrams
- **Templates:** `../../templates/` - Blank diagram templates
