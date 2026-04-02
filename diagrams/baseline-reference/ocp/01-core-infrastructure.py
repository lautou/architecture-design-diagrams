"""
OpenShift Container Platform - Core Infrastructure Baseline

This diagram shows the foundational OCP infrastructure components and operators:
- Control Plane and Worker Nodes (logical representation)
- Storage: OpenShift Data Foundation
- Compute: GPU and Node Feature Discovery
- Networking: DNS and base networking
- Integration points with external infrastructure

Note: No pod-level representation - focus on logical components and operators
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.controlplane import APIServer, ControllerManager, Scheduler
from diagrams.k8s.infra import Master, Node
from diagrams.onprem.network import Etcd, Nginx
from diagrams.onprem.storage import Ceph
from diagrams.onprem.compute import Server
from diagrams.k8s.ecosystem import Helm

graph_attr = {
    "fontsize": "16",
    "bgcolor": "white",
    "pad": "0.5",
    "nodesep": "1.0",
    "ranksep": "1.2"
}

with Diagram(
    "OCP Baseline - Core Infrastructure",
    show=False,
    direction="TB",
    filename="output/baseline-ocp-01-core-infrastructure",
    graph_attr=graph_attr
):

    with Cluster("External Infrastructure Integration"):
        lb = Nginx("Load Balancer\n(External)")
        dns_external = Server("DNS\n(External)")
        storage_external = Ceph("External Storage\n(Optional)")

    with Cluster("OpenShift Control Plane"):
        with Cluster("API & Management"):
            api = APIServer("API Server\n(HA: 3x)")
            scheduler = Scheduler("Scheduler")
            controller = ControllerManager("Controller Manager")

        etcd_cluster = Etcd("etcd Cluster\n(HA: 3x)")

    with Cluster("Core Operators"):
        dns_operator = Helm("DNS Operator")

    with Cluster("Compute Infrastructure"):
        with Cluster("Worker Nodes"):
            with Cluster("Standard Compute"):
                workers = Node("Worker Nodes\n(CPU workloads)")

            with Cluster("GPU Compute"):
                nfd_operator = Helm("Node Feature\nDiscovery Operator")
                gpu_operator = Helm("NVIDIA GPU\nOperator")
                gpu_nodes = Server("GPU Worker Nodes\n(AI/ML workloads)")

                nfd_operator >> Edge(label="detect features") >> gpu_nodes
                gpu_operator >> Edge(label="manage drivers") >> gpu_nodes

    with Cluster("Storage Infrastructure"):
        with Cluster("OpenShift Data Foundation (ODF)"):
            odf_operator = Helm("ODF Operator")

            with Cluster("Storage Classes"):
                sc_block = Ceph("Block (RBD)")
                sc_file = Ceph("File (CephFS)")
                sc_object = Ceph("Object (RGW/S3)")

            with Cluster("Ceph Cluster"):
                ceph = Ceph("Ceph Storage\n(MON, OSD, MDS, RGW)")

            odf_operator >> ceph
            ceph >> [sc_block, sc_file, sc_object]

    with Cluster("Machine Management"):
        machine_api = Helm("Machine API\n& Autoscaler")

    # External integration
    lb >> Edge(label="ingress traffic") >> api
    dns_external >> Edge(label="DNS resolution") >> dns_operator

    # Control plane connections
    api >> etcd_cluster
    api >> [scheduler, controller]

    # DNS operator manages cluster DNS
    dns_operator >> api

    # Machine management
    machine_api >> api
    machine_api >> Edge(label="provision") >> [workers, gpu_nodes]

    # Storage integration
    api >> odf_operator

    # External storage option
    storage_external >> Edge(label="alternative", style="dashed") >> api

    # Workload placement
    scheduler >> Edge(label="schedule workloads") >> workers
    scheduler >> Edge(label="schedule GPU workloads") >> gpu_nodes

print("✓ Generated: output/baseline-ocp-01-core-infrastructure.png")
