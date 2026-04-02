"""
Common - Shared Services (Template)

Shows shared services used across all environments:
- Central GitOps / Fleet Management
- Aggregated monitoring
- Central container registry
- Backup infrastructure

Customize based on customer's shared services strategy.
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.infra import Master
from diagrams.onprem.gitops import Argocd
from diagrams.onprem.monitoring import Prometheus, Grafana
from diagrams.onprem.registry import Harbor
from diagrams.onprem.storage import Ceph

graph_attr = {
    "fontsize": "16",
    "bgcolor": "white",
    "pad": "0.5",
    "ranksep": "1.5"
}

with Diagram(
    "Common - Shared Services (Template)",
    show=False,
    direction="TB",
    filename="output/engagement-common-shared-services",
    graph_attr=graph_attr
):

    with Cluster("Shared Services Cluster"):

        with Cluster("Fleet Management"):
            fleet_gitops = Argocd("Fleet GitOps\n(Multi-cluster)")

        with Cluster("Central Registry"):
            registry = Harbor("Container Registry\n(Quay/Harbor)")

        with Cluster("Aggregated Observability"):
            central_prom = Prometheus("Observability Hub")
            central_grafana = Grafana("Central Dashboards")

            central_prom >> central_grafana

        with Cluster("Backup Services"):
            backup = Ceph("Centralized Backup\n(Velero/OADP)")

    with Cluster("Environment Clusters"):
        prod_cluster = Master("Production")
        preprod_cluster = Master("Pre-Production")
        sandbox_cluster = Master("Sandbox")

    # GitOps manages all clusters
    fleet_gitops >> Edge(label="deploy configs") >> [prod_cluster, preprod_cluster, sandbox_cluster]

    # All clusters use central registry
    [prod_cluster, preprod_cluster, sandbox_cluster] >> Edge(label="pull images") >> registry

    # Metrics aggregation
    [prod_cluster, preprod_cluster, sandbox_cluster] >> Edge(label="forward metrics", style="dotted") >> central_prom

    # Backup
    [prod_cluster, preprod_cluster, sandbox_cluster] >> Edge(label="backup", style="dashed") >> backup

print("✓ Generated: output/engagement-common-shared-services.png")
print("NOTE: TEMPLATE - Customize based on customer's shared services architecture")
