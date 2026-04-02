"""
OpenShift CI/CD Pipeline Architecture

Demonstrates a complete CI/CD pipeline using:
- OpenShift Pipelines (Tekton)
- OpenShift GitOps (ArgoCD)
- Image registry (Quay)
- Source code management integration
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.vcs import Github, Gitlab
from diagrams.onprem.gitops import Argocd
from diagrams.onprem.ci import Jenkins
from diagrams.k8s.compute import Pod, Deployment
from diagrams.k8s.controlplane import APIServer
from diagrams.onprem.registry import Harbor
from diagrams.onprem.monitoring import Prometheus

graph_attr = {
    "fontsize": "16",
    "bgcolor": "white",
    "pad": "0.5"
}

with Diagram(
    "OpenShift CI/CD Pipeline",
    show=False,
    direction="LR",
    filename="output/cicd-pipeline",
    graph_attr=graph_attr
):

    # Source
    with Cluster("Source Code"):
        github = Github("GitHub/GitLab")
        config_repo = Gitlab("Config Repo")

    with Cluster("OpenShift Cluster"):

        api = APIServer("OpenShift API")

        with Cluster("CI - OpenShift Pipelines (Tekton)"):
            with Cluster("Pipeline Execution"):
                pipeline = Pod("Pipeline")

                with Cluster("Tasks"):
                    task_clone = Pod("Git Clone")
                    task_build = Pod("Build (S2I/Buildah)")
                    task_test = Pod("Run Tests")
                    task_scan = Pod("Security Scan")
                    task_push = Pod("Push Image")

                pipeline >> [task_clone, task_build, task_test, task_scan, task_push]

        with Cluster("Image Registry"):
            quay = Harbor("Quay Registry")

        with Cluster("CD - OpenShift GitOps (ArgoCD)"):
            argocd = Argocd("ArgoCD")

            with Cluster("ArgoCD Applications"):
                app_dev = Pod("App: Dev")
                app_staging = Pod("App: Staging")
                app_prod = Pod("App: Prod")

        with Cluster("Development"):
            dev_deploy = Deployment("Dev Deployment")
            dev_pods = Pod("Dev Pods")

        with Cluster("Staging"):
            staging_deploy = Deployment("Staging Deployment")
            staging_pods = Pod("Staging Pods")

        with Cluster("Production"):
            prod_deploy = Deployment("Prod Deployment")
            prod_pods = [Pod(f"Prod Pod {i}") for i in range(3)]

        with Cluster("Monitoring"):
            prometheus = Prometheus("Prometheus")

    # CI Flow
    github >> Edge(label="1. webhook") >> pipeline
    task_clone >> Edge(label="clone") >> github
    task_build >> Edge(label="build image") >> task_test
    task_test >> task_scan
    task_scan >> Edge(label="2. push") >> task_push
    task_push >> Edge(label="3. push image") >> quay

    # Update config
    task_push >> Edge(label="4. update tag", style="dashed") >> config_repo

    # CD Flow
    config_repo >> Edge(label="5. poll/webhook") >> argocd
    argocd >> [app_dev, app_staging, app_prod]

    quay >> dev_deploy
    quay >> staging_deploy
    quay >> prod_deploy

    app_dev >> Edge(label="6. sync") >> dev_deploy >> dev_pods
    app_staging >> Edge(label="7. sync (auto)") >> staging_deploy >> staging_pods
    app_prod >> Edge(label="8. sync (manual)") >> prod_deploy >> prod_pods

    # Monitoring
    dev_pods >> Edge(label="metrics") >> prometheus
    staging_pods >> Edge(label="metrics") >> prometheus
    prod_pods[0] >> Edge(label="metrics") >> prometheus

print("✓ Generated: output/cicd-pipeline.png")
