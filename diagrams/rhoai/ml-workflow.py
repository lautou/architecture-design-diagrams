"""
RHOAI (Red Hat OpenShift AI) ML Workflow Architecture

This diagram illustrates a typical ML workflow on RHOAI:
- Data ingestion and preparation
- Model training with distributed workloads
- Model serving and inference
- MLOps pipeline integration
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod, Job
from diagrams.k8s.storage import PV, PVC
from diagrams.k8s.network import Service
from diagrams.onprem.client import Users
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.mlops import Mlflow
from diagrams.custom import Custom
from diagrams.programming.framework import React
from diagrams.programming.language import Python

graph_attr = {
    "fontsize": "16",
    "bgcolor": "white",
    "pad": "0.5"
}

with Diagram(
    "RHOAI ML Workflow",
    show=False,
    direction="LR",
    filename="output/rhoai-ml-workflow",
    graph_attr=graph_attr
):
    data_scientist = Users("Data Scientist")
    ml_engineer = Users("ML Engineer")

    with Cluster("RHOAI Platform"):
        with Cluster("Development Environment"):
            jupyter = Python("JupyterLab")
            vscode = Python("VS Code Server")

        with Cluster("Data Pipeline"):
            with Cluster("Data Processing"):
                data_prep = Job("Data Preparation Job")
                feature_eng = Job("Feature Engineering")

        with Cluster("Model Training"):
            with Cluster("Distributed Training"):
                training_pods = [Pod("Training Pod") for _ in range(3)]
                training_job = Job("PyTorch/TensorFlow Job")
                training_job >> training_pods

        with Cluster("Model Registry"):
            model_registry = Mlflow("Model Registry")

        with Cluster("Model Serving"):
            with Cluster("Inference Runtime"):
                model_server = Service("Model Server\n(OVMS/Triton)")
                inference_pods = [Pod("Inference Pod") for _ in range(2)]
                model_server >> inference_pods

        with Cluster("Storage Layer"):
            s3_storage = PV("S3/Object Storage")
            model_storage = PVC("Model Storage")
            data_storage = PVC("Data Storage")

        with Cluster("Monitoring & Tracking"):
            prometheus = Service("Prometheus")
            grafana = Service("Grafana")
            mlflow = Mlflow("MLflow Tracking")

    with Cluster("Data Sources"):
        database = PostgreSQL("Database")
        data_lake = PV("Data Lake")

    with Cluster("Applications"):
        app = React("ML Application")

    # Workflow connections
    data_scientist >> jupyter
    jupyter >> data_prep

    database >> data_storage
    data_lake >> data_storage

    data_storage >> data_prep >> feature_eng
    feature_eng >> Edge(label="prepared data") >> training_job

    training_pods >> Edge(label="metrics") >> mlflow
    training_pods >> Edge(label="trained model") >> model_registry

    model_registry >> Edge(label="deploy") >> model_storage
    model_storage >> inference_pods

    ml_engineer >> model_server
    app >> Edge(label="inference request") >> model_server

    inference_pods >> Edge(label="metrics") >> prometheus
    prometheus >> grafana

print("✓ Generated: output/rhoai-ml-workflow.png")
