"""
Sandbox Environment - Functional Architecture (Template)

Sandbox for data scientist experimentation with flexible policies.
Isolated from production and pre-production environments.
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.controlplane import APIServer
from diagrams.k8s.network import Service
from diagrams.onprem.client import Users
from diagrams.onprem.vcs import Github

graph_attr = {
    "fontsize": "16",
    "bgcolor": "white",
    "pad": "0.5"
}

with Diagram(
    "Sandbox - Functional Architecture (Template)",
    show=False,
    direction="TB",
    filename="output/engagement-03-sandbox-functional",
    graph_attr=graph_attr
):

    data_scientists = Users("Data Scientists")
    git = Github("Git (Experiments)")

    with Cluster("Sandbox Cluster"):
        api = APIServer("OCP API")
        rhoai = Service("RHOAI\n(Full Access)")

        with Cluster("Self-Service Projects"):
            user_projects = Service("Data Science Projects\n(User-created)")

    data_scientists >> rhoai
    rhoai >> user_projects
    user_projects >> git

print("✓ Generated: output/engagement-03-sandbox-functional.png")
print("NOTE: TEMPLATE - Sandbox should allow experimentation without impacting other environments")
