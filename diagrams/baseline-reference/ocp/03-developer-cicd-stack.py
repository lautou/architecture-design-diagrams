"""
OpenShift Container Platform - Developer & CI/CD Stack Baseline

Namespace-based layered architecture for developer experience:
- GitOps Operators (openshift-gitops-operator, openshift-gitops)
- Pipeline Operators (openshift-pipelines, openshift-builds)
- Developer Workspaces (openshift-operators)

Color-coded connections:
- Orange: Operator management
- Green: Git/source code flows
- Blue: Image/artifact flows
- Purple: Deployment flows

Note: Shows actual namespace organization
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.controlplane import APIServer
from diagrams.onprem.vcs import Github, Gitlab
from diagrams.programming.language import Python
from diagrams.onprem.client import Users
from diagrams.onprem.compute import Server
from diagrams.custom import Custom
import os

# Get absolute paths for icons
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(BASE_DIR, '../../..')
OPERATOR_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Technology icons/operator/Technology_icon-Red_Hat-operator-Standard-RGB.Large_icon_transparent.png")
GITOPS_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Technology icons/Red Hat OpenShift GitOps/Technology_icon-Red_Hat-OpenShift_GitOps-Standard-RGB.Large_icon_transparent.png")
PIPELINES_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Technology icons/Red Hat OpenShift Pipelines/Technology_icon-Red_Hat-OpenShift_Pipelines-Standard-RGB.Large_icon_transparent.png")
BUILDS_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Technology icons/Builds for Red Hat OpenShift/Technology_icon-Red_Hat-OpenShift_Builds-Standard-RGB.Large_icon_transparent.png")

graph_attr = {
    "fontsize": "16",
    "bgcolor": "white",
    "pad": "0.5",
    "nodesep": "1.0",
    "ranksep": "1.8"
}

with Diagram(
    "OCP Baseline - Developer & CI/CD Stack (Namespace-Based)",
    show=False,
    direction="LR",
    filename="output/baseline-ocp-03-developer-cicd-stack",
    graph_attr=graph_attr
):

    # ========== PERSONAS ==========
    with Cluster("Users"):
        developer = Users("\nDeveloper")
        platform_engineer = Users("\nPlatform Engineer")

    # ========== EXTERNAL ==========
    with Cluster("External Systems"):
        source_repo = Github("\nSource Repository\n(GitHub/GitLab)")
        config_repo = Gitlab("\nConfig Repository\n(GitOps)")
        external_registry = Server("\nExternal Registry\n(Quay, Harbor)")

    api = APIServer("\nOpenShift\nAPI Server")

    # ========== GITOPS - CONTINUOUS DELIVERY ==========
    with Cluster("GitOps - Continuous Delivery"):

        with Cluster("openshift-gitops-operator"):
            gitops_operator = Custom("\nGitOps Operator", GITOPS_ICON)

        with Cluster("openshift-gitops"):
            argocd_server = Custom("\nArgoCD Server", GITOPS_ICON)
            argocd_apps = Server("\nArgoCD Applications\n(App of Apps)")
            argocd_appsets = Server("\nApplicationSets")

    # ========== PIPELINES - CONTINUOUS INTEGRATION ==========
    with Cluster("Pipelines - Continuous Integration"):

        with Cluster("openshift-pipelines"):
            pipelines_operator = Custom("\nPipelines Operator\n(Tekton)", PIPELINES_ICON)

            with Cluster("Pipeline Execution"):
                tekton_pipeline = Custom("\nTekton Pipeline", PIPELINES_ICON)
                event_listener = Server("\nEventListener\n(Webhooks)")
                pipeline_runs = Server("\nPipelineRuns")

    # ========== BUILDS ==========
    with Cluster("Image Builds"):

        with Cluster("openshift-builds"):
            builds_operator = Custom("\nBuilds Operator\n(Shipwright)", BUILDS_ICON)

            with Cluster("Build Strategies"):
                s2i_build = Server("\nSource-to-Image")
                buildah_build = Server("\nBuildah\n(Dockerfile)")
                buildpacks = Server("\nCloud Native\nBuildpacks")

    # ========== DEVELOPER WORKSPACE ==========
    with Cluster("Developer Workspace"):

        with Cluster("openshift-operators"):
            devworkspace_operator = Custom("\nDevWorkspace\nOperator", OPERATOR_ICON)
            web_terminal_operator = Custom("\nWeb Terminal\nOperator", OPERATOR_ICON)

            with Cluster("Developer Tools"):
                cloud_ide = Python("\nCloud IDE\n(DevSpaces)")
                web_terminal = Python("\nWeb Terminal")

    # ========== REGISTRY ==========
    with Cluster("openshift-image-registry"):
        internal_registry = Server("\nInternal Registry")

    # ========== APPLICATION DEPLOYMENTS ==========
    with Cluster("User Namespaces"):
        applications = Server("\nApplications\n(Deployments)")

    # =========================================================
    # CONNECTIONS
    # =========================================================

    # --- OPERATOR MANAGEMENT (Orange) ---
    api >> Edge(color="orange") >> gitops_operator
    api >> Edge(color="orange") >> pipelines_operator
    api >> Edge(color="orange") >> builds_operator
    api >> Edge(color="orange") >> devworkspace_operator
    api >> Edge(color="orange") >> web_terminal_operator

    gitops_operator >> Edge(color="orange") >> argocd_server
    pipelines_operator >> Edge(color="orange") >> [tekton_pipeline, event_listener]
    builds_operator >> Edge(color="orange") >> [s2i_build, buildah_build, buildpacks]
    devworkspace_operator >> Edge(color="orange") >> cloud_ide
    web_terminal_operator >> Edge(color="orange") >> web_terminal

    # --- USER ACCESS (Green) ---
    developer >> Edge(color="green", label="access") >> cloud_ide
    developer >> Edge(color="green", label="access") >> web_terminal
    platform_engineer >> Edge(color="green", label="configure") >> argocd_server

    # --- GITOPS FLOW (Purple = Deployment) ---
    config_repo >> Edge(color="purple", label="1. poll/webhook") >> argocd_server
    argocd_server >> argocd_apps
    argocd_server >> argocd_appsets
    argocd_apps >> Edge(color="purple", label="2. sync") >> api
    api >> Edge(color="purple", label="3. deploy") >> applications

    # --- CI PIPELINE FLOW ---
    # Trigger
    source_repo >> Edge(color="green", label="1. webhook") >> event_listener
    event_listener >> Edge(label="2. trigger") >> tekton_pipeline
    tekton_pipeline >> pipeline_runs

    # Build process
    pipeline_runs >> Edge(color="green", label="3. clone") >> source_repo
    pipeline_runs >> Edge(label="4. build") >> [s2i_build, buildah_build, buildpacks]

    # Image push
    s2i_build >> Edge(color="blue", label="5. push") >> internal_registry
    buildah_build >> Edge(color="blue", label="5. push") >> internal_registry
    buildpacks >> Edge(color="blue", label="5. push") >> internal_registry

    # External registry option
    pipeline_runs >> Edge(color="blue", style="dashed", label="push") >> external_registry

    # --- IMAGE TRIGGER ---
    internal_registry >> Edge(color="purple", label="6. image change") >> argocd_apps

    # --- DEVELOPER WORKFLOW ---
    cloud_ide >> Edge(color="green", label="commit") >> source_repo
    cloud_ide >> Edge(color="green", label="test deploy") >> api
    web_terminal >> Edge(color="green", label="oc/kubectl") >> api

    # --- REGISTRY SYNC ---
    internal_registry >> Edge(style="dotted", label="mirror") >> external_registry

print("✓ Generated: output/baseline-ocp-03-developer-cicd-stack.png")
print("  → Namespace-based: openshift-gitops → openshift-pipelines → openshift-builds")
print("  → Color-coded: Orange=management, Green=source, Blue=images, Purple=deployment")
