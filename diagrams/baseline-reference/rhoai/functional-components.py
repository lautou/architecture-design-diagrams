"""
Red Hat OpenShift AI (RHOAI) - Functional Components Baseline

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
- prod-ai-project-x: Model Server + TrustyAI Service
- prod-guardrails-project-y: Model Server + Guardrail Orchestrator

Layout: 5x3 grid for redhat-ods-applications, structured rows for other namespaces
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom
from diagrams.onprem.monitoring import Prometheus
from diagrams.onprem.tracing import Tempo
import os

# Get absolute paths for icons
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(BASE_DIR, '../../..')
OPERATOR_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Technology icons/operator/Technology_icon-Red_Hat-operator-Standard-RGB.Large_icon_transparent.png")
DASHBOARD_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/Monitor/Icon-Red_Hat-Monitor_Blank-A-Red-RGB.Large_icon_transparent.png")
OTEL_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/OpenTelemetry/opentelemetry-400x400.png")
THANOS_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/Thanos/thanos-400x400.png")

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

graph_attr = {
    "fontsize": "9",
    "bgcolor": "white",
    "pad": "0.5",
    "nodesep": "1.0",
    "ranksep": "0.5",
    "dpi": "300"
}

node_attr = {
    "margin": "0.5,0.3"
}

with Diagram(
    "Red Hat OpenShift AI - Functional Components",
    show=False,
    direction="TB",
    filename="output/baseline-rhoai-functional-components",
    graph_attr=graph_attr,
    node_attr=node_attr
):

    # ========== RED HAT OPENSHIFT AI PLATFORM ==========
    with Cluster("Red Hat OpenShift AI", graph_attr={"margin": "20", "bgcolor": "lightblue"}):

        # redhat-ods-applications namespace (out-of-the-box)
        with Cluster("redhat-ods-applications", graph_attr={"margin": "15", "bgcolor": "lightgray"}):
            # Row 1: Core (5 components)
            dashboard = Custom("\nDashboard", DASHBOARD_ICON)
            rhoai_operator = Custom("\nRed Hat\nOpenShift AI\nOperator", OPERATOR_ICON)
            kubeflow_notebook = Custom("\nKubeflow\nNotebook\nController", OPERATOR_ICON)
            odh_notebook = Custom("\nOpen Data Hub\nNotebook\nController Manager", OPERATOR_ICON)
            kserve_controller = Custom("\nKServe\nController\nManager", OPERATOR_ICON)

            # Row 2: Model & Pipelines (5 components)
            odh_model_controller = Custom("\nOpen Data Hub\nModel\nController", OPERATOR_ICON)
            modelreg_controller = Custom("\nModel Registry\nOperator\nController Manager", OPERATOR_ICON)
            dsp_operator = Custom("\nData Science\nPipelines Operator\nController Manager", OPERATOR_ICON)
            training_operator = Custom("\nKubeflow\nTraining\nOperator", OPERATOR_ICON)
            kuberay_operator = Custom("\nKubeRay\nOperator", OPERATOR_ICON)

            # Row 3: ML Platforms & Governance (5 components)
            mlflow_operator = Custom("\nMLFlow\nOperator\nController Manager", OPERATOR_ICON)
            llamastack_operator = Custom("\nLlamaStack\nK8s Operator\nController Manager", OPERATOR_ICON)
            feast_operator = Custom("\nFeast\nOperator\nController Manager", OPERATOR_ICON)
            trustyai_operator = Custom("\nTrustyAI\nService Operator\nController Manager", OPERATOR_ICON)
            maas_api = Custom("\nMaaS API", OPERATOR_ICON)

            # Horizontal edges for rows
            dashboard - Edge(style="invis") - rhoai_operator - Edge(style="invis") - kubeflow_notebook - Edge(style="invis") - odh_notebook - Edge(style="invis") - kserve_controller
            odh_model_controller - Edge(style="invis") - modelreg_controller - Edge(style="invis") - dsp_operator - Edge(style="invis") - training_operator - Edge(style="invis") - kuberay_operator
            mlflow_operator - Edge(style="invis") - llamastack_operator - Edge(style="invis") - feast_operator - Edge(style="invis") - trustyai_operator - Edge(style="invis") - maas_api

            # Vertical edges to stack rows
            dashboard >> Edge(style="invis") >> odh_model_controller >> Edge(style="invis") >> mlflow_operator
            rhoai_operator >> Edge(style="invis") >> modelreg_controller >> Edge(style="invis") >> llamastack_operator
            kubeflow_notebook >> Edge(style="invis") >> dsp_operator >> Edge(style="invis") >> feast_operator
            odh_notebook >> Edge(style="invis") >> training_operator >> Edge(style="invis") >> trustyai_operator
            kserve_controller >> Edge(style="invis") >> kuberay_operator >> Edge(style="invis") >> maas_api

        # redhat-ods-monitoring namespace (out-of-the-box)
        with Cluster("redhat-ods-monitoring", graph_attr={"margin": "15", "bgcolor": "lightgray"}):
            # Row 1: Metrics
            alertmanager_ds = Prometheus("\nAlertManager\nData Science\nMonitoring Stack")
            prometheus_ds = Prometheus("\nPrometheus\nData Science\nMonitoring Stack")
            thanos_querier = Custom("\nThanos Querier\nData Science", THANOS_ICON)

            # Row 2: Telemetry
            ds_collector = Custom("\nData Science\nCollector", OTEL_ICON)
            tempo_ds = Tempo("\nTempo\nData Science\nTempoMonolithic")

            # Layout
            alertmanager_ds - Edge(style="invis") - prometheus_ds - Edge(style="invis") - thanos_querier
            ds_collector - Edge(style="invis") - tempo_ds
            alertmanager_ds >> Edge(style="invis") >> ds_collector

        # rhods notebook namespace (out-of-the-box)
        with Cluster("rhods-notebooks", graph_attr={"margin": "15", "bgcolor": "lightgray"}):
            workbench_default1 = Custom("\nJupyter\nWorkbench 1", JUPYTER_ICON)
            workbench_default2 = Custom("\nJupyter\nWorkbench 2", JUPYTER_ICON)
            workbench_default1 - Edge(style="invis") - workbench_default2

        # Model registries namespace (out-of-the-box)
        with Cluster("rhoai-model-registries", graph_attr={"margin": "15", "bgcolor": "lightgray"}):
            model_registry_a = Custom("\nmodel-registry-A", KUBEFLOW_ICON)
            model_registry_b = Custom("\nmodel-registry-B", KUBEFLOW_ICON)
            model_catalog = Custom("\nModel Catalog", CATALOG_ICON)
            postgres_db = Custom("\nModel Catalog\nPostgreSQL", POSTGRESQL_ICON)

            model_registry_a - Edge(style="invis") - model_registry_b - Edge(style="invis") - model_catalog - Edge(style="invis") - postgres_db

        # AI Project 1: Development with Jupyter
        with Cluster("dev-ai-project-x", graph_attr={"margin": "10"}):
            workbench_jupyter = Custom("\nJupyter\nWorkbench", JUPYTER_ICON)
            model_server_x = Custom("\nModel Server\n(KServe)", AI_MODEL_ICON)
            workbench_jupyter - Edge(style="invis") - model_server_x

        # AI Project 2: Development with VS Code
        with Cluster("dev-ai-project-z", graph_attr={"margin": "10"}):
            workbench_vscode = Custom("\nVS Code\nWorkbench", VSCODE_ICON)

        # AI Project 3: MLOps Pipeline
        with Cluster("mlops-pipeline-project-y", graph_attr={"margin": "10"}):
            pipeline_server = Custom("\nData Science\nPipeline Server", KUBEFLOW_ICON)
            ray_cluster = Custom("\nRay Cluster", RAY_ICON)
            pipeline_server - Edge(style="invis") - ray_cluster

        # AI Project 4: Production serving with TrustyAI
        with Cluster("prod-ai-project-x", graph_attr={"margin": "10"}):
            model_server_prod = Custom("\nModel Server\n(KServe)", AI_MODEL_ICON)
            trustyai_service = Custom("\nTrustyAI Service", TRUSTYAI_ICON)
            model_server_prod - Edge(style="invis") - trustyai_service

        # AI Project 5: Production with Guardrails
        with Cluster("prod-guardrails-project-y", graph_attr={"margin": "10"}):
            model_server_guardrails = Custom("\nModel Server\n(KServe)", AI_MODEL_ICON)
            guardrail_orchestrator = Custom("\nGuardrail\nOrchestrator", GUARDRAILS_ICON)
            model_server_guardrails - Edge(style="invis") - guardrail_orchestrator

print("✓ Generated: output/baseline-rhoai-functional-components.png")
print("  → Platform namespaces (gray): redhat-ods-applications + redhat-ods-monitoring + rhods-notebooks + rhoai-model-registries")
print("  → AI Project namespaces: dev-ai-project-x/z + mlops-pipeline-project-y + prod-ai-project-x + prod-guardrails-project-y")
print("  → Components: 15 operators + 5 monitoring + 2 workbenches + 4 model registry components + 5 AI projects")
