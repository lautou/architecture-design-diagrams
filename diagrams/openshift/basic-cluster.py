"""
Basic OpenShift Cluster Architecture

This diagram shows a simplified OpenShift cluster with:
- Control plane components
- Worker nodes with compute resources
- Storage and networking layers
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.controlplane import APIServer, ControllerManager, Scheduler
from diagrams.k8s.compute import Pod, Deployment
from diagrams.k8s.network import Service, Ingress
from diagrams.k8s.storage import PV, PVC, StorageClass
from diagrams.onprem.network import Etcd
from diagrams.onprem.client import Users

graph_attr = {
    "fontsize": "16",
    "bgcolor": "white",
    "pad": "0.5"
}

with Diagram(
    "OpenShift Basic Cluster Architecture",
    show=False,
    direction="TB",
    filename="output/openshift-basic-cluster",
    graph_attr=graph_attr
):
    users = Users("Users/Developers")

    with Cluster("Control Plane"):
        with Cluster("API Layer"):
            api = APIServer("OpenShift API")

        with Cluster("Management"):
            scheduler = Scheduler("Scheduler")
            controller = ControllerManager("Controller Manager")

        etcd = Etcd("etcd cluster")

    with Cluster("Compute Layer"):
        with Cluster("Worker Node 1"):
            with Cluster("Namespace: app-prod"):
                deployment1 = Deployment("App Deployment")
                pods1 = [Pod("Pod") for _ in range(2)]
                svc1 = Service("Service")
                deployment1 >> pods1 >> svc1

        with Cluster("Worker Node 2"):
            with Cluster("Namespace: app-dev"):
                deployment2 = Deployment("Dev Deployment")
                pods2 = Pod("Pod")
                svc2 = Service("Service")
                deployment2 >> pods2 >> svc2

    with Cluster("Networking"):
        ingress = Ingress("OpenShift Router")
        ingress >> [svc1, svc2]

    with Cluster("Storage"):
        sc = StorageClass("Storage Class")
        pv = PV("Persistent Volume")
        pvc = PVC("PVC")
        sc >> pv >> pvc

    # Connections
    users >> ingress
    users >> Edge(label="oc/kubectl") >> api
    api >> etcd
    api >> scheduler
    api >> controller
    scheduler >> Edge(label="schedule") >> pods1
    pvc >> pods1[0]

print("✓ Generated: output/openshift-basic-cluster.png")
