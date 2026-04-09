"""
OpenShift Container Platform - Security & Service Mesh Stack (Direct Graphviz)
Uses HTML table labels for perfect icon centering
"""
from graphviz import Digraph
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(BASE_DIR, '../../..')

OPERATOR_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Technology icons/operator/Technology_icon-Red_Hat-operator-Standard-RGB.Large_icon_transparent.png")
CERT_MANAGER_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/CertManager/cert-manager-400x400.png")
AUTHORINO_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/Authorino/authorino-400x400.png")
LIMITADOR_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/Limitador/limitador-400x400.png")
OSSM_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/OSSM/ossm-400x400.png")
OPENSHIFT_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Technology icons/Red Hat OpenShift/Technology_icon-Red_Hat-OpenShift-Standard-RGB.Large_icon_transparent.png")

def html_node(icon, label):
    return f'<<table border="0"><tr><td><img src="{icon}"/></td></tr><tr><td>{label}</td></tr></table>>'

dot = Digraph("OCP_Security_ServiceMesh", filename="output/baseline-ocp-04-security-servicemesh-stack")
dot.attr(rankdir="TB", fontsize="16", bgcolor="white", pad="0.5", nodesep="1.0", ranksep="1.8")

# API
dot.node('api', label=html_node(OPENSHIFT_ICON, 'OpenShift<br/>API Server'), shape='none')

# Identity
with dot.subgraph(name='cluster_identity') as identity:
    identity.attr(label='Identity & Auth')
    with identity.subgraph(name='cluster_keycloak') as keycloak:
        keycloak.attr(label='keycloak-system')
        keycloak.node('keycloak_operator', label=html_node(OPERATOR_ICON, 'Keycloak Operator'), shape='none')
        keycloak.node('keycloak', label=html_node(OPENSHIFT_ICON, 'Keycloak<br/>(SSO)'), shape='none')

# Certificate Management
with dot.subgraph(name='cluster_certs') as certs:
    certs.attr(label='Certificate Management')
    with certs.subgraph(name='cluster_certmgr') as certmgr:
        certmgr.attr(label='cert-manager-operator')
        certmgr.node('certmgr_operator', label=html_node(OPERATOR_ICON, 'cert-manager Operator'), shape='none')
        certmgr.node('certmgr', label=html_node(CERT_MANAGER_ICON, 'cert-manager'), shape='none')

# Service Mesh
with dot.subgraph(name='cluster_mesh') as mesh:
    mesh.attr(label='Service Mesh')
    with mesh.subgraph(name='cluster_ossm') as ossm:
        ossm.attr(label='openshift-operators')
        ossm.node('ossm_operator', label=html_node(OPERATOR_ICON, 'Service Mesh Operator'), shape='none')
        ossm.node('istio', label=html_node(OSSM_ICON, 'Istio<br/>(Control Plane)'), shape='none')

# Kuadrant (AuthZ + Rate Limiting)
with dot.subgraph(name='cluster_kuadrant') as kuadrant:
    kuadrant.attr(label='kuadrant-system')
    kuadrant.node('authorino', label=html_node(AUTHORINO_ICON, 'Authorino<br/>(AuthZ)'), shape='none')
    kuadrant.node('limitador', label=html_node(LIMITADOR_ICON, 'Limitador<br/>(Rate Limiting)'), shape='none')

# App Workloads
with dot.subgraph(name='cluster_apps') as apps:
    apps.attr(label='Application Workloads')
    apps.node('app_pods', label=html_node(OPENSHIFT_ICON, 'Application Pods<br/>(in Service Mesh)'), shape='none')

# Connections
dot.edge('api', 'keycloak_operator', color='orange')
dot.edge('api', 'certmgr_operator', color='orange')
dot.edge('api', 'ossm_operator', color='orange')

dot.edge('keycloak_operator', 'keycloak', color='orange')
dot.edge('certmgr_operator', 'certmgr', color='orange')
dot.edge('ossm_operator', 'istio', color='orange')

dot.edge('istio', 'app_pods', color='purple', label='sidecar injection')
dot.edge('app_pods', 'authorino', color='blue', style='dotted', label='authz check')
dot.edge('app_pods', 'limitador', color='red', style='dotted', label='rate limit')
dot.edge('app_pods', 'keycloak', color='green', style='dotted', label='OIDC auth')

dot.edge('certmgr', 'istio', color='brown', style='dashed', label='TLS certs')

dot.render(format='png', view=False, quiet=True)
print("✓ Generated: output/baseline-ocp-04-security-servicemesh-stack.png (Graphviz HTML)")
