"""
Red Hat OpenShift AI (RHOAI) - Functional Components Baseline

This diagram follows the namespace-based layered architecture pattern:
- LAYER 1: Management & Operators (redhat-ods-operator, redhat-ods-applications)
- LAYER 2: User Workloads (AI Projects - user namespaces)
- LAYER 3: Infrastructure Dependencies (External systems)
- SIDE: Observability (redhat-ods-monitoring)

Color-coded connections:
- Orange: Management/hierarchy
- Purple: Observability/monitoring
- Green: API requests
- Blue: Data flows

Note: Organized by actual OpenShift namespaces for clarity
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.controlplane import APIServer
from diagrams.k8s.network import Ingress
from diagrams.k8s.ecosystem import Helm
from diagrams.onprem.mlops import Mlflow
from diagrams.onprem.vcs import Github
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.storage import Ceph
from diagrams.programming.language import Python
from diagrams.onprem.compute import Server
from diagrams.onprem.client import Users
from diagrams.onprem.monitoring import Prometheus

graph_attr = {
    "fontsize": "14",
    "bgcolor": "white",
    "pad": "0.5",
    "nodesep": "0.8",
    "ranksep": "1.5"
}

with Diagram(
    "RHOAI Baseline - Functional Components (Namespace-Based)",
    show=False,
    direction="TB",
    filename="output/baseline-rhoai-functional-components",
    graph_attr=graph_attr
):

    # ========== PERSONAS ==========
    with Cluster("Users"):
        data_scientist = Users("Data Scientist")
        mlops_engineer = Users("MLOps Engineer")

    # ========== EXTERNAL INTEGRATION ==========
    with Cluster("Infrastructure Dependencies (External)"):
        idp = Server("Identity Provider\n(Keycloak/LDAP)")
        git = Github("Git Repository\n(GitHub/GitLab)")
        s3_storage = Ceph("Object Storage\n(S3/Ceph RGW)")
        external_db = PostgreSQL("External Database\n(MariaDB/MySQL)")

    ocp_api = APIServer("OpenShift\nAPI Server")
    router = Ingress("OpenShift Router")

    # ========== LAYER 1: MANAGEMENT & OPERATORS ==========
    with Cluster("LAYER 1: Management & Operators"):

        # Master Operator
        with Cluster("redhat-ods-operator"):
            rhoai_operator = Helm("Red Hat OpenShift AI\nOperator")

        with Cluster("redhat-ods-applications"):

            # Dashboard
            dashboard = Python("RHOAI Dashboard")

            # Row 1: Common Controllers
            with Cluster("Common Controllers"):
                dsp_operator = Helm("Data Science Pipelines\nOperator")
                kserve_operator = Helm("KServe\nController")
                trustyai_operator = Helm("TrustyAI\nOperator")
                modelreg_operator = Helm("Model Registry\nOperator")
                notebook_controller = Helm("Notebook\nController")

            # Row 2: Model & Framework Support
            with Cluster("Model & Framework Support"):
                ray_operator = Helm("KubeRay\nOperator")
                training_operator = Helm("Kubeflow Training\nOperator")
                kueue_operator = Helm("Kueue Operator\n(Red Hat build)")

    # ========== LAYER 2: USER WORKLOADS ==========
    with Cluster("LAYER 2: Execution Layer (User Workloads)"):

        with Cluster("AI Projects (User Namespaces)"):
            # Main Workloads
            workbenches = Python("Workbenches\n(Jupyter, VSCode, RStudio)")
            pipeline_server = Mlflow("AI Pipelines\nServer")
            model_serving = Server("Model Serving\n(KServe)")
            trusty_service = Python("TrustyAI Service")

            # Ephemeral Workloads
            pipeline_runs = Python("AI Pipeline\nRuns")

            # Training Jobs
            training_jobs = Python("Training Jobs\n(PyTorch, TensorFlow)")
            ray_cluster = Python("Ray Cluster\n(Distributed)")

            # Storage
            pvc = Ceph("Persistent Volume\nClaims")

        with Cluster("rhoai-model-registries"):
            model_registry = Mlflow("Model Registry")

    # ========== SIDE: OBSERVABILITY ==========
    with Cluster("redhat-ods-monitoring"):
        with Cluster("Data Science Monitoring Stack"):
            prometheus_ds = Prometheus("Prometheus\n(Data Science)")
            collector_ds = Prometheus("Data Science\nCollector")
            alertmanager_ds = Prometheus("Alertmanager")

    # ========== LAYER 3: ACCELERATOR MANAGEMENT ==========
    with Cluster("Accelerator Management"):
        accelerator_profiles = Helm("Accelerator Profiles\n(GPU/TPU Config)")
        gpu_nodes = Server("GPU Worker Nodes")

    # =========================================================
    # CONNECTIONS
    # =========================================================

    # --- 1. USER ACCESS (Green = API requests) ---
    data_scientist >> Edge(color="green") >> router
    router >> Edge(color="green") >> dashboard
    data_scientist >> Edge(color="green", label="launches") >> workbenches
    mlops_engineer >> Edge(color="green", label="registers models") >> model_registry

    # --- 2. AUTHENTICATION ---
    router >> Edge(label="SSO") >> idp

    # --- 3. OPERATOR HIERARCHY (Orange = Management) ---
    ocp_api >> Edge(color="orange", style="bold") >> rhoai_operator
    rhoai_operator >> Edge(color="orange", style="bold", label="manages") >> dashboard
    rhoai_operator >> Edge(color="orange") >> dsp_operator
    rhoai_operator >> Edge(color="orange") >> kserve_operator
    rhoai_operator >> Edge(color="orange") >> trustyai_operator
    rhoai_operator >> Edge(color="orange") >> modelreg_operator
    rhoai_operator >> Edge(color="orange") >> notebook_controller
    rhoai_operator >> Edge(color="orange") >> ray_operator
    rhoai_operator >> Edge(color="orange") >> training_operator
    rhoai_operator >> Edge(color="orange") >> kueue_operator

    # --- 4. PROVISIONING (Controllers -> Workloads) ---
    notebook_controller >> Edge(label="manages") >> workbenches
    dsp_operator >> Edge(label="manages") >> pipeline_server
    kserve_operator >> Edge(label="manages") >> model_serving
    modelreg_operator >> Edge(label="manages") >> model_registry
    trustyai_operator >> Edge(label="manages") >> trusty_service
    training_operator >> Edge(label="manages") >> training_jobs
    ray_operator >> Edge(label="manages") >> ray_cluster

    # --- 5. DASHBOARD CONFIGURATION ---
    dashboard >> Edge(label="user config") >> workbenches
    dashboard >> Edge(label="user config") >> pipeline_server

    # --- 6. WORKLOAD FLOWS (Blue = Data flows) ---
    workbenches >> Edge(color="blue", label="sync code") >> git
    workbenches >> Edge(color="blue", label="mount data") >> pvc
    pipeline_server >> Edge(label="spawns") >> pipeline_runs
    pipeline_runs >> Edge(color="blue", label="artifacts") >> s3_storage

    # Training workflow
    pipeline_runs >> Edge(label="submit") >> training_jobs
    training_jobs >> Edge(label="request GPUs") >> kueue_operator
    kueue_operator >> Edge(label="allocate") >> accelerator_profiles
    accelerator_profiles >> Edge(label="configure") >> gpu_nodes
    training_jobs >> Edge(color="blue", label="run on") >> gpu_nodes

    # Distributed computing
    pipeline_runs >> Edge(label="submit") >> ray_cluster
    ray_cluster >> Edge(color="blue", label="use GPUs") >> gpu_nodes

    # Model serving
    training_jobs >> Edge(color="blue", label="register model") >> model_registry
    model_registry >> Edge(color="blue", label="deploy") >> model_serving
    model_serving >> Edge(color="blue", label="fetch models") >> s3_storage
    model_serving >> Edge(color="blue", label="inference on") >> gpu_nodes

    # TrustyAI monitoring
    model_serving >> Edge(label="prediction data") >> trusty_service

    # --- 7. DATABASE DEPENDENCIES ---
    trusty_service >> Edge(label="persist data") >> external_db
    model_registry >> Edge(label="metadata") >> external_db
    pipeline_server >> Edge(label="metadata") >> external_db

    # --- 8. OBSERVABILITY (Purple = Monitoring) ---
    collector_ds >> Edge(color="purple", style="dotted", label="scrapes") >> model_serving
    collector_ds >> Edge(color="purple", style="dotted", label="scrapes") >> trusty_service
    collector_ds >> Edge(color="purple", style="dotted", label="scrapes") >> workbenches
    prometheus_ds << Edge(color="purple", style="dotted", label="ingests") << collector_ds
    prometheus_ds >> alertmanager_ds

    # --- 9. STORAGE INTEGRATION ---
    workbenches >> Edge(color="blue") >> pvc
    pipeline_server >> Edge(color="blue") >> pvc

print("✓ Generated: output/baseline-rhoai-functional-components.png")
print("  → Namespace-based layers: redhat-ods-operator → redhat-ods-applications → AI Projects")
print("  → Color-coded: Orange=management, Purple=observability, Green=API, Blue=data")
