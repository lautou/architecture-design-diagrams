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
from diagrams.onprem.security import Vault
from diagrams.onprem.client import Users
from diagrams.onprem.compute import Server
from diagrams.custom import Custom
import os

# Get absolute paths for icons
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(BASE_DIR, '../../..')
OPERATOR_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Technology icons/operator/Technology_icon-Red_Hat-operator-Standard-RGB.Large_icon_transparent.png")
KEYCLOAK_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Technology icons/Red Hat build of Keycloak/Technology_icon-Red_Hat-Keycloak-Standard-RGB.Large_icon_transparent.png")
SERVICE_MESH_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Technology icons/Red Hat OpenShift Service Mesh/Technology_icon-Red_Hat-OpenShift_Service_Mesh-Standard-RGB.Large_icon_transparent.png")
CONNECTIVITY_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Technology icons/Red Hat Connectivity Link/Technology_icon-Red_Hat-Connectivity_Link-Standard-RGB.Large_icon_transparent.png")

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
    end_users = Users("\nEnd Users")

    # ========== EXTERNAL ==========
    with Cluster("External Security Services"):
        corporate_idp = Server("\nCorporate IDP\n(LDAP/AD/OIDC)")
        enterprise_pki = Vault("\nEnterprise PKI\n(CA)")

    api = APIServer("\nOpenShift\nAPI Server")
    router = Ingress("\nOpenShift Router")

    # ========== IDENTITY & ACCESS MANAGEMENT ==========
    with Cluster("Identity & Access Management"):

        with Cluster("rhsso-operator"):
            keycloak_operator = Custom("\nKeycloak Operator", KEYCLOAK_ICON)

        with Cluster("keycloak (instance namespace)"):
            keycloak_server = Custom("\nKeycloak Server\n(Red Hat build)", KEYCLOAK_ICON)
            keycloak_realms = Vault("\nRealms & Clients\n(OIDC/SAML)")

        with Cluster("authorino-operator"):
            authorino_operator = Custom("\nAuthorino Operator", OPERATOR_ICON)

        with Cluster("authorino-instances"):
            authorino_service = Vault("\nAuthorino\n(API Authorization)")

    # ========== CERTIFICATE MANAGEMENT ==========
    with Cluster("Certificate Management"):

        with Cluster("openshift-cert-manager-operator"):
            certmanager_operator = Custom("\ncert-manager\nOperator", OPERATOR_ICON)

        with Cluster("openshift-cert-manager"):
            with Cluster("Certificate Issuers"):
                ca_issuer = Vault("\nCA Issuer")
                acme_issuer = Vault("\nACME Issuer\n(Let's Encrypt)")
                cert_manager = Vault("\ncert-manager\nController")

    # ========== SERVICE MESH ==========
    with Cluster("Service Mesh"):

        with Cluster("openshift-operators (Service Mesh)"):
            servicemesh_operator = Custom("\nService Mesh\nOperator", SERVICE_MESH_ICON)

        with Cluster("istio-system"):
            istiod = Custom("\nIstiod\n(Control Plane)", SERVICE_MESH_ICON)

            with Cluster("Mesh Features"):
                mtls_enforcement = Server("\nmTLS Enforcement")
                traffic_management = Server("\nTraffic Management\n(VirtualServices)")
                mesh_observability = Server("\nMesh Telemetry\n(Traces)")

    # ========== RATE LIMITING ==========
    with Cluster("Rate Limiting & Traffic Control"):

        with Cluster("openshift-operators (Limitador)"):
            limitador_operator = Custom("\nLimitador Operator", OPERATOR_ICON)

        with Cluster("limitador-system"):
            limitador_service = Server("\nLimitador\n(Rate Limiting)")

    # ========== CONNECTIVITY ==========
    with Cluster("Hybrid Cloud Connectivity"):

        with Cluster("openshift-operators (Connectivity)"):
            connectivity_operator = Custom("\nConnectivity Link\nOperator", CONNECTIVITY_ICON)

        with Cluster("skupper-site-controller"):
            connectivity_service = Custom("\nSkupper\n(Service Interconnect)", CONNECTIVITY_ICON)

    # ========== APPLICATION SERVICES ==========
    with Cluster("Application Services"):
        mesh_applications = Server("\nService Mesh\nApplications")
        standard_applications = Server("\nStandard\nApplications")

    with Cluster("Remote Services"):
        remote_services = Server("\nOn-Premise/Cloud\nServices")

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
    mesh_observability >> Edge(style="dotted", label="export traces") >> Server("\nTempo/Jaeger")

    # --- HYBRID CONNECTIVITY (Purple = secure tunnel) ---
    connectivity_service >> Edge(color="purple", style="dotted", label="secure tunnel") >> remote_services
    mesh_applications >> Edge(style="dotted") >> connectivity_service

print("✓ Generated: output/baseline-ocp-04-security-servicemesh-stack.png")
print("  → Namespace-based: rhsso-operator → istio-system → limitador-system")
print("  → Color-coded: Orange=management, Green=traffic, Red=security, Purple=mTLS")
