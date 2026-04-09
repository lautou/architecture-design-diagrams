"""
RHOAI on OCP - Integration Architecture (Direct Graphviz with HTML Tables)

Shows RHOAI platform running on OpenShift Container Platform with OCP services.
Uses direct Graphviz with HTML table labels for perfect icon centering.

Structure:
- OpenShift Container Platform (outer cluster)
  - OCP Platform Services (6 categories):
    - Compute And Acceleration Services: NVIDIA GPU Operator, NFD, Kueue, Leader Worker Set
    - Observability Services: Cluster Monitoring, UDWM, Grafana, Cluster Observability, Logging, Loki, OpenTelemetry, Tempo, Network Observability
    - Security & Identity Services: cert-manager, Authorino, Limitador, DNS, RHCL (kuadrant-system), OpenShift Service Mesh
    - Developer Services: Builds, Pipelines, GitOps
    - Storage Services: OpenShift Data Foundation
    - Core Components (20 essential OpenShift components in 2-row grid)
  - Red Hat OpenShift AI Platform (runs on OCP):
    - redhat-ods-applications: RHOAI operator
    - redhat-ods-monitoring: RHOAI monitoring stack
    - rhods-notebooks: Jupyter workbench, Code Server workbench
    - ai-project-A through ai-project-H: Sample AI workloads

Layout: 4-row layout with distributed anchor points
- Row 1: RHOAI Platform (11 namespaces)
- Row 2: Compute And Acceleration Services (4), Observability Services (9)
- Row 3: Security & Identity Services (6), Developer Services (3), Storage Services (1)
- Row 4: Core Components (20 components in 2-row grid: 10 + 10)

Technical Notes:
- Uses direct graphviz.Digraph() instead of diagrams library
- HTML table labels for perfect icon centering with long cluster labels
- All icons perfectly centered regardless of cluster label length
"""

from graphviz import Digraph
import os

# Calculate absolute paths for custom icons
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(BASE_DIR, '../../..')

# Icon paths
OPERATOR_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Technology icons/operator/Technology_icon-Red_Hat-operator-Standard-RGB.Large_icon_transparent.png")
MONITORING_ICON = os.path.join(PROJECT_ROOT, "custom_icons/UI icons/rh-ui-icon-monitoring-fill.Large_icon_transparent.png")
BUILDS_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Technology icons/Builds for Red Hat OpenShift/Technology_icon-Red_Hat-builds_for_Red_Hat_OpenShift-Standard-RGB.Large_icon_transparent.png")
TEMPO_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/Tempo/tempo-400x400.png")
NVIDIA_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/NVIDIA/nvidia-400x400.png")
RHCL_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/RHCL/rhcl-400x400.png")
OPENTELEMETRY_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/OpenTelemetry/opentelemetry-400x400.png")
RHOAI_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/AI/ai-standard-small.png")
ODF_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/ODF/odf-400x400.png")
DNS_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/DNS/dns-400x400.png")
AUTHORINO_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/Authorino/authorino-400x400.png")
LIMITADOR_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/Limitador/limitador-400x400.png")
NFD_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/NFD/nfd-400x400.png")
PIPELINES_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/Pipelines/pipelines-400x400.png")
GRAFANA_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/Grafana/grafana-400x400.png")
KUEUE_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/Kueue/kueue-400x400.png")
LWS_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/LWS/lws-400x400.png")
CERT_MANAGER_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/CertManager/cert-manager-400x400.png")
OBSERVABILITY_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/Observability/observability-400x400.png")
LOGGING_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/Logging/logging-400x400.png")
LOKI_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/Loki/loki-400x400.png")
GITOPS_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/GitOps/gitops-400x400.png")
NETWORK_OBSERVABILITY_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/NetworkObservability/network-observability-400x400.png")
OSSM_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/OSSM/ossm-400x400.png")
AI_MODEL_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Technology icons/AI model/Technology_icon-Red_Hat-AI_model-Red-RGB.Large_icon_transparent.png")
CLUSTER_OBSERVABILITY_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Technology icons/Cluster observability/Technology_icon-Red_Hat-cluster_observability-Standard-RGB.Large_icon_transparent.png")
JUPYTER_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/Jupyter/jupyter-400x400.png")
VSCODE_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/VSCode/vscode-400x400.png")
OPENSHIFT_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Technology icons/Red Hat OpenShift/Technology_icon-Red_Hat-OpenShift-Standard-RGB.Large_icon_transparent.png")

# Helper function to create HTML table label for nodes
def html_node(icon_path, label_text):
    """Create HTML table label for perfect centering"""
    return f'''<<table border="0">
<tr><td><img src="{icon_path}"/></td></tr>
<tr><td>{label_text}</td></tr>
</table>>'''

# Create diagram
dot = Digraph("RHOAI_on_OCP_Integration", filename="output/rhoai-ocp-integration")
dot.attr(rankdir="TB")
dot.attr(fontsize="9", bgcolor="white", pad="0.5", nodesep="1.0", ranksep="1.0", dpi="300")

# Main cluster: OpenShift Container Platform
with dot.subgraph(name='cluster_ocp') as ocp:
    ocp.attr(label='OpenShift Container Platform', margin='20', bgcolor='lightgray')

    # OCP Platform Services
    with ocp.subgraph(name='cluster_ocp_services') as services:
        services.attr(label='OCP Platform Services', margin='15', bgcolor='lightgreen')

        # Compute And Acceleration Services
        with services.subgraph(name='cluster_compute') as compute:
            compute.attr(label='Compute And Acceleration Services', margin='10', bgcolor='lightyellow')

            with compute.subgraph(name='cluster_gpu') as gpu_cluster:
                gpu_cluster.attr(label='nvidia-gpu-operator', margin='10', bgcolor='white', style='rounded', labeljust='c')
                gpu_cluster.node('gpu_operator', label=html_node(NVIDIA_ICON, 'NVIDIA GPU<br/>Operator'), shape='none')

            with compute.subgraph(name='cluster_nfd') as nfd_cluster:
                nfd_cluster.attr(label='openshift-nfd', margin='10', bgcolor='white', style='rounded', labeljust='c')
                nfd_cluster.node('nfd', label=html_node(NFD_ICON, 'Node Feature<br/>Discovery Operator'), shape='none')

            with compute.subgraph(name='cluster_kueue') as kueue_cluster:
                kueue_cluster.attr(label='openshift-kueue-operator', margin='10', bgcolor='white', style='rounded', labeljust='c')
                kueue_cluster.node('kueue', label=html_node(KUEUE_ICON, 'Red Hat Build Of<br/>Kueue Operator'), shape='none')

            with compute.subgraph(name='cluster_lws') as lws_cluster:
                lws_cluster.attr(label='openshift-leader-worker-set-operator', margin='10', bgcolor='white', style='rounded', labeljust='c')
                lws_cluster.node('lws', label=html_node(LWS_ICON, 'Red Hat Build Of<br/>Leader Worker Set<br/>Operator'), shape='none')

        # Observability Services
        with services.subgraph(name='cluster_observability') as obs:
            obs.attr(label='Observability Services', margin='10', bgcolor='lightyellow')

            with obs.subgraph(name='cluster_monitoring') as monitoring_cluster:
                monitoring_cluster.attr(label='openshift-monitoring', margin='10', bgcolor='white', style='rounded', labeljust='c')
                monitoring_cluster.node('cluster_monitoring', label=html_node(MONITORING_ICON, 'Cluster Monitoring'), shape='none')

            with obs.subgraph(name='cluster_udwm') as udwm_cluster:
                udwm_cluster.attr(label='openshift-user-workload-monitoring', margin='10', bgcolor='white', style='rounded', labeljust='c')
                udwm_cluster.node('udwm', label=html_node(MONITORING_ICON, 'User Defined<br/>Workload Monitoring'), shape='none')

            with obs.subgraph(name='cluster_grafana') as grafana_cluster:
                grafana_cluster.attr(label='openshift-operators', margin='10', bgcolor='white', style='rounded', labeljust='c')
                grafana_cluster.node('grafana', label=html_node(GRAFANA_ICON, 'Grafana<br/>Operator'), shape='none')

            with obs.subgraph(name='cluster_cluster_obs') as cluster_obs_cluster:
                cluster_obs_cluster.attr(label='openshift-cluster-observability-operator', margin='10', bgcolor='white', style='rounded', labeljust='c')
                cluster_obs_cluster.node('cluster_observability', label=html_node(CLUSTER_OBSERVABILITY_ICON, 'Cluster Observability<br/>Operator'), shape='none')

            with obs.subgraph(name='cluster_logging') as logging_cluster:
                logging_cluster.attr(label='openshift-logging', margin='10', bgcolor='white', style='rounded', labeljust='c')
                logging_cluster.node('openshift_logging', label=html_node(LOGGING_ICON, 'OpenShift<br/>Logging Operator'), shape='none')

            with obs.subgraph(name='cluster_loki') as loki_cluster:
                loki_cluster.attr(label='openshift-operators-redhat', margin='10', bgcolor='white', style='rounded', labeljust='c')
                loki_cluster.node('loki', label=html_node(LOKI_ICON, 'Loki<br/>Operator'), shape='none')

            with obs.subgraph(name='cluster_otel') as otel_cluster:
                otel_cluster.attr(label='openshift-opentelemetry-operator', margin='10', bgcolor='white', style='rounded', labeljust='c')
                otel_cluster.node('opentelemetry', label=html_node(OPENTELEMETRY_ICON, 'Red Hat Build Of<br/>OpenTelemetry'), shape='none')

            with obs.subgraph(name='cluster_tempo') as tempo_cluster:
                tempo_cluster.attr(label='openshift-tempo-operator', margin='10', bgcolor='white', style='rounded', labeljust='c')
                tempo_cluster.node('tempo', label=html_node(TEMPO_ICON, 'Tempo<br/>Operator'), shape='none')

            with obs.subgraph(name='cluster_netobserv') as netobserv_cluster:
                netobserv_cluster.attr(label='netobserv', margin='10', bgcolor='white', style='rounded', labeljust='c')
                netobserv_cluster.node('netobserv', label=html_node(NETWORK_OBSERVABILITY_ICON, 'Network<br/>Observability<br/>Operator'), shape='none')

        # Security & Identity Services
        with services.subgraph(name='cluster_security') as security:
            security.attr(label='Security & Identity Services', margin='10', bgcolor='lightyellow')

            with security.subgraph(name='cluster_cert_manager') as cert_cluster:
                cert_cluster.attr(label='cert-manager-operator', margin='10', bgcolor='white', style='rounded', labeljust='c')
                cert_cluster.node('cert_manager', label=html_node(CERT_MANAGER_ICON, 'Cert Manager For<br/>Red Hat OpenShift'), shape='none')

            with security.subgraph(name='cluster_kuadrant') as kuadrant_cluster:
                kuadrant_cluster.attr(label='kuadrant-system', margin='10', bgcolor='white', style='rounded', labeljust='c')
                kuadrant_cluster.node('authorino', label=html_node(AUTHORINO_ICON, 'Authorino<br/>Operator'), shape='none')
                kuadrant_cluster.node('limitador', label=html_node(LIMITADOR_ICON, 'Limitador<br/>Operator'), shape='none')
                kuadrant_cluster.node('dns', label=html_node(DNS_ICON, 'DNS<br/>Operator'), shape='none')
                kuadrant_cluster.node('connectivity_link', label=html_node(RHCL_ICON, 'Red Hat<br/>Connectivity Link<br/>Operator'), shape='none')

            with security.subgraph(name='cluster_ossm') as ossm_cluster:
                ossm_cluster.attr(label='OpenShift\nOperators', margin='10', bgcolor='white', style='rounded', labeljust='c')
                ossm_cluster.node('ossm', label=html_node(OSSM_ICON, 'OpenShift<br/>Service Mesh'), shape='none')

        # Developer Services
        with services.subgraph(name='cluster_developer') as developer:
            developer.attr(label='Developer Services', margin='10', bgcolor='lightyellow')

            with developer.subgraph(name='cluster_builds') as builds_cluster:
                builds_cluster.attr(label='openshift-builds', margin='10', bgcolor='white', style='rounded', labeljust='c')
                builds_cluster.node('builds', label=html_node(BUILDS_ICON, 'Builds For<br/>Red Hat OpenShift'), shape='none')

            with developer.subgraph(name='cluster_pipelines') as pipelines_cluster:
                pipelines_cluster.attr(label='openshift-pipelines', margin='10', bgcolor='white', style='rounded', labeljust='c')
                pipelines_cluster.node('pipelines', label=html_node(PIPELINES_ICON, 'OpenShift<br/>Pipelines Operator'), shape='none')

            with developer.subgraph(name='cluster_gitops') as gitops_cluster:
                gitops_cluster.attr(label='openshift-gitops-operator', margin='10', bgcolor='white', style='rounded', labeljust='c')
                gitops_cluster.node('gitops', label=html_node(GITOPS_ICON, 'OpenShift<br/>GitOps Operator'), shape='none')

        # Storage Services
        with services.subgraph(name='cluster_storage') as storage:
            storage.attr(label='Storage Services', margin='10', bgcolor='lightyellow')

            with storage.subgraph(name='cluster_odf') as odf_cluster:
                odf_cluster.attr(label='openshift-storage', margin='10', bgcolor='white', style='rounded', labeljust='c')
                odf_cluster.node('odf', label=html_node(ODF_ICON, 'OpenShift Data<br/>Foundation<br/>Operator'), shape='none')

        # Core Components (20 essential components - no namespace rectangles, just icons)
        with services.subgraph(name='cluster_core') as core:
            core.attr(label='Core Components', margin='10', bgcolor='lightyellow')

            # Row 1: Control Plane + Networking (10 items)
            core.node('api_server', label=html_node(OPENSHIFT_ICON, 'API Server'), shape='none')
            core.node('authentication', label=html_node(OPENSHIFT_ICON, 'Authentication'), shape='none')
            core.node('etcd', label=html_node(OPENSHIFT_ICON, 'Etcd'), shape='none')
            core.node('controller', label=html_node(OPENSHIFT_ICON, 'Controller'), shape='none')
            core.node('scheduler', label=html_node(OPENSHIFT_ICON, 'Scheduler'), shape='none')
            core.node('dns_core', label=html_node(OPENSHIFT_ICON, 'DNS'), shape='none')
            core.node('ingress', label=html_node(OPENSHIFT_ICON, 'Ingress'), shape='none')
            core.node('ovn', label=html_node(OPENSHIFT_ICON, 'OVN'), shape='none')
            core.node('multus', label=html_node(OPENSHIFT_ICON, 'Multus'), shape='none')
            core.node('console', label=html_node(OPENSHIFT_ICON, 'Console'), shape='none')

            # Row 2: Management + Storage + Infrastructure + Security (10 items)
            core.node('olm', label=html_node(OPENSHIFT_ICON, 'OLM'), shape='none')
            core.node('insights', label=html_node(OPENSHIFT_ICON, 'Insights'), shape='none')
            core.node('marketplace', label=html_node(OPENSHIFT_ICON, 'Marketplace'), shape='none')
            core.node('image_registry', label=html_node(OPENSHIFT_ICON, 'Image Registry'), shape='none')
            core.node('cluster_storage', label=html_node(OPENSHIFT_ICON, 'Cluster Storage'), shape='none')
            core.node('machine_api', label=html_node(OPENSHIFT_ICON, 'Machine API'), shape='none')
            core.node('machine_config', label=html_node(OPENSHIFT_ICON, 'Machine Config'), shape='none')
            core.node('tuned', label=html_node(OPENSHIFT_ICON, 'Tuned'), shape='none')
            core.node('service_ca', label=html_node(OPENSHIFT_ICON, 'Service CA'), shape='none')
            core.node('cloud_credential', label=html_node(OPENSHIFT_ICON, 'Cloud Credential'), shape='none')

            # Stack Row 2 below Row 1 using vertical edges
            core.edge('api_server', 'olm', style='invis')
            core.edge('authentication', 'insights', style='invis')
            core.edge('etcd', 'marketplace', style='invis')
            core.edge('controller', 'image_registry', style='invis')
            core.edge('scheduler', 'cluster_storage', style='invis')
            core.edge('dns_core', 'machine_api', style='invis')
            core.edge('ingress', 'machine_config', style='invis')
            core.edge('ovn', 'tuned', style='invis')
            core.edge('multus', 'service_ca', style='invis')
            core.edge('console', 'cloud_credential', style='invis')

    # RHOAI Platform (runs on OCP)
    with ocp.subgraph(name='cluster_rhoai') as rhoai:
        rhoai.attr(label='Red Hat OpenShift AI Platform', margin='15', bgcolor='lightblue')

        with rhoai.subgraph(name='cluster_rhoai_apps') as apps:
            apps.attr(label='redhat-ods-applications', margin='10', bgcolor='white', style='rounded', labeljust='c')
            apps.node('rhoai_platform', label=html_node(RHOAI_ICON, 'Red Hat<br/>OpenShift AI'), shape='none')

        with rhoai.subgraph(name='cluster_rhoai_mon') as mon:
            mon.attr(label='redhat-ods-monitoring', margin='10', bgcolor='white', style='rounded', labeljust='c')
            mon.node('rhoai_monitoring', label=html_node(CLUSTER_OBSERVABILITY_ICON, 'RHOAI<br/>Monitoring'), shape='none')

        with rhoai.subgraph(name='cluster_notebooks') as notebooks:
            notebooks.attr(label='rhods-notebooks', margin='10', bgcolor='white', style='rounded', labeljust='c')
            notebooks.node('jupyter_workbench', label=html_node(JUPYTER_ICON, 'Jupyter<br/>Workbench'), shape='none')
            notebooks.node('vscode_workbench', label=html_node(VSCODE_ICON, 'Code Server<br/>Workbench'), shape='none')

        with rhoai.subgraph(name='cluster_project_a') as proj_a:
            proj_a.attr(label='AI Project A', margin='10', bgcolor='white', style='rounded', labeljust='c')
            proj_a.node('ai_workload_a', label=html_node(AI_MODEL_ICON, 'AI<br/>Workload'), shape='none')

        with rhoai.subgraph(name='cluster_project_b') as proj_b:
            proj_b.attr(label='AI Project B', margin='10', bgcolor='white', style='rounded', labeljust='c')
            proj_b.node('ai_workload_b', label=html_node(AI_MODEL_ICON, 'AI<br/>Workload'), shape='none')

        with rhoai.subgraph(name='cluster_project_c') as proj_c:
            proj_c.attr(label='AI Project C', margin='10', bgcolor='white', style='rounded', labeljust='c')
            proj_c.node('ai_workload_c', label=html_node(AI_MODEL_ICON, 'AI<br/>Workload'), shape='none')

        with rhoai.subgraph(name='cluster_project_d') as proj_d:
            proj_d.attr(label='AI Project D', margin='10', bgcolor='white', style='rounded', labeljust='c')
            proj_d.node('ai_workload_d', label=html_node(AI_MODEL_ICON, 'AI<br/>Workload'), shape='none')

        with rhoai.subgraph(name='cluster_project_e') as proj_e:
            proj_e.attr(label='AI Project E', margin='10', bgcolor='white', style='rounded', labeljust='c')
            proj_e.node('ai_workload_e', label=html_node(AI_MODEL_ICON, 'AI<br/>Workload'), shape='none')

        with rhoai.subgraph(name='cluster_project_f') as proj_f:
            proj_f.attr(label='AI Project F', margin='10', bgcolor='white', style='rounded', labeljust='c')
            proj_f.node('ai_workload_f', label=html_node(AI_MODEL_ICON, 'AI<br/>Workload'), shape='none')

        with rhoai.subgraph(name='cluster_project_g') as proj_g:
            proj_g.attr(label='AI Project G', margin='10', bgcolor='white', style='rounded', labeljust='c')
            proj_g.node('ai_workload_g', label=html_node(AI_MODEL_ICON, 'AI<br/>Workload'), shape='none')

        with rhoai.subgraph(name='cluster_project_h') as proj_h:
            proj_h.attr(label='AI Project H', margin='10', bgcolor='white', style='rounded', labeljust='c')
            proj_h.node('ai_workload_h', label=html_node(AI_MODEL_ICON, 'AI<br/>Workload'), shape='none')

# Force 4-row layout with distributed anchor points

# Force Row 2 (OCP Compute & Observability) below Row 1 (RHOAI)
dot.edge('rhoai_platform', 'gpu_operator', style='invis')
dot.edge('rhoai_monitoring', 'nfd', style='invis')
dot.edge('jupyter_workbench', 'kueue', style='invis')
dot.edge('vscode_workbench', 'lws', style='invis')
dot.edge('ai_workload_a', 'cluster_monitoring', style='invis')
dot.edge('ai_workload_b', 'udwm', style='invis')
dot.edge('ai_workload_c', 'grafana', style='invis')
dot.edge('ai_workload_d', 'cluster_observability', style='invis')
dot.edge('ai_workload_e', 'openshift_logging', style='invis')
dot.edge('ai_workload_f', 'loki', style='invis')
dot.edge('ai_workload_g', 'opentelemetry', style='invis')
dot.edge('ai_workload_h', 'tempo', style='invis')

# Force Row 3 (OCP Security/Developer/Storage) below Row 2
dot.edge('gpu_operator', 'cert_manager', style='invis')
dot.edge('nfd', 'authorino', style='invis')
dot.edge('kueue', 'builds', style='invis')
dot.edge('lws', 'pipelines', style='invis')
dot.edge('cluster_monitoring', 'gitops', style='invis')
dot.edge('udwm', 'odf', style='invis')
dot.edge('grafana', 'ossm', style='invis')
dot.edge('netobserv', 'connectivity_link', style='invis')

# Force Row 4 (Core Components) below Row 3 - distributed anchors
dot.edge('cert_manager', 'api_server', style='invis')
dot.edge('authorino', 'authentication', style='invis')
dot.edge('limitador', 'etcd', style='invis')
dot.edge('builds', 'controller', style='invis')
dot.edge('pipelines', 'scheduler', style='invis')
dot.edge('gitops', 'dns_core', style='invis')
dot.edge('odf', 'ingress', style='invis')
dot.edge('ossm', 'console', style='invis')

# Render diagram
dot.render(format='png', view=False, quiet=True)

print("✓ Generated: output/rhoai-ocp-integration.png (Direct Graphviz with HTML tables)")
print("  → 4-row layout: RHOAI Platform (Row 1) + OCP Services (Rows 2-4)")
print("  → Row 1: RHOAI (11 namespaces)")
print("  → Row 2: Compute & Acceleration (4), Observability (9)")
print("  → Row 3: Security & Identity (6), Developer (3), Storage (1)")
print("  → Row 4: Core Components (20 essential components in 2-row grid)")
print("  → All icons perfectly centered with HTML table labels!")
