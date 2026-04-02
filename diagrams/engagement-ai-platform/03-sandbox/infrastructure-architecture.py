"""
Sandbox Environment - Infrastructure Architecture (Template)

Smaller infrastructure footprint for development and experimentation.
May use single control plane, reduced HA requirements.
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.infra import Master, Node
from diagrams.onprem.storage import Ceph

graph_attr = {
    "fontsize": "16",
    "bgcolor": "white",
    "pad": "0.5"
}

with Diagram(
    "Sandbox - Infrastructure Architecture (Template)",
    show=False,
    direction="TB",
    filename="output/engagement-03-sandbox-infrastructure",
    graph_attr=graph_attr
):

    with Cluster("Sandbox Cluster"):
        master = Master("Master\n(Single or 3x)")
        workers = [Node(f"Worker {i+1}") for i in range(2)]
        gpu_worker = Node("GPU Worker\n(Shared)")
        storage = Ceph("Storage\n(Lower tier)")

        master >> workers
        master >> gpu_worker

print("✓ Generated: output/engagement-03-sandbox-infrastructure.png")
print("NOTE: TEMPLATE - Cost-optimized for development, may use spot instances or lower-tier hardware")
