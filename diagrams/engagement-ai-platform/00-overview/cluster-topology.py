"""
AI Platform Engagement - Cluster Topology Strategy

Shows the cluster distribution strategy and rationale.
This is a TEMPLATE to be customized based on customer requirements.

Common patterns:
- Option 1: Dedicated cluster per environment (max isolation, higher cost)
- Option 2: Shared non-prod cluster (cost optimized)
- Option 3: Multi-tenant shared cluster with namespace isolation

Adapt based on: budget, compliance, team structure, data sensitivity
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.infra import Master, Node
from diagrams.k8s.network import NetworkPolicy
from diagrams.onprem.network import Internet

graph_attr = {
    "fontsize": "16",
    "bgcolor": "white",
    "pad": "0.5",
    "ranksep": "1.5"
}

with Diagram(
    "AI Platform - Cluster Topology Strategy",
    show=False,
    direction="LR",
    filename="output/engagement-00-cluster-topology",
    graph_attr=graph_attr
):

    with Cluster("Production Cluster (Dedicated)"):
        with Cluster("Control Plane (HA)"):
            prod_masters = [Master(f"Master") for _ in range(3)]

        with Cluster("Worker Nodes"):
            prod_cpu = Node("CPU Workers\n(3x Standard)")
            prod_gpu = Node("GPU Workers\n(2x GPU)")

        with Cluster("Network Isolation"):
            prod_netpol = NetworkPolicy("Strict Network\nPolicies")

        prod_netpol >> [prod_cpu, prod_gpu]

    with Cluster("Pre-Production Cluster (Shared: QA + Test)"):
        with Cluster("Control Plane (HA)"):
            preprod_masters = [Master(f"Master") for _ in range(3)]

        with Cluster("Worker Nodes"):
            preprod_cpu = Node("CPU Workers\n(2x Standard)")
            preprod_gpu = Node("GPU Workers\n(1x GPU)")

        with Cluster("Namespace Isolation"):
            ns_qa = NetworkPolicy("QA Namespace\n(Isolated)")
            ns_test = NetworkPolicy("Test Namespace\n(Isolated)")

        ns_qa >> preprod_cpu
        ns_test >> preprod_cpu
        ns_qa >> preprod_gpu
        ns_test >> preprod_gpu

    with Cluster("Sandbox Cluster (Dedicated)"):
        with Cluster("Control Plane"):
            sandbox_masters = Master("Master\n(Single Node)")

        with Cluster("Worker Nodes"):
            sandbox_cpu = Node("CPU Workers\n(2x Standard)")
            sandbox_gpu = Node("GPU Workers\n(1x GPU)")

        with Cluster("Flexible Access"):
            sandbox_policy = NetworkPolicy("Relaxed Policies\n(Development)")

        sandbox_policy >> [sandbox_cpu, sandbox_gpu]

    internet = Internet("Internet /\nExternal Access")

    # Production - strict isolation
    internet >> Edge(label="HTTPS only\n(Firewall restricted)", color="red") >> prod_masters

    # Pre-prod - moderate access
    internet >> Edge(label="HTTPS + VPN\n(Controlled access)", color="orange") >> preprod_masters

    # Sandbox - flexible for development
    internet >> Edge(label="Developer access\n(VPN)", color="green") >> sandbox_masters

    # Cluster isolation
    prod_masters[0] >> Edge(label="NO DIRECT\nCONNECTION", color="red", style="dashed") >> sandbox_masters
    preprod_masters[0] >> Edge(label="NO DIRECT\nCONNECTION", color="red", style="dashed") >> sandbox_masters

print("✓ Generated: output/engagement-00-cluster-topology.png")
print("NOTE: This is a TEMPLATE - adapt cluster sizing and isolation to customer needs")
