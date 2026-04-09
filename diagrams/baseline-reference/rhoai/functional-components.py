"""
Red Hat OpenShift AI (RHOAI) - Functional Components Baseline (Direct Graphviz)

Functional view showing RHOAI platform components organized by namespace.

Out-of-the-box namespaces (gray background):
- redhat-ods-applications: Dashboard + 14 Operators/Controllers
- redhat-ods-monitoring: Monitoring stack (Prometheus, Alertmanager, Thanos, Tempo, OTel)
- rhods-notebooks: Default Jupyter Workbenches (2x)
- rhoai-model-registries: Model registries + Model Catalog + PostgreSQL

AI Project namespaces (user-created, Kubernetes naming convention):
- dev-ai-project-x: Jupyter Workbench + Model Server
- dev-ai-project-z: VS Code Workbench
- mlops-pipeline-project-y: Data Science Pipeline Server + Ray Cluster
- prod-ai-project-x: Secured Model Server (KServe + TrustyAI Agent) + TrustyAI Service
- prod-ai-project-y: Model Servers (embeddings + llama 3.2 8b with Guardrails) + LlamaStack
- prod-ai-project-z: Secured Model Server (KServe + Guardrail Detector + Gateway) + Guardrail Orchestrator + LLM Router

Layout Technique:
- Two-area vertical stacking: Platform Components (top) + AI Projects (bottom)
- 5x3 grid in applications using vertical-only edges (no horizontal edges)
- 8 distributed anchor points across width to force clean vertical alignment
- Vertical stacking within namespaces to save horizontal space
- Uses direct Graphviz with HTML table labels for perfect icon centering

Note: See CLAUDE.md "Complex Multi-Cluster Layouts" section for pattern details
"""

from graphviz import Digraph
import os

# Get absolute paths for icons
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(BASE_DIR, '../../..')

# Platform icons
OPERATOR_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Technology icons/operator/Technology_icon-Red_Hat-operator-Standard-RGB.Large_icon_transparent.png")
DASHBOARD_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/Monitor/Icon-Red_Hat-Monitor_Blank-A-Red-RGB.Large_icon_transparent.png")
OTEL_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/OpenTelemetry/opentelemetry-400x400.png")
THANOS_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/Thanos/thanos-400x400.png")
MONITORING_ICON = os.path.join(PROJECT_ROOT, "custom_icons/UI icons/rh-ui-icon-monitoring-fill.Large_icon_transparent.png")
TEMPO_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/Tempo/tempo-400x400.png")

# AI Project workload icons
JUPYTER_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/Jupyter/jupyter-400x400.png")
VSCODE_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/VSCode/vscode-400x400.png")
AI_MODEL_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Technology icons/AI model/Technology_icon-Red_Hat-AI_model-Standard-RGB.Large_icon_transparent.png")
KUBEFLOW_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/Kubeflow/kubeflow-400x400.png")
RAY_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/Ray/ray-400x400.png")
TRUSTYAI_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/TrustyAI/trustyai-400x400.png")
GUARDRAILS_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/Guardrails/guardrails-400x400.png")
CATALOG_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/Catalog/Icon-Red_Hat-Catalog-A-Red-RGB.Large_icon_transparent.png")
POSTGRESQL_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/PostgreSQL/postgresql-400x400.png")
LLMD_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/LLMD/llmd-400x400.png")
LLAMASTACK_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/LlamaStack/llamastack-400x400.png")

# Helper function
def html_node(icon_path, label_text):
    """Create HTML table label for perfect centering"""
    return f'''<<table border="0">
<tr><td><img src="{icon_path}"/></td></tr>
<tr><td>{label_text}</td></tr>
</table>>'''

# Create diagram
dot = Digraph("RHOAI_Functional_Components", filename="output/baseline-rhoai-functional-components")
dot.attr(rankdir="TB")
dot.attr(fontsize="9", bgcolor="white", pad="0.5", nodesep="1.0", ranksep="1.0", dpi="300")

# ========== RED HAT OPENSHIFT AI PLATFORM ==========
with dot.subgraph(name='cluster_platform') as platform:
    platform.attr(label='Red Hat OpenShift AI Platform Components', margin='20', bgcolor='lightblue')

    # redhat-ods-applications namespace (out-of-the-box)
    with platform.subgraph(name='cluster_ods_apps') as apps:
        apps.attr(label='redhat-ods-applications', margin='15', bgcolor='lightgray')

        # Row 1: Core (5 components)
        apps.node('dashboard', label=html_node(DASHBOARD_ICON, 'Dashboard'), shape='none')
        apps.node('rhoai_operator', label=html_node(OPERATOR_ICON, 'Red Hat<br/>OpenShift AI<br/>Operator'), shape='none')
        apps.node('kubeflow_notebook', label=html_node(OPERATOR_ICON, 'Kubeflow<br/>Notebook<br/>Controller'), shape='none')
        apps.node('odh_notebook', label=html_node(OPERATOR_ICON, 'Open Data Hub<br/>Notebook<br/>Controller Manager'), shape='none')
        apps.node('kserve_controller', label=html_node(OPERATOR_ICON, 'KServe<br/>Controller<br/>Manager'), shape='none')

        # Row 2: Model & Pipelines (5 components)
        apps.node('odh_model_controller', label=html_node(OPERATOR_ICON, 'Open Data Hub<br/>Model<br/>Controller'), shape='none')
        apps.node('modelreg_controller', label=html_node(OPERATOR_ICON, 'Model Registry<br/>Operator<br/>Controller Manager'), shape='none')
        apps.node('dsp_operator', label=html_node(OPERATOR_ICON, 'Data Science<br/>Pipelines Operator<br/>Controller Manager'), shape='none')
        apps.node('training_operator', label=html_node(OPERATOR_ICON, 'Kubeflow<br/>Training<br/>Operator'), shape='none')
        apps.node('kuberay_operator', label=html_node(OPERATOR_ICON, 'KubeRay<br/>Operator'), shape='none')

        # Row 3: ML Platforms & Governance (5 components)
        apps.node('mlflow_operator', label=html_node(OPERATOR_ICON, 'MLFlow<br/>Operator<br/>Controller Manager'), shape='none')
        apps.node('llamastack_operator', label=html_node(OPERATOR_ICON, 'LlamaStack<br/>K8s Operator<br/>Controller Manager'), shape='none')
        apps.node('feast_operator', label=html_node(OPERATOR_ICON, 'Feast<br/>Operator<br/>Controller Manager'), shape='none')
        apps.node('trustyai_operator', label=html_node(OPERATOR_ICON, 'TrustyAI<br/>Service Operator<br/>Controller Manager'), shape='none')
        apps.node('maas_api', label=html_node(OPERATOR_ICON, 'MaaS API'), shape='none')

        # Vertical columns (no horizontal edges) - Graphviz will place columns side-by-side naturally
        # Column 1
        apps.edge('dashboard', 'odh_model_controller', style='invis')
        apps.edge('odh_model_controller', 'mlflow_operator', style='invis')

        # Column 2
        apps.edge('rhoai_operator', 'modelreg_controller', style='invis')
        apps.edge('modelreg_controller', 'llamastack_operator', style='invis')

        # Column 3
        apps.edge('kubeflow_notebook', 'dsp_operator', style='invis')
        apps.edge('dsp_operator', 'feast_operator', style='invis')

        # Column 4
        apps.edge('odh_notebook', 'training_operator', style='invis')
        apps.edge('training_operator', 'trustyai_operator', style='invis')

        # Column 5
        apps.edge('kserve_controller', 'kuberay_operator', style='invis')
        apps.edge('kuberay_operator', 'maas_api', style='invis')

    # redhat-ods-monitoring namespace (out-of-the-box)
    with platform.subgraph(name='cluster_ods_monitoring') as monitoring:
        monitoring.attr(label='redhat-ods-monitoring', margin='15', bgcolor='lightgray')

        # Row 1: Metrics
        monitoring.node('alertmanager_ds', label=html_node(MONITORING_ICON, 'AlertManager<br/>Data Science<br/>Monitoring Stack'), shape='none')
        monitoring.node('prometheus_ds', label=html_node(MONITORING_ICON, 'Prometheus<br/>Data Science<br/>Monitoring Stack'), shape='none')
        monitoring.node('thanos_querier', label=html_node(THANOS_ICON, 'Thanos Querier<br/>Data Science'), shape='none')

        # Row 2: Telemetry
        monitoring.node('ds_collector', label=html_node(OTEL_ICON, 'Data Science<br/>Collector'), shape='none')
        monitoring.node('tempo_ds', label=html_node(TEMPO_ICON, 'Tempo<br/>Data Science<br/>TempoMonolithic'), shape='none')

        # Layout
        monitoring.edge('alertmanager_ds', 'prometheus_ds', style='invis', constraint='false')
        monitoring.edge('prometheus_ds', 'thanos_querier', style='invis', constraint='false')
        monitoring.edge('ds_collector', 'tempo_ds', style='invis', constraint='false')
        monitoring.edge('alertmanager_ds', 'ds_collector', style='invis')

    # rhods notebook namespace (out-of-the-box)
    with platform.subgraph(name='cluster_rhods_notebooks') as notebooks:
        notebooks.attr(label='rhods-notebooks', margin='15', bgcolor='lightgray')
        notebooks.node('workbench_default1', label=html_node(JUPYTER_ICON, 'Jupyter<br/>Workbench 1'), shape='none')
        notebooks.node('workbench_default2', label=html_node(JUPYTER_ICON, 'Jupyter<br/>Workbench 2'), shape='none')
        notebooks.edge('workbench_default1', 'workbench_default2', style='invis', constraint='false')

    # Model registries namespace (out-of-the-box)
    with platform.subgraph(name='cluster_model_registries') as registries:
        registries.attr(label='rhoai-model-registries', margin='15', bgcolor='lightgray')
        registries.node('model_registry_a', label=html_node(KUBEFLOW_ICON, 'model-registry-A'), shape='none')
        registries.node('model_registry_b', label=html_node(KUBEFLOW_ICON, 'model-registry-B'), shape='none')
        registries.node('model_catalog', label=html_node(CATALOG_ICON, 'Model Catalog'), shape='none')
        registries.node('postgres_db', label=html_node(POSTGRESQL_ICON, 'Model Catalog<br/>PostgreSQL'), shape='none')
        registries.edge('model_registry_a', 'model_registry_b', style='invis', constraint='false')
        registries.edge('model_registry_b', 'model_catalog', style='invis', constraint='false')
        registries.edge('model_catalog', 'postgres_db', style='invis', constraint='false')

# ========== USER WORKLOADS ==========
with dot.subgraph(name='cluster_user_workloads') as workloads:
    workloads.attr(label='AI Project Environments (User Workloads)', margin='20', bgcolor='honeydew')

    # AI Project 1: Development with Jupyter
    with workloads.subgraph(name='cluster_dev_x') as dev_x:
        dev_x.attr(label='dev-ai-project-x', margin='10')
        dev_x.node('workbench_jupyter', label=html_node(JUPYTER_ICON, 'Jupyter<br/>Workbench'), shape='none')
        dev_x.node('model_server_x', label=html_node(AI_MODEL_ICON, 'Model Server<br/>(KServe)'), shape='none')
        dev_x.edge('workbench_jupyter', 'model_server_x', style='invis', constraint='false')

    # AI Project 2: Development with VS Code
    with workloads.subgraph(name='cluster_dev_z') as dev_z:
        dev_z.attr(label='dev-ai-project-z', margin='10')
        dev_z.node('workbench_vscode', label=html_node(VSCODE_ICON, 'VS Code<br/>Workbench'), shape='none')

    # AI Project 3: MLOps Pipeline
    with workloads.subgraph(name='cluster_mlops_y') as mlops_y:
        mlops_y.attr(label='mlops-pipeline-project-y', margin='10')
        mlops_y.node('pipeline_server', label=html_node(KUBEFLOW_ICON, 'Data Science<br/>Pipeline Server'), shape='none')
        mlops_y.node('ray_cluster', label=html_node(RAY_ICON, 'Ray Cluster'), shape='none')
        mlops_y.edge('pipeline_server', 'ray_cluster', style='invis', constraint='false')

    # AI Project 4: Production serving with TrustyAI
    with workloads.subgraph(name='cluster_prod_x') as prod_x:
        prod_x.attr(label='prod-ai-project-x', margin='10')

        with prod_x.subgraph(name='cluster_secured_x') as secured_x:
            secured_x.attr(label='Secured Model Server', margin='8', bgcolor='lightyellow', style='rounded')
            secured_x.node('model_server_trusty', label=html_node(AI_MODEL_ICON, 'KServe<br/>Model Server'), shape='none')
            secured_x.node('trustyai_agent', label=html_node(TRUSTYAI_ICON, 'TrustyAI<br/>Agent'), shape='none')
            secured_x.edge('model_server_trusty', 'trustyai_agent', style='invis', constraint='false')

        prod_x.node('trustyai_service', label=html_node(TRUSTYAI_ICON, 'TrustyAI Service'), shape='none')

    # AI Project 5: Production with Guardrails
    with workloads.subgraph(name='cluster_prod_z') as prod_z:
        prod_z.attr(label='prod-ai-project-z', margin='10')

        with prod_z.subgraph(name='cluster_secured_z') as secured_z:
            secured_z.attr(label='Secured Model Server', margin='8', bgcolor='lightyellow', style='rounded')
            secured_z.node('model_server_guardrails', label=html_node(AI_MODEL_ICON, 'KServe<br/>Model Server'), shape='none')
            secured_z.node('guardrail_detector', label=html_node(GUARDRAILS_ICON, 'Guardrail<br/>Built-in Detector'), shape='none')
            secured_z.node('guardrail_gateway', label=html_node(GUARDRAILS_ICON, 'Guardrail<br/>Gateway'), shape='none')
            secured_z.edge('model_server_guardrails', 'guardrail_detector', style='invis', constraint='false')
            secured_z.edge('guardrail_detector', 'guardrail_gateway', style='invis', constraint='false')

        prod_z.node('guardrail_orchestrator', label=html_node(GUARDRAILS_ICON, 'Guardrail<br/>Orchestrator'), shape='none')
        prod_z.node('llm_router', label=html_node(LLMD_ICON, 'LLM KServe<br/>Router Scheduler'), shape='none')
        prod_z.edge('guardrail_orchestrator', 'llm_router', style='invis')

    # AI Project 6: Production with LlamaStack
    with workloads.subgraph(name='cluster_prod_y') as prod_y:
        prod_y.attr(label='prod-ai-project-y', margin='10')
        prod_y.node('model_server_embeddings', label=html_node(AI_MODEL_ICON, 'KServe<br/>Model Server<br/>(embeddings)'), shape='none')

        with prod_y.subgraph(name='cluster_secured_y') as secured_y:
            secured_y.attr(label='Secured Model Server', margin='8', bgcolor='lightyellow', style='rounded')
            secured_y.node('model_server_llama', label=html_node(AI_MODEL_ICON, 'KServe<br/>Model Server<br/>(llama 3.2 8b)'), shape='none')
            secured_y.node('guardrail_detector_llama', label=html_node(GUARDRAILS_ICON, 'Guardrail<br/>Built-in Detector'), shape='none')
            secured_y.edge('model_server_llama', 'guardrail_detector_llama', style='invis', constraint='false')

        prod_y.node('guardrail_orchestrator_y', label=html_node(GUARDRAILS_ICON, 'Guardrail<br/>Orchestrator'), shape='none')
        prod_y.node('llamastack', label=html_node(LLAMASTACK_ICON, 'LlamaStack<br/>Server'), shape='none')
        prod_y.edge('model_server_embeddings', 'guardrail_orchestrator_y', style='invis')
        prod_y.edge('guardrail_orchestrator_y', 'llamastack', style='invis')

# Force vertical alignment: Platform Components on top, AI Projects on bottom
# Multiple connections across the entire width to force clean vertical stacking
dot.edge('mlflow_operator', 'workbench_jupyter', style='invis')
dot.edge('llamastack_operator', 'model_server_x', style='invis')
dot.edge('feast_operator', 'workbench_vscode', style='invis')
dot.edge('trustyai_operator', 'pipeline_server', style='invis')
dot.edge('maas_api', 'ray_cluster', style='invis')
dot.edge('tempo_ds', 'model_server_trusty', style='invis')
dot.edge('workbench_default2', 'trustyai_service', style='invis')
dot.edge('postgres_db', 'model_server_embeddings', style='invis')

# Render diagram
dot.render(format='png', view=False, quiet=True)

print("✓ Generated: output/baseline-rhoai-functional-components.png (Direct Graphviz with HTML tables)")
print("  → Platform namespaces (gray): redhat-ods-applications + redhat-ods-monitoring + rhods-notebooks + rhoai-model-registries")
print("  → AI Project namespaces: dev-ai-project-x/z + mlops-pipeline-project-y + prod-ai-project-x/y/z")
print("  → Components: 15 operators + 5 monitoring + 2 workbenches + 4 model registry components + 6 AI projects")
print("  → All icons perfectly centered!")
