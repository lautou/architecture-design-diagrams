"""
OpenShift Container Platform - Observability Stack Baseline (Direct Graphviz)

Namespace-based layered architecture for observability:
- LAYER 1: Embedded Monitoring (openshift-monitoring, openshift-user-workload-monitoring)
- LAYER 2: Add-on Operators (openshift-logging, openshift-tempo-operator, etc.)
- Integration with external systems

Color-coded connections:
- Purple: Observability/monitoring flows
- Orange: Operator management
- Blue: Data ingestion
- Red: Alerts

Note: Shows actual OpenShift observability namespaces
Uses direct Graphviz with HTML table labels for perfect icon centering
"""

from graphviz import Digraph
import os

# Get absolute paths for icons
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(BASE_DIR, '../../..')

# Icon paths
OPERATOR_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Technology icons/operator/Technology_icon-Red_Hat-operator-Standard-RGB.Large_icon_transparent.png")
OTEL_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Technology icons/Red Hat build of OpenTelemetry/Technology_icon-Red_Hat-build_of_OpenTelemetry-Standard-RGB.Large_icon_transparent.png")
CLUSTER_OBS_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Technology icons/Cluster observability/Technology_icon-Red_Hat-cluster_observability-Standard-RGB.Large_icon_transparent.png")
MONITORING_ICON = os.path.join(PROJECT_ROOT, "custom_icons/UI icons/rh-ui-icon-monitoring-fill.Large_icon_transparent.png")
GRAFANA_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/Grafana/grafana-400x400.png")
LOKI_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/Loki/loki-400x400.png")
TEMPO_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/Tempo/tempo-400x400.png")
OPENSHIFT_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Technology icons/Red Hat OpenShift/Technology_icon-Red_Hat-OpenShift-Standard-RGB.Large_icon_transparent.png")

# Helper function
def html_node(icon_path, label_text):
    """Create HTML table label for perfect centering"""
    return f'''<<table border="0">
<tr><td><img src="{icon_path}"/></td></tr>
<tr><td>{label_text}</td></tr>
</table>>'''

# Create diagram
dot = Digraph("OCP_Observability_Stack", filename="output/baseline-ocp-02-observability-stack")
dot.attr(rankdir="TB")
dot.attr(fontsize="16", bgcolor="white", pad="0.5", nodesep="1.0", ranksep="1.8")

# API Server
dot.node('api', label=html_node(OPENSHIFT_ICON, 'OpenShift<br/>API Server'), shape='none')

# ========== LAYER 1: EMBEDDED MONITORING ==========
with dot.subgraph(name='cluster_layer1') as layer1:
    layer1.attr(label='LAYER 1: Embedded Monitoring (Built-in)')

    # openshift-monitoring
    with layer1.subgraph(name='cluster_monitoring') as monitoring:
        monitoring.attr(label='openshift-monitoring')

        with monitoring.subgraph(name='cluster_cluster_monitoring') as cm:
            cm.attr(label='Cluster Monitoring')
            cm.node('cluster_prom', label=html_node(MONITORING_ICON, 'Prometheus<br/>(Platform Metrics)'), shape='none')
            cm.node('cluster_alert', label=html_node(MONITORING_ICON, 'Alertmanager<br/>(Platform Alerts)'), shape='none')

    # openshift-user-workload-monitoring
    with layer1.subgraph(name='cluster_udwm') as udwm_cluster:
        udwm_cluster.attr(label='openshift-user-workload-monitoring')

        with udwm_cluster.subgraph(name='cluster_udwm_inner') as udwm:
            udwm.attr(label='User Defined Workload Monitoring')
            udwm.node('udwm_prom', label=html_node(MONITORING_ICON, 'Prometheus<br/>(User Metrics)'), shape='none')
            udwm.node('thanos', label=html_node(MONITORING_ICON, 'Thanos Querier<br/>(Unified)'), shape='none')

# ========== LAYER 2: ADD-ON OPERATORS ==========
with dot.subgraph(name='cluster_layer2') as layer2:
    layer2.attr(label='LAYER 2: Add-on Observability Operators')

    # openshift-logging
    with layer2.subgraph(name='cluster_logging') as logging:
        logging.attr(label='openshift-logging')
        logging.node('logging_operator', label=html_node(OPERATOR_ICON, 'Logging Operator'), shape='none')

        with logging.subgraph(name='cluster_log_collection') as log_collect:
            log_collect.attr(label='Log Collection & Storage')
            log_collect.node('log_collector', label=html_node(LOKI_ICON, 'Vector/Fluentd<br/>(Collector)'), shape='none')
            log_collect.node('loki_stack', label=html_node(LOKI_ICON, 'LokiStack<br/>(Storage)'), shape='none')

    # openshift-tempo-operator
    with layer2.subgraph(name='cluster_tempo') as tempo_cluster:
        tempo_cluster.attr(label='openshift-tempo-operator')
        tempo_cluster.node('tempo_operator', label=html_node(OPERATOR_ICON, 'Tempo Operator'), shape='none')
        tempo_cluster.node('tempo', label=html_node(TEMPO_ICON, 'Tempo<br/>(Distributed Tracing)'), shape='none')

    # openshift-opentelemetry-operator
    with layer2.subgraph(name='cluster_otel') as otel_cluster:
        otel_cluster.attr(label='openshift-opentelemetry-operator')
        otel_cluster.node('otel_operator', label=html_node(OTEL_ICON, 'OpenTelemetry<br/>Operator'), shape='none')
        otel_cluster.node('otel_collector', label=html_node(OTEL_ICON, 'OTel Collector<br/>(OTLP)'), shape='none')

    # openshift-cluster-observability-operator
    with layer2.subgraph(name='cluster_cluster_obs') as cluster_obs:
        cluster_obs.attr(label='openshift-cluster-observability-operator')
        cluster_obs.node('cluster_obs_operator', label=html_node(CLUSTER_OBS_ICON, 'Cluster Observability<br/>Operator'), shape='none')

    # netobserv
    with layer2.subgraph(name='cluster_netobserv') as netobserv:
        netobserv.attr(label='netobserv')
        netobserv.node('network_obs_operator', label=html_node(OPERATOR_ICON, 'Network Observability<br/>Operator'), shape='none')
        netobserv.node('flow_collector', label=html_node(OPENSHIFT_ICON, 'Flow Collector<br/>(eBPF)'), shape='none')

    # openshift-operators (Grafana)
    with layer2.subgraph(name='cluster_grafana') as grafana_cluster:
        grafana_cluster.attr(label='openshift-operators (Grafana)')
        grafana_cluster.node('grafana_operator', label=html_node(OPERATOR_ICON, 'Grafana Operator'), shape='none')
        grafana_cluster.node('grafana', label=html_node(GRAFANA_ICON, 'Grafana<br/>(Custom Dashboards)'), shape='none')

# ========== APPLICATION WORKLOADS ==========
with dot.subgraph(name='cluster_apps') as apps:
    apps.attr(label='Application Workloads')
    apps.node('platform_apps', label=html_node(OPENSHIFT_ICON, 'Platform<br/>Components'), shape='none')
    apps.node('user_apps', label=html_node(OPENSHIFT_ICON, 'User<br/>Applications'), shape='none')

# ========== EXTERNAL INTEGRATION ==========
with dot.subgraph(name='cluster_external') as external:
    external.attr(label='External Integration')
    external.node('external_storage', label=html_node(OPENSHIFT_ICON, 'External Storage<br/>(S3/NFS)'), shape='none')
    external.node('external_siem', label=html_node(OPENSHIFT_ICON, 'External SIEM<br/>(Splunk, Elastic)'), shape='none')

# =========================================================
# CONNECTIONS
# =========================================================

# --- OPERATOR MANAGEMENT (Orange) ---
dot.edge('api', 'logging_operator', color='orange')
dot.edge('api', 'tempo_operator', color='orange')
dot.edge('api', 'otel_operator', color='orange')
dot.edge('api', 'network_obs_operator', color='orange')
dot.edge('api', 'grafana_operator', color='orange')
dot.edge('api', 'cluster_obs_operator', color='orange')

dot.edge('logging_operator', 'log_collector', color='orange')
dot.edge('logging_operator', 'loki_stack', color='orange')
dot.edge('tempo_operator', 'tempo', color='orange')
dot.edge('otel_operator', 'otel_collector', color='orange')
dot.edge('network_obs_operator', 'flow_collector', color='orange')
dot.edge('grafana_operator', 'grafana', color='orange')

# --- EMBEDDED MONITORING FLOW (Purple) ---
dot.edge('cluster_prom', 'cluster_alert', color='purple')
dot.edge('udwm_prom', 'thanos', color='purple')
dot.edge('cluster_prom', 'thanos', color='purple')

# --- DATA COLLECTION (Blue) ---
dot.edge('platform_apps', 'cluster_prom', color='blue', style='dotted', label='platform metrics')
dot.edge('user_apps', 'udwm_prom', color='blue', style='dotted', label='user metrics')
dot.edge('user_apps', 'log_collector', color='blue', style='dotted', label='logs')
dot.edge('user_apps', 'otel_collector', color='blue', style='dotted', label='traces')

# Log flow
dot.edge('log_collector', 'loki_stack', color='blue', label='forward')

# OTel distribution
dot.edge('otel_collector', 'tempo', color='purple', label='traces')
dot.edge('otel_collector', 'udwm_prom', color='purple', label='metrics')
dot.edge('otel_collector', 'loki_stack', color='purple', label='logs')

# --- VISUALIZATION (Purple queries) ---
dot.edge('grafana', 'thanos', color='purple', style='dashed', label='query')
dot.edge('grafana', 'loki_stack', color='purple', style='dashed', label='query')
dot.edge('grafana', 'tempo', color='purple', style='dashed', label='query')
dot.edge('grafana', 'flow_collector', color='purple', style='dashed', label='query')

# --- EXTERNAL INTEGRATION ---
dot.edge('loki_stack', 'external_storage', style='dotted', label='export')
dot.edge('log_collector', 'external_siem', style='dotted', label='forward')

# --- CLUSTER OBSERVABILITY COORDINATION ---
dot.edge('cluster_obs_operator', 'grafana', color='orange', style='dashed', label='configure')
dot.edge('cluster_obs_operator', 'thanos', color='orange', style='dashed', label='configure')

# --- ALERTS (Red) ---
dot.edge('cluster_alert', 'external_siem', color='red', style='bold', label='platform alerts')

# Render diagram
dot.render(format='png', view=False, quiet=True)

print("✓ Generated: output/baseline-ocp-02-observability-stack.png (Direct Graphviz with HTML tables)")
print("  → Namespace-based: openshift-monitoring → openshift-logging → netobserv")
print("  → Color-coded: Orange=management, Purple=observability, Blue=data, Red=alerts")
print("  → All icons perfectly centered!")
