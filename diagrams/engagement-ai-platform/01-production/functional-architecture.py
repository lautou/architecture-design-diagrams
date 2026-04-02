"""
Production Environment - Functional Architecture

Shows the functional components and integration points for the production AI platform.
This composes the baseline OCP and RHOAI diagrams with production-specific configurations.

Customize based on customer production requirements:
- High availability configurations
- Production-grade integrations
- Security and compliance requirements
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.controlplane import APIServer
from diagrams.k8s.network import Service, Ingress
from diagrams.onprem.client import Users
from diagrams.onprem.security import Vault
from diagrams.onprem.monitoring import Prometheus, Grafana
from diagrams.onprem.network import Internet

graph_attr = {
    "fontsize": "16",
    "bgcolor": "white",
    "pad": "0.5",
    "ranksep": "1.2"
}

with Diagram(
    "Production - Functional Architecture (AI Platform)",
    show=False,
    direction="TB",
    filename="output/engagement-01-production-functional",
    graph_attr=graph_attr
):

    business_users = Users("Business Users\n(Production Apps)")

    with Cluster("External Production Services"):
        enterprise_idp = Service("Enterprise IDP\n(Production)")
        enterprise_ca = Vault("Enterprise PKI\n(Production CAs)")
        external_firewall = Service("Enterprise Firewall\n& WAF")

    with Cluster("Production OpenShift Cluster"):

        api = APIServer("OCP API Server\n(HA)")
        router = Ingress("OpenShift Router\n(HA)")

        with Cluster("OCP Platform - Production Config"):
            # Reference: baseline-reference/ocp/01-core-infrastructure.py
            core_infra = Service("Core Infrastructure\n(See baseline-ocp-01)")

            # Reference: baseline-reference/ocp/02-observability-stack.py
            observability = Prometheus("Observability Stack\n(See baseline-ocp-02)")

            # Reference: baseline-reference/ocp/03-developer-cicd-stack.py
            cicd = Service("CI/CD Stack\n(See baseline-ocp-03)")

            # Reference: baseline-reference/ocp/04-security-servicemesh-stack.py
            security = Service("Security & Service Mesh\n(See baseline-ocp-04)")

        with Cluster("RHOAI Platform - Production"):
            # Reference: baseline-reference/rhoai/functional-components.py
            rhoai_dashboard = Service("RHOAI Dashboard")
            model_serving = Service("Model Serving\n(KServe - HA)")
            model_registry = Service("Model Registry\n(Production)")
            trustyai = Service("TrustyAI\n(Model Monitoring)")

        with Cluster("Production ML Applications"):
            ml_app_1 = Service("ML Application 1\n(Business Critical)")
            ml_app_2 = Service("ML Application 2\n(Customer Facing)")

    with Cluster("Production Monitoring & Compliance"):
        prod_monitoring = Grafana("Production\nDashboards")
        audit_logs = Service("Audit Logging\n(Compliance)")

    # External access flow
    business_users >> Edge(label="1. access") >> external_firewall
    external_firewall >> Edge(label="2. filtered traffic") >> router
    router >> Edge(label="3. route") >> [ml_app_1, ml_app_2]

    # Authentication
    router >> Edge(label="authenticate") >> enterprise_idp
    enterprise_idp >> api

    # Model serving in production
    [ml_app_1, ml_app_2] >> Edge(label="inference requests") >> model_serving
    model_serving >> Edge(label="load models") >> model_registry

    # TrustyAI monitoring
    model_serving >> Edge(label="prediction data") >> trustyai
    trustyai >> Edge(label="fairness & explainability") >> audit_logs

    # Security integration
    enterprise_ca >> Edge(label="certificates") >> [router, api]

    # Observability
    [model_serving, ml_app_1, ml_app_2] >> Edge(label="metrics", style="dotted") >> observability
    observability >> prod_monitoring

    # Compliance logging
    [api, router, model_serving] >> Edge(label="audit trail", style="dotted") >> audit_logs

print("✓ Generated: output/engagement-01-production-functional.png")
print("NOTE: This is a TEMPLATE - References baseline OCP and RHOAI diagrams")
print("      Customize with customer-specific production integrations")
