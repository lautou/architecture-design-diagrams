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
- prod-ai-project-x: Secured Model Server (KServe + TrustyAI Agent) + TrustyAI Service
- prod-ai-project-y: Model Servers (embeddings + llama 3.2 8b with Guardrails) + LlamaStack
- prod-ai-project-z: Secured Model Server (KServe + Guardrail Detector + Gateway) + Guardrail Orchestrator + LLM Router

Layout Technique:
- Two-area vertical stacking: Platform Components (top) + AI Projects (bottom)
- 5x3 grid in applications using vertical-only edges (no horizontal edges)
- 8 distributed anchor points across width to force clean vertical alignment
- Vertical stacking within namespaces to save horizontal space
- See CLAUDE.md "Complex Multi-Cluster Layouts" section for pattern details
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
GUARDRAILS_SMALL_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/Guardrails/guardrails-100x100.png")
CATALOG_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/Catalog/Icon-Red_Hat-Catalog-A-Red-RGB.Large_icon_transparent.png")
POSTGRESQL_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/PostgreSQL/postgresql-400x400.png")
LLMD_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/LLMD/llmd-400x400.png")
LLAMASTACK_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/LlamaStack/llamastack-400x400.png")

graph_attr = {
    "fontsize": "9",
    "bgcolor": "white",
    "pad": "0.5",
    "nodesep": "1.0",
    "ranksep": "1.0",
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
    with Cluster("Red Hat OpenShift AI Platform Components", graph_attr={"margin": "20", "bgcolor": "lightblue"}):

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

            # Vertical columns (no horizontal edges) - Graphviz will place columns side-by-side naturally
            # Column 1
            dashboard >> Edge(style="invis") >> odh_model_controller >> Edge(style="invis") >> mlflow_operator

            # Column 2
            rhoai_operator >> Edge(style="invis") >> modelreg_controller >> Edge(style="invis") >> llamastack_operator

            # Column 3
            kubeflow_notebook >> Edge(style="invis") >> dsp_operator >> Edge(style="invis") >> feast_operator

            # Column 4
            odh_notebook >> Edge(style="invis") >> training_operator >> Edge(style="invis") >> trustyai_operator

            # Column 5
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

    # ========== USER WORKLOADS ==========
    with Cluster("AI Project Environments (User Workloads)", graph_attr={"margin": "20", "bgcolor": "honeydew"}):

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
            with Cluster("Secured Model Server", graph_attr={"margin": "8", "bgcolor": "lightyellow", "style": "rounded"}):
                model_server_trusty = Custom("\nKServe\nModel Server", AI_MODEL_ICON)
                trustyai_agent = Custom("\nTrustyAI\nAgent", TRUSTYAI_ICON)
                model_server_trusty - Edge(style="invis") - trustyai_agent
            trustyai_service = Custom("\nTrustyAI Service", TRUSTYAI_ICON)

        # AI Project 5: Production with Guardrails
        with Cluster("prod-ai-project-z", graph_attr={"margin": "10"}):
            with Cluster("Secured Model Server", graph_attr={"margin": "8", "bgcolor": "lightyellow", "style": "rounded"}):
                model_server_guardrails = Custom("\nKServe\nModel Server", AI_MODEL_ICON)
                guardrail_detector = Custom("\nGuardrail\nBuilt-in Detector", GUARDRAILS_ICON)
                guardrail_gateway = Custom("\nGuardrail\nGateway", GUARDRAILS_ICON)
                model_server_guardrails - Edge(style="invis") - guardrail_detector - Edge(style="invis") - guardrail_gateway
            guardrail_orchestrator = Custom("\nGuardrail\nOrchestrator", GUARDRAILS_ICON)
            llm_router = Custom("\nLLM KServe\nRouter Scheduler", LLMD_ICON)

            # Stack vertically to save space
            guardrail_orchestrator >> Edge(style="invis") >> llm_router

        # AI Project 6: Production with LlamaStack
        with Cluster("prod-ai-project-y", graph_attr={"margin": "10"}):
            model_server_embeddings = Custom("\nKServe\nModel Server\n(embeddings)", AI_MODEL_ICON)
            with Cluster("Secured Model Server", graph_attr={"margin": "8", "bgcolor": "lightyellow", "style": "rounded"}):
                model_server_llama = Custom("\nKServe\nModel Server\n(llama 3.2 8b)", AI_MODEL_ICON)
                guardrail_detector_llama = Custom("\nGuardrail\nBuilt-in Detector", GUARDRAILS_ICON)
                model_server_llama - Edge(style="invis") - guardrail_detector_llama
            guardrail_orchestrator_y = Custom("\nGuardrail\nOrchestrator", GUARDRAILS_ICON)
            llamastack = Custom("\nLlamaStack\nServer", LLAMASTACK_ICON)

            # Stack vertically to save space
            model_server_embeddings >> Edge(style="invis") >> guardrail_orchestrator_y >> Edge(style="invis") >> llamastack

    # Force vertical alignment: Platform Components on top, AI Projects on bottom
    # Multiple connections across the entire width to force clean vertical stacking
    mlflow_operator >> Edge(style="invis") >> workbench_jupyter
    llamastack_operator >> Edge(style="invis") >> model_server_x
    feast_operator >> Edge(style="invis") >> workbench_vscode
    trustyai_operator >> Edge(style="invis") >> pipeline_server
    maas_api >> Edge(style="invis") >> ray_cluster
    tempo_ds >> Edge(style="invis") >> model_server_trusty
    workbench_default2 >> Edge(style="invis") >> trustyai_service
    postgres_db >> Edge(style="invis") >> model_server_embeddings

print("✓ Generated: output/baseline-rhoai-functional-components.png")
print("  → Platform namespaces (gray): redhat-ods-applications + redhat-ods-monitoring + rhods-notebooks + rhoai-model-registries")
print("  → AI Project namespaces: dev-ai-project-x/z + mlops-pipeline-project-y + prod-ai-project-x/y/z")
print("  → Components: 15 operators + 5 monitoring + 2 workbenches + 4 model registry components + 6 AI projects")
