"""
Pre-Production Environment - Functional Architecture (Template)

Similar to production but with shared QA/Test environments and less stringent HA requirements.
Customize based on customer pre-production strategy.
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.controlplane import APIServer
from diagrams.k8s.network import Service
from diagrams.onprem.client import Users

graph_attr = {
    "fontsize": "16",
    "bgcolor": "white",
    "pad": "0.5"
}

with Diagram(
    "Pre-Production - Functional Architecture (Template)",
    show=False,
    direction="TB",
    filename="output/engagement-02-preproduction-functional",
    graph_attr=graph_attr
):

    qa_users = Users("QA Team")
    test_users = Users("Test Automation")

    with Cluster("Pre-Production Cluster"):
        api = APIServer("OCP API")

        with Cluster("QA Namespace"):
            qa_rhoai = Service("RHOAI (QA)")
            qa_apps = Service("ML Apps (QA)")

        with Cluster("Test Namespace"):
            test_rhoai = Service("RHOAI (Test)")
            test_apps = Service("ML Apps (Test)")

    qa_users >> qa_apps
    test_users >> test_apps

print("✓ Generated: output/engagement-02-preproduction-functional.png")
print("NOTE: TEMPLATE - Expand with customer-specific pre-production requirements")
