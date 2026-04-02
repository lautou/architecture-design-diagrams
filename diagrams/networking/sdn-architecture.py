"""
OpenShift SDN (Software Defined Networking) Architecture

Demonstrates OpenShift networking with:
- OVN-Kubernetes CNI
- Network policies
- Ingress/Egress traffic flow
- Service mesh integration (optional)
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.network import Service, Ingress, NetworkPolicy
from diagrams.k8s.compute import Pod
from diagrams.k8s.controlplane import APIServer
from diagrams.onprem.network import Internet
from diagrams.onprem.client import Users

graph_attr = {
    "fontsize": "16",
    "bgcolor": "white",
    "pad": "0.5"
}

with Diagram(
    "OpenShift SDN Architecture (OVN-Kubernetes)",
    show=False,
    direction="TB",
    filename="output/openshift-sdn-architecture",
    graph_attr=graph_attr
):

    external_users = Users("External Users")
    internet = Internet("Internet")

    with Cluster("OpenShift Cluster"):

        with Cluster("Networking Layer"):
            router = Ingress("OpenShift Router\n(HAProxy)")

            with Cluster("OVN-Kubernetes CNI"):
                ovn_master = Service("OVN Master")
                ovn_controller = Service("OVN Controller")

        with Cluster("Project: Frontend"):
            frontend_netpol = NetworkPolicy("Network Policy\n(Allow: 8080)")
            frontend_svc = Service("Frontend Service")
            frontend_pods = [Pod("Frontend Pod") for _ in range(2)]

            frontend_netpol >> frontend_pods
            frontend_svc >> frontend_pods

        with Cluster("Project: Backend"):
            backend_netpol = NetworkPolicy("Network Policy\n(Allow from Frontend)")
            backend_svc = Service("Backend Service")
            backend_pods = [Pod("Backend Pod") for _ in range(2)]

            backend_netpol >> backend_pods
            backend_svc >> backend_pods

        with Cluster("Project: Database"):
            db_netpol = NetworkPolicy("Network Policy\n(Deny Ingress)")
            db_svc = Service("DB Service")
            db_pod = Pod("PostgreSQL Pod")

            db_netpol >> db_pod
            db_svc >> db_pod

        api = APIServer("API Server")

    # External traffic flow
    external_users >> Edge(label="HTTPS") >> router
    router >> Edge(label="route") >> frontend_svc

    # Internal traffic flow
    frontend_pods >> Edge(label="allowed by policy", color="green") >> backend_svc
    backend_pods >> Edge(label="allowed by policy", color="green") >> db_svc

    # Blocked traffic (for illustration)
    frontend_pods >> Edge(label="blocked", color="red", style="dashed") >> db_svc

    # SDN control plane
    api >> ovn_master >> ovn_controller
    ovn_controller >> Edge(label="configure") >> [frontend_netpol, backend_netpol, db_netpol]

    # Egress
    backend_pods >> Edge(label="egress", style="dotted") >> internet

print("✓ Generated: output/openshift-sdn-architecture.png")
