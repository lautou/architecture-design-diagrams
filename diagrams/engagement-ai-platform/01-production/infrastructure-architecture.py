"""
Production Environment - Infrastructure Architecture

Shows the physical/infrastructure components for the production AI platform.
Focus on infrastructure integration points: Load Balancers, Storage, Network, Compute.

Customize based on customer infrastructure:
- On-premises vs. Cloud vs. Hybrid
- Network topology and security zones
- Storage backend (SAN, NAS, Cloud Storage)
- Compute resources (bare metal, VMs, cloud instances)
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.infra import Master, Node
from diagrams.onprem.network import Nginx, Internet
from diagrams.onprem.storage import Ceph
from diagrams.onprem.compute import Server
from diagrams.onprem.security import Vault

graph_attr = {
    "fontsize": "16",
    "bgcolor": "white",
    "pad": "0.5",
    "ranksep": "1.5"
}

with Diagram(
    "Production - Infrastructure Architecture (AI Platform)",
    show=False,
    direction="TB",
    filename="output/engagement-01-production-infrastructure",
    graph_attr=graph_attr
):

    internet = Internet("Internet")

    with Cluster("DMZ / Edge Network"):
        external_lb = Nginx("External Load Balancer\n(F5/HAProxy/Cloud LB)")
        firewall = Vault("Enterprise Firewall\n& WAF")

    with Cluster("Production Data Center / Cloud Region"):

        with Cluster("Network Layer"):
            internal_lb = Nginx("Internal Load Balancer\n(API & Ingress)")
            dns_server = Server("DNS Server\n(Internal)")

        with Cluster("OpenShift Control Plane (HA)"):
            masters = [Master(f"Master {i+1}\n(4vCPU, 16GB)") for i in range(3)]

        with Cluster("Worker Nodes - Compute"):
            with Cluster("Standard Workers"):
                cpu_workers = [Node(f"Worker {i+1}\n(8vCPU, 32GB)") for i in range(3)]

            with Cluster("GPU Workers (AI/ML)"):
                gpu_workers = [Server(f"GPU Worker {i+1}\n(16vCPU, 64GB, A100)") for i in range(2)]

        with Cluster("Storage Layer"):
            with Cluster("Block Storage"):
                san = Ceph("SAN / Block Storage\n(for etcd, PVs)")

            with Cluster("Object Storage"):
                s3 = Ceph("S3-Compatible Storage\n(models, datasets)")

            with Cluster("File Storage (Optional)"):
                nas = Ceph("NFS / File Storage\n(shared workspaces)")

        with Cluster("Infrastructure Services"):
            ntp_server = Server("NTP Server")
            proxy_server = Server("Proxy Server\n(Internet access)")
            ldap_server = Server("LDAP/AD Server\n(Identity)")

    with Cluster("Backup & DR"):
        backup_storage = Ceph("Backup Storage\n(Off-site)")
        dr_site = Server("DR Site\n(Standby)")

    # External traffic flow
    internet >> Edge(label="HTTPS") >> firewall
    firewall >> Edge(label="filtered") >> external_lb
    external_lb >> Edge(label="route") >> internal_lb

    # Load balancer to control plane
    internal_lb >> Edge(label="API (6443)") >> masters
    internal_lb >> Edge(label="Ingress (443)") >> cpu_workers

    # DNS resolution
    dns_server >> masters

    # Control plane HA
    masters[0] >> Edge(label="quorum", style="dashed") >> masters[1]
    masters[1] >> Edge(label="quorum", style="dashed") >> masters[2]

    # Worker node management
    masters[0] >> Edge(label="orchestrate") >> cpu_workers
    masters[0] >> Edge(label="schedule GPU jobs") >> gpu_workers

    # Storage connections
    masters[0] >> Edge(label="etcd data") >> san
    cpu_workers[0] >> Edge(label="PVs") >> san
    cpu_workers[1] >> Edge(label="PVs") >> nas
    gpu_workers[0] >> Edge(label="model storage") >> s3

    # Infrastructure services
    masters[0] >> Edge(label="time sync", style="dotted") >> ntp_server
    cpu_workers[0] >> Edge(label="time sync", style="dotted") >> ntp_server
    gpu_workers[0] >> Edge(label="time sync", style="dotted") >> ntp_server
    cpu_workers[0] >> Edge(label="outbound traffic", style="dotted") >> proxy_server
    masters[0] >> Edge(label="authentication", style="dotted") >> ldap_server

    # Backup
    san >> Edge(label="backup", style="dashed") >> backup_storage
    s3 >> Edge(label="backup", style="dashed") >> backup_storage
    masters[0] >> Edge(label="replicate config", style="dashed") >> dr_site

print("✓ Generated: output/engagement-01-production-infrastructure.png")
print("NOTE: This is a TEMPLATE - Customize with customer-specific infrastructure")
print("      Consider: on-prem vs cloud, network zones, storage backends, compute types")
