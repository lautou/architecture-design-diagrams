"""
OpenShift Multi-Cluster Hub-Spoke Architecture

Shows Advanced Cluster Management (ACM) / Red Hat Advanced Cluster Management for Kubernetes
hub managing multiple spoke clusters across different environments.
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.controlplane import APIServer
from diagrams.k8s.infra import Master, Node
from diagrams.onprem.gitops import Argocd
from diagrams.onprem.monitoring import Prometheus, Grafana

graph_attr = {
    "fontsize": "16",
    "bgcolor": "white",
    "pad": "0.5"
}

with Diagram(
    "OpenShift Multi-Cluster Hub-Spoke",
    show=False,
    direction="TB",
    filename="output/openshift-multicluster-hub-spoke",
    graph_attr=graph_attr
):

    with Cluster("Hub Cluster (ACM)"):
        with Cluster("Management Components"):
            acm = Master("ACM Hub")
            gitops = Argocd("OpenShift GitOps")
            observability = Prometheus("Observability")
            dashboard = Grafana("ACM Console")

        acm >> gitops
        acm >> observability >> dashboard

    with Cluster("Production Clusters"):
        with Cluster("Spoke - US East"):
            prod_us_api = APIServer("API")
            prod_us_nodes = [Node("Worker") for _ in range(3)]

        with Cluster("Spoke - EU West"):
            prod_eu_api = APIServer("API")
            prod_eu_nodes = [Node("Worker") for _ in range(3)]

    with Cluster("Development Clusters"):
        with Cluster("Spoke - Dev"):
            dev_api = APIServer("API")
            dev_nodes = Node("Worker")

        with Cluster("Spoke - QA"):
            qa_api = APIServer("API")
            qa_nodes = Node("Worker")

    # Hub to Spoke connections
    acm >> Edge(label="manage") >> prod_us_api
    acm >> Edge(label="manage") >> prod_eu_api
    acm >> Edge(label="manage") >> dev_api
    acm >> Edge(label="manage") >> qa_api

    # GitOps deployments
    gitops >> Edge(label="deploy policies") >> [prod_us_api, prod_eu_api]
    gitops >> Edge(label="deploy apps") >> [dev_api, qa_api]

    # Observability
    observability << Edge(label="metrics") << [prod_us_api, prod_eu_api, dev_api, qa_api]

print("✓ Generated: output/openshift-multicluster-hub-spoke.png")
