"""
OpenShift Container Platform - Core Infrastructure Baseline

This diagram follows namespace-based layered architecture:
- LAYER 1: Control Plane (openshift-kube-* namespaces)
- LAYER 2: Infrastructure Services (openshift-dns, openshift-ingress, etc.)
- LAYER 3: Platform Services (openshift-image-registry, openshift-authentication, etc.)
- User Workloads (user namespaces)

Color-coded connections:
- Orange: Management/hierarchy
- Green: API requests
- Blue: Data flows
- Purple: Infrastructure services

Note: Organized by actual OpenShift namespaces
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.controlplane import APIServer, ControllerManager, Scheduler
from diagrams.k8s.infra import Master, Node
from diagrams.onprem.network import Etcd, Nginx
from diagrams.onprem.storage import Ceph
from diagrams.onprem.compute import Server
from diagrams.k8s.ecosystem import Helm
from diagrams.k8s.network import Ingress
from diagrams.onprem.client import Users

graph_attr = {
    "fontsize": "16",
    "bgcolor": "white",
    "pad": "0.5",
    "nodesep": "1.0",
    "ranksep": "1.8"
}

with Diagram(
    "OCP Baseline - Core Infrastructure (Namespace-Based)",
    show=False,
    direction="TB",
    filename="output/baseline-ocp-01-core-infrastructure",
    graph_attr=graph_attr
):

    # ========== EXTERNAL ==========
    with Cluster("External Infrastructure"):
        lb_external = Nginx("Load Balancer\n(External)")
        dns_external = Server("DNS\n(External)")
        storage_external = Ceph("External Storage\n(Optional)")

    users = Users("Users/Developers")

    # ========== LAYER 1: CONTROL PLANE ==========
    with Cluster("LAYER 1: Control Plane"):

        with Cluster("openshift-kube-apiserver"):
            api = APIServer("API Server\n(HA: 3x)")

        with Cluster("Core Controllers"):
            with Cluster("openshift-etcd"):
                etcd_cluster = Etcd("etcd Cluster\n(HA: 3x)")

            with Cluster("openshift-kube-controller-manager"):
                controller = ControllerManager("Controller Manager")

            with Cluster("openshift-kube-scheduler"):
                scheduler = Scheduler("Scheduler")

    # ========== LAYER 2: NETWORK & EDGE ==========
    with Cluster("LAYER 2: Network & Edge Services"):

        with Cluster("openshift-ingress"):
            router = Ingress("Ingress Controller\n(HAProxy)")

        with Cluster("openshift-dns"):
            cluster_dns = Server("Cluster DNS\n(CoreDNS)")

        with Cluster("openshift-network-operator"):
            network_operator = Helm("Cluster Network\n(OVN-Kubernetes)")

        with Cluster("openshift-dns-operator"):
            dns_operator = Helm("DNS Operator")

    # ========== LAYER 3: PLATFORM SERVICES ==========
    with Cluster("LAYER 3: Platform Services"):

        with Cluster("openshift-image-registry"):
            internal_registry = Server("Internal Registry")

        with Cluster("openshift-authentication"):
            oauth_server = Server("OAuth Server")

        with Cluster("openshift-operator-lifecycle-manager"):
            olm = Helm("Operator Lifecycle\nManager (OLM)")

        with Cluster("openshift-machine-api"):
            machine_api = Helm("Machine API\n& Autoscaler")

    # ========== COMPUTE INFRASTRUCTURE ==========
    with Cluster("Compute Infrastructure"):

        with Cluster("Standard Worker Nodes"):
            cpu_workers = Node("CPU Workers\n(Compute)")

        with Cluster("GPU Worker Nodes"):
            with Cluster("openshift-nfd"):
                nfd_operator = Helm("Node Feature\nDiscovery Operator")

            with Cluster("nvidia-gpu-operator"):
                gpu_operator = Helm("NVIDIA GPU\nOperator")

            gpu_nodes = Server("GPU Workers\n(AI/ML)")

    # ========== STORAGE INFRASTRUCTURE ==========
    with Cluster("Storage Infrastructure"):

        with Cluster("openshift-storage"):
            with Cluster("OpenShift Data Foundation"):
                odf_operator = Helm("ODF Operator")

                with Cluster("Storage Classes"):
                    sc_block = Ceph("Block (RBD)")
                    sc_file = Ceph("File (CephFS)")
                    sc_object = Ceph("Object (RGW/S3)")

                ceph_cluster = Ceph("Ceph Storage\n(MON, OSD, MDS, RGW)")

    # ========== USER WORKLOADS ==========
    with Cluster("User Namespaces"):
        user_workloads = Server("User Workloads\n(Applications)")

    # =========================================================
    # CONNECTIONS
    # =========================================================

    # --- EXTERNAL ACCESS (Green = API/User traffic) ---
    users >> Edge(color="green", label="access") >> lb_external
    lb_external >> Edge(color="green") >> router
    router >> Edge(color="green", label="routes traffic") >> user_workloads

    users >> Edge(color="green", label="oc/kubectl") >> api

    # --- DNS INTEGRATION (Purple = Infrastructure) ---
    dns_external >> Edge(color="purple", label="resolve") >> dns_operator
    dns_operator >> Edge(color="purple") >> cluster_dns
    user_workloads >> Edge(color="purple", style="dotted", label="service discovery") >> cluster_dns

    # --- CONTROL PLANE (Orange = Management) ---
    api >> Edge(color="orange", style="bold") >> etcd_cluster
    api >> Edge(color="orange") >> controller
    api >> Edge(color="orange") >> scheduler

    # --- PLATFORM SERVICES ---
    api >> Edge(color="orange") >> [olm, machine_api, dns_operator, network_operator]

    # Authentication
    router >> Edge(label="authenticate") >> oauth_server
    oauth_server >> Edge(color="green") >> api

    # --- WORKLOAD SCHEDULING (Blue = Data/workload flows) ---
    scheduler >> Edge(color="blue", label="schedule") >> cpu_workers
    scheduler >> Edge(color="blue", label="schedule GPU jobs") >> gpu_nodes

    # Machine management
    machine_api >> Edge(label="provision") >> cpu_workers
    machine_api >> Edge(label="provision") >> gpu_nodes

    # --- GPU MANAGEMENT ---
    nfd_operator >> Edge(label="detect features") >> gpu_nodes
    gpu_operator >> Edge(label="manage drivers") >> gpu_nodes

    # --- STORAGE ---
    odf_operator >> Edge(color="orange") >> ceph_cluster
    ceph_cluster >> [sc_block, sc_file, sc_object]
    user_workloads >> Edge(color="blue", label="PVCs") >> sc_block
    user_workloads >> Edge(color="blue", label="shared storage") >> sc_file

    # External storage option
    storage_external >> Edge(style="dashed", label="alternative") >> user_workloads

    # --- IMAGE REGISTRY ---
    user_workloads >> Edge(color="blue", style="dotted", label="image pull") >> internal_registry

print("✓ Generated: output/baseline-ocp-01-core-infrastructure.png")
print("  → Namespace-based layers: Control Plane → Network & Edge → Platform Services")
print("  → Color-coded: Orange=management, Purple=infrastructure, Green=API, Blue=data")
