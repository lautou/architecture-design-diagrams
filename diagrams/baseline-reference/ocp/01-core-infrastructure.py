"""
OpenShift Container Platform - Core Infrastructure (Direct Graphviz)
Uses HTML table labels for perfect icon centering
"""
from graphviz import Digraph
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(BASE_DIR, '../../..')

OPENSHIFT_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Technology icons/Red Hat OpenShift/Technology_icon-Red_Hat-OpenShift-Standard-RGB.Large_icon_transparent.png")
OPERATOR_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Technology icons/operator/Technology_icon-Red_Hat-operator-Standard-RGB.Large_icon_transparent.png")
ODF_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/ODF/odf-400x400.png")

def html_node(icon, label):
    return f'<<table border="0"><tr><td><img src="{icon}"/></td></tr><tr><td>{label}</td></tr></table>>'

dot = Digraph("OCP_Core_Infrastructure", filename="output/baseline-ocp-01-core-infrastructure")
dot.attr(rankdir="TB", fontsize="16", bgcolor="white", pad="0.5", nodesep="1.0", ranksep="1.8")

# Control Plane
with dot.subgraph(name='cluster_control') as control:
    control.attr(label='LAYER 1: Control Plane')
    with control.subgraph(name='cluster_api') as api:
        api.attr(label='openshift-kube-apiserver')
        api.node('apiserver', label=html_node(OPENSHIFT_ICON, 'API Server'), shape='none')
    with control.subgraph(name='cluster_etcd') as etcd:
        etcd.attr(label='openshift-etcd')
        etcd.node('etcd', label=html_node(OPENSHIFT_ICON, 'etcd'), shape='none')

# Compute
with dot.subgraph(name='cluster_compute') as compute:
    compute.attr(label='LAYER 2: Compute Nodes')
    compute.node('cpu_workers', label=html_node(OPENSHIFT_ICON, 'CPU Worker Nodes'), shape='none')
    compute.node('gpu_workers', label=html_node(OPENSHIFT_ICON, 'GPU Worker Nodes'), shape='none')

# Storage
with dot.subgraph(name='cluster_storage') as storage:
    storage.attr(label='LAYER 3: Storage')
    with storage.subgraph(name='cluster_odf') as odf:
        odf.attr(label='openshift-storage')
        odf.node('odf_operator', label=html_node(OPERATOR_ICON, 'ODF Operator'), shape='none')
        odf.node('odf_services', label=html_node(ODF_ICON, 'ODF Services<br/>(Ceph, NooBaa)'), shape='none')

# Networking
with dot.subgraph(name='cluster_network') as network:
    network.attr(label='LAYER 4: Networking')
    with network.subgraph(name='cluster_dns') as dns:
        dns.attr(label='openshift-dns')
        dns.node('dns_service', label=html_node(OPENSHIFT_ICON, 'DNS'), shape='none')
    with network.subgraph(name='cluster_ingress') as ingress:
        ingress.attr(label='openshift-ingress')
        ingress.node('ingress_controller', label=html_node(OPENSHIFT_ICON, 'Ingress Controller'), shape='none')

# Connections
dot.edge('apiserver', 'etcd', color='purple')
dot.edge('apiserver', 'cpu_workers', color='blue')
dot.edge('apiserver', 'gpu_workers', color='blue')
dot.edge('apiserver', 'odf_operator', color='orange')
dot.edge('odf_operator', 'odf_services', color='orange')
dot.edge('cpu_workers', 'odf_services', color='brown', style='dotted', label='PV requests')
dot.edge('gpu_workers', 'odf_services', color='brown', style='dotted', label='PV requests')

dot.render(format='png', view=False, quiet=True)
print("✓ Generated: output/baseline-ocp-01-core-infrastructure.png (Graphviz HTML)")
