"""
AI Platform Engagement - Environment Landscape Overview

High-level view of all environments in the AI platform engagement.
This diagram shows the relationship between Production, Pre-production, and Sandbox environments.

Customize this template based on customer requirements:
- Number of environments
- Isolation strategy
- Shared services approach
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.infra import Master
from diagrams.k8s.network import Service
from diagrams.onprem.client import Users
from diagrams.onprem.gitops import Argocd
from diagrams.onprem.monitoring import Prometheus

graph_attr = {
    "fontsize": "16",
    "bgcolor": "white",
    "pad": "0.5",
    "ranksep": "1.5"
}

with Diagram(
    "AI Platform - Environment Landscape",
    show=False,
    direction="TB",
    filename="output/engagement-00-environment-landscape",
    graph_attr=graph_attr
):

    with Cluster("External Users"):
        business_users = Users("Business Users\n(Production Apps)")
        internal_users = Users("Internal Users\n(QA, Testing)")
        data_scientists = Users("Data Scientists\n(Development)")

    with Cluster("Shared Services (Cross-Environment)"):
        central_gitops = Argocd("Central GitOps\n(Fleet Management)")
        central_monitoring = Prometheus("Central Monitoring\n(Aggregated)")
        central_registry = Service("Central Container\nRegistry")
        central_idp = Service("Corporate IDP\n(SSO)")

    with Cluster("Production Environment"):
        with Cluster("Production Cluster"):
            prod_ocp = Master("OCP Cluster\n(Production)")
            prod_rhoai = Service("RHOAI Platform\n(Production)")

            prod_ocp >> prod_rhoai

    with Cluster("Pre-Production Environment"):
        with Cluster("Pre-Prod Cluster (Shared: QA + Test)"):
            preprod_ocp = Master("OCP Cluster\n(Pre-Production)")
            preprod_rhoai = Service("RHOAI Platform\n(QA/Test)")

            preprod_ocp >> preprod_rhoai

    with Cluster("Sandbox Environment"):
        with Cluster("Sandbox Cluster"):
            sandbox_ocp = Master("OCP Cluster\n(Sandbox)")
            sandbox_rhoai = Service("RHOAI Platform\n(Development)")

            sandbox_ocp >> sandbox_rhoai

    # User access
    business_users >> Edge(label="access prod apps") >> prod_rhoai
    internal_users >> Edge(label="QA/testing") >> preprod_rhoai
    data_scientists >> Edge(label="experimentation") >> sandbox_rhoai

    # Shared services integration
    central_idp >> Edge(label="SSO", style="dashed") >> [prod_ocp, preprod_ocp, sandbox_ocp]
    central_gitops >> Edge(label="deploy", style="dashed") >> [prod_ocp, preprod_ocp, sandbox_ocp]
    [prod_ocp, preprod_ocp, sandbox_ocp] >> Edge(label="metrics", style="dotted") >> central_monitoring

    # Image promotion flow
    sandbox_rhoai >> Edge(label="1. develop & test") >> central_registry
    central_registry >> Edge(label="2. promote") >> preprod_rhoai
    preprod_rhoai >> Edge(label="3. validate") >> central_registry
    central_registry >> Edge(label="4. promote to prod") >> prod_rhoai

    # Environment isolation
    prod_ocp >> Edge(label="ISOLATED\n(no direct access)", color="red", style="bold") >> sandbox_ocp
    preprod_ocp >> Edge(label="ISOLATED\n(no direct access)", color="red", style="bold") >> sandbox_ocp

print("✓ Generated: output/engagement-00-environment-landscape.png")
print("NOTE: This is a TEMPLATE - customize for your customer engagement")
