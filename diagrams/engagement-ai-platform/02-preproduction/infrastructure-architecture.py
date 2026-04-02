"""
Pre-Production Environment - Infrastructure Architecture (Template)

Shows infrastructure for pre-production (shared QA/Test cluster).
Typically smaller scale than production with namespace isolation.
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.infra import Master, Node
from diagrams.onprem.network import Nginx
from diagrams.onprem.storage import Ceph

graph_attr = {
    "fontsize": "16",
    "bgcolor": "white",
    "pad": "0.5"
}

with Diagram(
    "Pre-Production - Infrastructure Architecture (Template)",
    show=False,
    direction="TB",
    filename="output/engagement-02-preproduction-infrastructure",
    graph_attr=graph_attr
):

    lb = Nginx("Load Balancer")

    with Cluster("Pre-Prod Cluster"):
        masters = [Master(f"Master {i+1}") for i in range(3)]
        workers = [Node(f"Worker {i+1}") for i in range(2)]
        gpu_worker = Node("GPU Worker")
        storage = Ceph("Shared Storage")

    lb >> masters
    masters[0] >> [workers[0], gpu_worker]

print("✓ Generated: output/engagement-02-preproduction-infrastructure.png")
print("NOTE: TEMPLATE - Customize sizing based on QA/Test workload requirements")
