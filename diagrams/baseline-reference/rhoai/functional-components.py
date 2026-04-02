"""
Red Hat OpenShift AI (RHOAI) - Functional Components Baseline

This diagram shows all RHOAI components available through the DataScienceCluster CR:
- Dashboard and user interface
- Workbenches (development environments)
- Data Science Pipelines
- Model Serving (KServe, ModelMesh)
- Distributed Computing (Ray, CodeFlare)
- Model Registry and TrustyAI
- Training Operator
- Integration with external systems (IDP, Git, S3, etc.)

Note: No pod-level representation - focus on logical components and data flows
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

graph_attr = {
    "fontsize": "14",
    "bgcolor": "white",
    "pad": "0.5",
    "nodesep": "0.8",
    "ranksep": "1.0"
}

with Diagram(
    "RHOAI Baseline - Functional Components (DataScienceCluster)",
    show=False,
    direction="TB",
    filename="output/baseline-rhoai-functional-components",
    graph_attr=graph_attr
):

    data_scientist = Users("Data Scientists\n& ML Engineers")

    with Cluster("External Integration Points"):
        idp = Server("Identity Provider\n(Keycloak/LDAP)")
        git = Github("Git Repository\n(GitHub/GitLab)")
        s3_storage = Ceph("Object Storage\n(S3/Ceph RGW)")
        external_db = PostgreSQL("External Database\n(PostgreSQL/MySQL)")

    ocp_api = APIServer("OpenShift\nAPI Server")
    router = Ingress("OpenShift Router")

    with Cluster("RHOAI Platform - DataScienceCluster CR"):

        rhoai_operator = Helm("RHOAI Operator")

        with Cluster("User Interface"):
            dashboard = Python("RHOAI Dashboard\n(Web Console)")

        with Cluster("Development Environments - Workbenches"):
            workbenches = Helm("Workbench Controller")

            with Cluster("Notebook Images"):
                jupyter = Python("JupyterLab")
                vscode = Python("VSCode Server")
                rstudio = Python("RStudio")

            workbenches >> [jupyter, vscode, rstudio]

        with Cluster("Data Science Pipelines"):
            dsp_operator = Helm("Data Science Pipelines\nOperator")

            with Cluster("Pipeline Components"):
                kubeflow = Mlflow("Kubeflow Pipelines\nAPI Server")
                elyra = Python("Elyra\n(Pipeline Authoring)")
                pipeline_storage = PostgreSQL("Pipeline Metadata\nDB")

            dsp_operator >> [kubeflow, elyra, pipeline_storage]

        with Cluster("Model Training"):
            training_operator = Helm("Training Operator")

            with Cluster("Distributed Training Frameworks"):
                pytorch = Python("PyTorchJob")
                tensorflow = Python("TensorFlowJob")
                xgboost = Python("XGBoostJob")
                mpi = Python("MPIJob")

            training_operator >> [pytorch, tensorflow, xgboost, mpi]

        with Cluster("Distributed Computing"):
            with Cluster("Ray"):
                ray_operator = Helm("Ray Operator")
                ray_cluster = Python("Ray Cluster\n(Head + Workers)")

                ray_operator >> ray_cluster

            with Cluster("CodeFlare"):
                codeflare_operator = Helm("CodeFlare Operator")
                codeflare_sdk = Python("CodeFlare SDK\n(Simplified API)")

                codeflare_operator >> codeflare_sdk

        with Cluster("Job Queuing & Resource Management"):
            kueue_operator = Helm("Kueue Operator\n(Red Hat build)")

            with Cluster("Queue Management"):
                cluster_queue = Helm("ClusterQueue\n(Resource Pools)")
                local_queue = Helm("LocalQueue\n(Namespace Queues)")

            kueue_operator >> [cluster_queue, local_queue]

        with Cluster("Model Serving"):
            with Cluster("KServe (Single Model)"):
                kserve = Helm("KServe Controller")
                serving_runtime = Server("Serving Runtimes\n(OVMS, vLLM, Triton)")

                kserve >> serving_runtime

            with Cluster("ModelMesh (Multi-Model)"):
                modelmesh = Helm("ModelMesh Controller")
                model_cache = Server("Model Cache\n& Routing")

                modelmesh >> model_cache

        with Cluster("Model Registry"):
            model_registry_operator = Helm("Model Registry\nOperator")

            with Cluster("Registry Components"):
                registry_api = Mlflow("Model Registry\nAPI")
                registry_db = PostgreSQL("Registry Metadata\nDB")
                registry_storage = Ceph("Model Artifacts\nStorage")

            model_registry_operator >> [registry_api, registry_db, registry_storage]

        with Cluster("Model Governance & Explainability"):
            trustyai_operator = Helm("TrustyAI Operator")

            with Cluster("TrustyAI Services"):
                explainability = Python("Model Explainability\n(LIME, SHAP)")
                fairness = Python("Fairness Metrics\n& Bias Detection")
                monitoring_trust = Mlflow("Model Monitoring")

            trustyai_operator >> [explainability, fairness, monitoring_trust]

        with Cluster("Accelerator Management"):
            accelerator_profiles = Helm("Accelerator Profiles\n(GPU/TPU Config)")

    with Cluster("OpenShift Infrastructure"):
        gpu_nodes = Server("GPU Worker Nodes\n(NVIDIA Operator)")
        odf_storage = Ceph("OpenShift Data Foundation\n(PVCs for models/data)")

    with Cluster("Monitoring & Observability"):
        prometheus = Server("Prometheus\n(UDWM)")
        grafana = Server("Grafana Dashboards")

    # User access
    data_scientist >> Edge(label="1. login (SSO)") >> idp
    idp >> Edge(label="authenticate") >> dashboard
    data_scientist >> Edge(label="2. access") >> router
    router >> dashboard

    # RHOAI operator manages all components
    ocp_api >> rhoai_operator
    rhoai_operator >> Edge(label="manage", style="dashed") >> [
        dashboard, workbenches, dsp_operator, training_operator,
        ray_operator, codeflare_operator, kueue_operator,
        kserve, modelmesh, model_registry_operator, trustyai_operator
    ]

    # Development workflow
    dashboard >> Edge(label="launch") >> workbenches
    [jupyter, vscode, rstudio] >> Edge(label="commit code") >> git
    [jupyter, vscode, rstudio] >> Edge(label="read/write data") >> s3_storage

    # Pipeline workflow
    workbenches >> Edge(label="create pipeline") >> elyra
    elyra >> Edge(label="submit") >> kubeflow
    kubeflow >> Edge(label="execute") >> training_operator
    kubeflow >> Edge(label="store metadata") >> pipeline_storage

    # Training workflow
    training_operator >> Edge(label="request GPUs") >> kueue_operator
    kueue_operator >> Edge(label="allocate resources") >> cluster_queue
    cluster_queue >> Edge(label="assign") >> gpu_nodes
    [pytorch, tensorflow, xgboost, mpi] >> Edge(label="run on") >> gpu_nodes

    # Distributed computing
    codeflare_sdk >> Edge(label="submit jobs") >> ray_cluster
    ray_cluster >> Edge(label="use GPUs") >> gpu_nodes
    kueue_operator >> Edge(label="queue") >> ray_cluster

    # Accelerator profiles
    accelerator_profiles >> Edge(label="configure") >> [training_operator, kserve, ray_cluster]

    # Model registry workflow
    training_operator >> Edge(label="register model") >> registry_api
    registry_api >> Edge(label="metadata") >> registry_db
    registry_api >> Edge(label="artifacts") >> registry_storage
    registry_storage >> s3_storage

    # Model serving
    registry_api >> Edge(label="deploy model") >> kserve
    kserve >> Edge(label="load from") >> registry_storage
    serving_runtime >> Edge(label="inference on") >> gpu_nodes
    router >> Edge(label="inference requests") >> serving_runtime

    # ModelMesh for multi-model serving
    registry_api >> Edge(label="deploy multiple") >> modelmesh
    model_cache >> s3_storage

    # TrustyAI integration
    kserve >> Edge(label="prediction data") >> trustyai_operator
    explainability >> Edge(label="analyze") >> serving_runtime
    fairness >> Edge(label="monitor") >> monitoring_trust

    # Storage integration
    [jupyter, vscode, rstudio] >> Edge(label="PVC") >> odf_storage
    pipeline_storage >> odf_storage
    registry_storage >> odf_storage

    # Data connections
    workbenches >> Edge(label="query data") >> external_db
    kubeflow >> Edge(label="data pipeline") >> external_db

    # Monitoring
    [workbenches, training_operator, kserve, ray_cluster] >> Edge(label="metrics", style="dotted") >> prometheus
    prometheus >> grafana

print("✓ Generated: output/baseline-rhoai-functional-components.png")
