"""
Template for creating OpenShift architecture diagrams

Copy this template and customize for your specific diagram needs.
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.controlplane import APIServer
from diagrams.k8s.compute import Pod
# Add more imports as needed

# Diagram configuration
DIAGRAM_NAME = "Your Diagram Name"
OUTPUT_FILENAME = "output/your-diagram-name"
DIRECTION = "TB"  # TB (top to bottom), LR (left to right), BT, RL

# Graph styling
graph_attr = {
    "fontsize": "16",
    "bgcolor": "white",
    "pad": "0.5",
    # "splines": "spline",  # Uncomment for curved lines
}

with Diagram(
    DIAGRAM_NAME,
    show=False,
    direction=DIRECTION,
    filename=OUTPUT_FILENAME,
    graph_attr=graph_attr
):

    # Example cluster structure
    with Cluster("Cluster Name"):
        component1 = APIServer("Component 1")
        component2 = Pod("Component 2")

    # Connections
    component1 >> Edge(label="description") >> component2

print(f"✓ Generated: {OUTPUT_FILENAME}.png")
