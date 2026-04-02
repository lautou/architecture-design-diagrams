"""
Common - Integration Patterns (Template)

Reusable integration patterns for AI platform engagements:
- IDP/SSO integration
- External storage integration
- Network security patterns
- Monitoring integration

Use these patterns across all environments with appropriate variations.
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.controlplane import APIServer
from diagrams.k8s.network import Service, Ingress
from diagrams.onprem.security import Vault
from diagrams.onprem.storage import Ceph
from diagrams.onprem.monitoring import Prometheus

graph_attr = {
    "fontsize": "16",
    "bgcolor": "white",
    "pad": "0.5",
    "ranksep": "1.2"
}

with Diagram(
    "Common - Integration Patterns (Template)",
    show=False,
    direction="LR",
    filename="output/engagement-common-integration-patterns",
    graph_attr=graph_attr
):

    with Cluster("External Enterprise Services"):
        enterprise_idp = Service("Corporate IDP\n(LDAP/AD/OIDC)")
        enterprise_storage = Ceph("Enterprise Storage\n(S3/NFS)")
        enterprise_monitoring = Prometheus("Enterprise Monitoring\n(SIEM/APM)")
        enterprise_pki = Vault("Enterprise PKI\n(Certificate Authority)")

    with Cluster("OpenShift Cluster (Any Environment)"):
        api = APIServer("OCP API")
        router = Ingress("Router")

        with Cluster("Integration Components"):
            keycloak = Service("Keycloak\n(IDP Bridge)")
            certmanager = Service("cert-manager\n(Certificate Mgmt)")
            otel = Service("OpenTelemetry\n(Observability)")

    # Pattern 1: IDP Integration
    enterprise_idp >> Edge(label="LDAP/SAML/OIDC") >> keycloak
    keycloak >> Edge(label="OAuth2/OIDC") >> api

    # Pattern 2: Storage Integration
    enterprise_storage >> Edge(label="S3 API / NFS") >> Service("Data Connections")

    # Pattern 3: Certificate Management
    enterprise_pki >> Edge(label="Issue certificates") >> certmanager
    certmanager >> Edge(label="provision") >> [router, api]

    # Pattern 4: Monitoring Integration
    otel >> Edge(label="forward metrics/logs") >> enterprise_monitoring

print("✓ Generated: output/engagement-common-integration-patterns.png")
print("NOTE: TEMPLATE - Use these patterns consistently across all environments")
print("      Adapt authentication, storage, and monitoring based on customer standards")
