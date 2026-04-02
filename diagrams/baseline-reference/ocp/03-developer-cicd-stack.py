"""
OpenShift Container Platform - Developer & CI/CD Stack Baseline

This diagram shows the developer experience and CI/CD components:
- OpenShift GitOps (ArgoCD)
- OpenShift Pipelines (Tekton)
- Builds for OpenShift
- Developer Workspaces
- Integration with external Git and registries

Note: No pod-level representation - focus on logical components and workflows
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.controlplane import APIServer
from diagrams.k8s.network import Service
from diagrams.onprem.gitops import Argocd
from diagrams.onprem.vcs import Github, Gitlab
from diagrams.onprem.registry import Harbor
from diagrams.onprem.ci import Jenkins

graph_attr = {
    "fontsize": "16",
    "bgcolor": "white",
    "pad": "0.5",
    "nodesep": "1.0",
    "ranksep": "1.2"
}

with Diagram(
    "OCP Baseline - Developer & CI/CD Stack",
    show=False,
    direction="LR",
    filename="output/baseline-ocp-03-developer-cicd-stack",
    graph_attr=graph_attr
):

    with Cluster("External Source Control"):
        git = Github("Git Repository\n(GitHub/GitLab/Gitea)")
        config_repo = Gitlab("Config Repository\n(GitOps)")

    with Cluster("External Registry"):
        external_registry = Harbor("External Registry\n(Quay, Harbor, etc.)")

    api = APIServer("OpenShift\nAPI Server")

    with Cluster("GitOps - Continuous Delivery"):
        gitops_operator = Service("OpenShift GitOps\nOperator")

        with Cluster("ArgoCD Instance"):
            argocd = Argocd("ArgoCD Server")
            argocd_apps = Service("ArgoCD Applications\n(App of Apps)")

            gitops_operator >> argocd
            argocd >> argocd_apps

    with Cluster("Pipelines - Continuous Integration"):
        pipelines_operator = Service("OpenShift Pipelines\nOperator (Tekton)")

        with Cluster("Pipeline Execution"):
            pipeline = Service("Pipeline\n(Tasks & Steps)")
            triggers = Service("EventListener\n(Webhooks)")

            pipelines_operator >> [pipeline, triggers]

    with Cluster("Builds"):
        builds_operator = Service("Builds for OpenShift\nOperator (Shipwright)")

        with Cluster("Build Strategies"):
            build_s2i = Service("Source-to-Image\n(S2I)")
            build_buildah = Service("Buildah\n(Dockerfile)")
            build_buildpacks = Service("Cloud Native\nBuildpacks")

            builds_operator >> [build_s2i, build_buildah, build_buildpacks]

    with Cluster("Internal Image Registry"):
        internal_registry = Harbor("OpenShift\nInternal Registry")

    with Cluster("Developer Workspace"):
        devworkspace_operator = Service("DevWorkspace\nOperator")
        web_terminal_operator = Service("Web Terminal\nOperator")

        with Cluster("Developer Tools"):
            ide = Service("Cloud IDE\n(DevSpaces/Eclipse Che)")
            terminal = Service("Web Terminal")

            devworkspace_operator >> ide
            web_terminal_operator >> terminal

    with Cluster("Application Deployments"):
        applications = Service("Applications\n(Deployments, StatefulSets)")

    # API integration
    api >> [gitops_operator, pipelines_operator, builds_operator, devworkspace_operator, web_terminal_operator]

    # GitOps flow
    config_repo >> Edge(label="1. poll/webhook") >> argocd
    argocd >> Edge(label="2. sync") >> api
    api >> Edge(label="3. deploy") >> applications

    # CI Pipeline flow
    git >> Edge(label="1. webhook") >> triggers
    triggers >> Edge(label="2. trigger") >> pipeline
    pipeline >> Edge(label="3. clone source") >> git
    pipeline >> Edge(label="4. build") >> [build_s2i, build_buildah, build_buildpacks]
    [build_s2i, build_buildah, build_buildpacks] >> Edge(label="5. push image") >> internal_registry

    # Pipeline can also push to external registry
    pipeline >> Edge(label="push", style="dashed") >> external_registry

    # Image triggers
    internal_registry >> Edge(label="6. image change trigger") >> argocd_apps

    # Developer workspace integration
    ide >> Edge(label="commit code") >> git
    ide >> Edge(label="deploy/test") >> api
    terminal >> Edge(label="oc/kubectl commands") >> api

    # Registry synchronization
    internal_registry >> Edge(label="mirror", style="dotted") >> external_registry

print("✓ Generated: output/baseline-ocp-03-developer-cicd-stack.png")
