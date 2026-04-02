"""
OpenShift Container Platform - Security & Service Mesh Stack Baseline

Namespace-based layered architecture for security:
- Identity & Access (rhsso-operator, authorino-operator)
- Certificate Management (openshift-cert-manager-operator)
- Service Mesh (openshift-operators, istio-system)
- Rate Limiting & Connectivity

Color-coded connections:
- Orange: Operator management
- Green: User/API traffic
- Red: Security enforcement
- Purple: mTLS/encrypted traffic

Note: Shows actual namespace organization for security stack
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.controlplane import APIServer
from diagrams.k8s.network import Ingress
from diagrams.k8s.ecosystem import Helm
from diagrams.onprem.security import Vault
from diagrams.onprem.network import Istio
from diagrams.onprem.client import Users
from diagrams.onprem.compute import Server

graph_attr = {
    "fontsize": "16",
    "bgcolor": "white",
    "pad": "0.5",
    "nodesep": "1.0",
    "ranksep": "1.8"
}

with Diagram(
    "OCP Baseline - Security & Service Mesh Stack (Namespace-Based)",
    show=False,
    direction="TB",
    filename="output/baseline-ocp-04-security-servicemesh-stack",
    graph_attr=graph_attr
):

    # ========== PERSONAS ==========
    end_users = Users("End Users")

    # ========== EXTERNAL ==========
    with Cluster("External Security Services"):
        corporate_idp = Server("Corporate IDP\n(LDAP/AD/OIDC)")
        enterprise_pki = Vault("Enterprise PKI\n(CA)")

    api = APIServer("OpenShift\nAPI Server")
    router = Ingress("OpenShift Router")

    # ========== IDENTITY & ACCESS MANAGEMENT ==========
    with Cluster("Identity & Access Management"):

        with Cluster("rhsso-operator"):
            keycloak_operator = Helm("Keycloak Operator")

        with Cluster("keycloak (instance namespace)"):
            keycloak_server = Vault("Keycloak Server\n(Red Hat build)")
            keycloak_realms = Vault("Realms & Clients\n(OIDC/SAML)")

        with Cluster("authorino-operator"):
            authorino_operator = Helm("Authorino Operator")

        with Cluster("authorino-instances"):
            authorino_service = Vault("Authorino\n(API Authorization)")

    # ========== CERTIFICATE MANAGEMENT ==========
    with Cluster("Certificate Management"):

        with Cluster("openshift-cert-manager-operator"):
            certmanager_operator = Helm("cert-manager\nOperator")

        with Cluster("openshift-cert-manager"):
            with Cluster("Certificate Issuers"):
                ca_issuer = Vault("CA Issuer")
                acme_issuer = Vault("ACME Issuer\n(Let's Encrypt)")
                cert_manager = Vault("cert-manager\nController")

    # ========== SERVICE MESH ==========
    with Cluster("Service Mesh"):

        with Cluster("openshift-operators (Service Mesh)"):
            servicemesh_operator = Helm("Service Mesh\nOperator")

        with Cluster("istio-system"):
            istiod = Istio("Istiod\n(Control Plane)")

            with Cluster("Mesh Features"):
                mtls_enforcement = Istio("mTLS Enforcement")
                traffic_management = Istio("Traffic Management\n(VirtualServices)")
                mesh_observability = Istio("Mesh Telemetry\n(Traces)")

    # ========== RATE LIMITING ==========
    with Cluster("Rate Limiting & Traffic Control"):

        with Cluster("openshift-operators (Limitador)"):
            limitador_operator = Helm("Limitador Operator")

        with Cluster("limitador-system"):
            limitador_service = Istio("Limitador\n(Rate Limiting)")

    # ========== CONNECTIVITY ==========
    with Cluster("Hybrid Cloud Connectivity"):

        with Cluster("openshift-operators (Connectivity)"):
            connectivity_operator = Helm("Connectivity Link\nOperator")

        with Cluster("skupper-site-controller"):
            connectivity_service = Istio("Skupper\n(Service Interconnect)")

    # ========== APPLICATION SERVICES ==========
    with Cluster("Application Services"):
        mesh_applications = Server("Service Mesh\nApplications")
        standard_applications = Server("Standard\nApplications")

    with Cluster("Remote Services"):
        remote_services = Server("On-Premise/Cloud\nServices")

    # =========================================================
    # CONNECTIONS
    # =========================================================

    # --- OPERATOR MANAGEMENT (Orange) ---
    api >> Edge(color="orange") >> keycloak_operator
    api >> Edge(color="orange") >> authorino_operator
    api >> Edge(color="orange") >> certmanager_operator
    api >> Edge(color="orange") >> servicemesh_operator
    api >> Edge(color="orange") >> limitador_operator
    api >> Edge(color="orange") >> connectivity_operator

    keycloak_operator >> Edge(color="orange") >> keycloak_server
    authorino_operator >> Edge(color="orange") >> authorino_service
    certmanager_operator >> Edge(color="orange") >> cert_manager
    servicemesh_operator >> Edge(color="orange") >> istiod
    limitador_operator >> Edge(color="orange") >> limitador_service
    connectivity_operator >> Edge(color="orange") >> connectivity_service

    # Keycloak internal
    keycloak_server >> keycloak_realms

    # Service mesh features
    istiod >> [mtls_enforcement, traffic_management, mesh_observability]

    # cert-manager issuers
    cert_manager >> [ca_issuer, acme_issuer]

    # --- EXTERNAL INTEGRATION ---
    corporate_idp >> Edge(label="federation") >> keycloak_server
    enterprise_pki >> Edge(color="red", label="issue certs") >> ca_issuer

    # --- USER AUTHENTICATION FLOW (Green → Red enforcement) ---
    end_users >> Edge(color="green", label="1. access") >> router
    router >> Edge(color="red", label="2. AuthN/AuthZ") >> authorino_service
    authorino_service >> Edge(color="red", label="3. validate") >> keycloak_server
    keycloak_server >> Edge(label="OIDC token") >> api

    # --- CERTIFICATE PROVISIONING ---
    cert_manager >> Edge(color="red", label="provision") >> router
    cert_manager >> Edge(color="red", label="provision") >> api
    cert_manager >> Edge(color="red", label="provision") >> istiod

    # --- SERVICE MESH TRAFFIC FLOW (Purple = mTLS) ---
    router >> Edge(color="green", label="ingress") >> mesh_applications
    mesh_applications >> Edge(color="purple", label="mTLS", style="bold") >> mesh_applications
    istiod >> Edge(color="purple", label="configure sidecars") >> mesh_applications

    # --- RATE LIMITING (Red = enforcement) ---
    router >> Edge(color="red", label="rate limit check") >> limitador_service
    limitador_service >> Edge(color="red", label="allow/deny") >> mesh_applications

    # --- STANDARD APPS (bypass mesh) ---
    router >> Edge(style="dashed", label="direct") >> standard_applications

    # --- OBSERVABILITY INTEGRATION ---
    mesh_observability >> Edge(style="dotted", label="export traces") >> Server("Tempo/Jaeger")

    # --- HYBRID CONNECTIVITY (Purple = secure tunnel) ---
    connectivity_service >> Edge(color="purple", style="dotted", label="secure tunnel") >> remote_services
    mesh_applications >> Edge(style="dotted") >> connectivity_service

print("✓ Generated: output/baseline-ocp-04-security-servicemesh-stack.png")
print("  → Namespace-based: rhsso-operator → istio-system → limitador-system")
print("  → Color-coded: Orange=management, Green=traffic, Red=security, Purple=mTLS")
