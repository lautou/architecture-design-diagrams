"""
OpenShift Container Platform - Developer & CI/CD Stack (Direct Graphviz)
Uses HTML table labels for perfect icon centering
"""
from graphviz import Digraph
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(BASE_DIR, '../../..')

# Icons
OPERATOR_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Technology icons/operator/Technology_icon-Red_Hat-operator-Standard-RGB.Large_icon_transparent.png")
GITOPS_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Technology icons/Red Hat OpenShift GitOps/Technology_icon-Red_Hat-OpenShift_GitOps-Standard-RGB.Large_icon_transparent.png")
PIPELINES_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Technology icons/Red Hat OpenShift Pipelines/Technology_icon-Red_Hat-OpenShift_Pipelines-Standard-RGB.Large_icon_transparent.png")
BUILDS_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Technology icons/Builds for Red Hat OpenShift/Technology_icon-Red_Hat-builds_for_Red_Hat_OpenShift-Standard-RGB.Large_icon_transparent.png")
OPENSHIFT_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Technology icons/Red Hat OpenShift/Technology_icon-Red_Hat-OpenShift-Standard-RGB.Large_icon_transparent.png")

def html_node(icon, label):
    return f'<<table border="0"><tr><td><img src="{icon}"/></td></tr><tr><td>{label}</td></tr></table>>'

dot = Digraph("OCP_Developer_CICD", filename="output/baseline-ocp-03-developer-cicd-stack")
dot.attr(rankdir="LR", fontsize="16", bgcolor="white", pad="0.5", nodesep="1.0", ranksep="1.8")

# Personas
dot.node('developer', label=html_node(OPENSHIFT_ICON, 'Developer'), shape='none')
dot.node('git_repo', label=html_node(OPENSHIFT_ICON, 'Git Repository<br/>(GitHub/GitLab)'), shape='none')

# API
dot.node('api', label=html_node(OPENSHIFT_ICON, 'OpenShift<br/>API Server'), shape='none')

# GitOps
with dot.subgraph(name='cluster_gitops') as gitops:
    gitops.attr(label='openshift-gitops-operator + openshift-gitops')
    gitops.node('gitops_operator', label=html_node(OPERATOR_ICON, 'GitOps Operator'), shape='none')
    gitops.node('argocd', label=html_node(GITOPS_ICON, 'Argo CD<br/>(GitOps Controller)'), shape='none')

# Pipelines  
with dot.subgraph(name='cluster_pipelines') as pipes:
    pipes.attr(label='openshift-pipelines')
    pipes.node('pipelines_operator', label=html_node(OPERATOR_ICON, 'Pipelines Operator'), shape='none')
    pipes.node('tekton', label=html_node(PIPELINES_ICON, 'Tekton<br/>(CI/CD Engine)'), shape='none')

# Builds
with dot.subgraph(name='cluster_builds') as builds:
    builds.attr(label='openshift-builds')
    builds.node('builds_operator', label=html_node(OPERATOR_ICON, 'Builds Operator'), shape='none')
    builds.node('shipwright', label=html_node(BUILDS_ICON, 'Shipwright<br/>(Build Framework)'), shape='none')

# Workloads
with dot.subgraph(name='cluster_workloads') as workloads:
    workloads.attr(label='Application Deployments')
    workloads.node('app_deploy', label=html_node(OPENSHIFT_ICON, 'Application<br/>Deployments'), shape='none')

# Connections
dot.edge('developer', 'git_repo', color='green', label='commits')
dot.edge('git_repo', 'argocd', color='green', style='dotted', label='sync')
dot.edge('git_repo', 'tekton', color='blue', style='dotted', label='webhook')

dot.edge('api', 'gitops_operator', color='orange')
dot.edge('api', 'pipelines_operator', color='orange')
dot.edge('api', 'builds_operator', color='orange')

dot.edge('gitops_operator', 'argocd', color='orange')
dot.edge('pipelines_operator', 'tekton', color='orange')
dot.edge('builds_operator', 'shipwright', color='orange')

dot.edge('tekton', 'shipwright', color='blue', label='trigger build')
dot.edge('shipwright', 'app_deploy', color='blue', label='push image')
dot.edge('argocd', 'app_deploy', color='purple', label='deploy', style='bold')

dot.render(format='png', view=False, quiet=True)
print("✓ Generated: output/baseline-ocp-03-developer-cicd-stack.png (Graphviz HTML)")
