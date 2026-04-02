"""
OpenShift Container Platform - Security & Service Mesh Stack Baseline

This diagram shows security and service mesh components:
- Identity and Access Management (Keycloak, Authorino)
- Certificate Management
- Service Mesh (Istio-based)
- Rate Limiting
- Integration with external IDP and security systems

Note: No pod-level representation - focus on logical components and security flows
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.controlplane import APIServer
from diagrams.k8s.network import Service, Ingress
from diagrams.onprem.security import Vault
from diagrams.onprem.network import Istio
from diagrams.onprem.client import Users

graph_attr = {
    "fontsize": "16",
    "bgcolor": "white",
    "pad": "0.5",
    "nodesep": "1.0",
    "ranksep": "1.2"
}

with Diagram(
    "OCP Baseline - Security & Service Mesh Stack",
    show=False,
    direction="TB",
    filename="output/baseline-ocp-04-security-servicemesh-stack",
    graph_attr=graph_attr
):

    users = Users("End Users")

    with Cluster("External Identity Provider"):
        external_idp = Service("Corporate IDP\n(LDAP/AD/SAML/OIDC)")

    with Cluster("External PKI/CA"):
        external_ca = Vault("External CA\n(Enterprise PKI)")

    api = APIServer("OpenShift\nAPI Server")
    router = Ingress("OpenShift Router\n(Ingress)")

    with Cluster("Identity & Access Management"):

        with Cluster("Keycloak (SSO)"):
            keycloak_operator = Service("Keycloak Operator")
            keycloak = Service("Keycloak\n(Red Hat build)")
            keycloak_realms = Service("Realms & Clients\n(OIDC/SAML)")

            keycloak_operator >> keycloak
            keycloak >> keycloak_realms

        with Cluster("API Security"):
            authorino_operator = Service("Authorino Operator")
            authorino = Service("Authorino\n(API Authorization)")

            authorino_operator >> authorino

    with Cluster("Certificate Management"):
        certmanager_operator = Service("cert-manager\nOperator")

        with Cluster("Certificate Issuers"):
            ca_issuer = Service("CA Issuer")
            acme_issuer = Service("ACME Issuer\n(Let's Encrypt)")

            certmanager_operator >> [ca_issuer, acme_issuer]

    with Cluster("Service Mesh"):
        servicemesh_operator = Service("Service Mesh\nOperator")

        with Cluster("Istio Control Plane"):
            istiod = Istio("Istiod\n(Control Plane)")

        with Cluster("Service Mesh Features"):
            mtls = Service("mTLS\n(Service-to-Service)")
            traffic_mgmt = Service("Traffic Management\n(Routing, LB)")
            observability_mesh = Service("Mesh Observability\n(Traces, Metrics)")

        servicemesh_operator >> istiod
        istiod >> [mtls, traffic_mgmt, observability_mesh]

    with Cluster("Rate Limiting & Traffic Control"):
        limitador_operator = Service("Limitador Operator")
        limitador = Service("Limitador\n(Rate Limiting)")

        limitador_operator >> limitador

    with Cluster("Connectivity"):
        connectivity_operator = Service("Connectivity Link\nOperator")
        connectivity = Service("Hybrid Cloud\nConnectivity")

        connectivity_operator >> connectivity

    with Cluster("Application Services"):
        mesh_apps = Service("Service Mesh\nApplications")
        standard_apps = Service("Standard\nApplications")

    # API integration
    api >> [keycloak_operator, authorino_operator, certmanager_operator, servicemesh_operator, limitador_operator, connectivity_operator]

    # External IDP integration
    external_idp >> Edge(label="federation") >> keycloak
    keycloak >> Edge(label="OIDC tokens") >> api
    keycloak >> Edge(label="OIDC") >> authorino

    # User authentication flow
    users >> Edge(label="1. access app") >> router
    router >> Edge(label="2. check auth") >> authorino
    authorino >> Edge(label="3. validate token") >> keycloak

    # Certificate management
    external_ca >> Edge(label="issue certs", style="dashed") >> ca_issuer
    certmanager_operator >> Edge(label="request certs") >> [ca_issuer, acme_issuer]
    ca_issuer >> Edge(label="provision") >> [router, istiod, api]

    # Service mesh traffic flow
    router >> Edge(label="ingress") >> mesh_apps
    mesh_apps >> Edge(label="service-to-service\n(mTLS)") >> mesh_apps
    istiod >> Edge(label="configure sidecar") >> mesh_apps

    # Rate limiting
    router >> Edge(label="rate limit check") >> limitador
    limitador >> Edge(label="allow/deny") >> mesh_apps

    # Standard apps (outside mesh)
    router >> Edge(label="direct", style="dashed") >> standard_apps

    # Observability integration
    observability_mesh >> Edge(label="export traces", style="dotted") >> Service("Tempo/Jaeger")

    # Hybrid connectivity
    connectivity >> Edge(label="secure tunnel", style="dotted") >> Service("Remote Services\n(On-prem, Cloud)")

print("✓ Generated: output/baseline-ocp-04-security-servicemesh-stack.png")
