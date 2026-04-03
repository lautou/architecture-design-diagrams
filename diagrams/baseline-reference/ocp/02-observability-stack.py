"""
OpenShift Container Platform - Observability Stack Baseline

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
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.controlplane import APIServer
from diagrams.onprem.monitoring import Prometheus, Grafana
from diagrams.onprem.logging import Loki
from diagrams.onprem.tracing import Jaeger
from diagrams.onprem.database import Clickhouse
from diagrams.onprem.compute import Server
from diagrams.custom import Custom
import os

# Get absolute paths for icons
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(BASE_DIR, '../../..')
OPERATOR_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Technology icons/operator/Technology_icon-Red_Hat-operator-Standard-RGB.Large_icon_transparent.png")
OTEL_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Technology icons/Red Hat build of OpenTelemetry/Technology_icon-Red_Hat-OpenTelemetry-Standard-RGB.Large_icon_transparent.png")
CLUSTER_OBS_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Technology icons/Cluster observability/Technology_icon-Red_Hat-Cluster_observability_operator-Standard-RGB.Large_icon_transparent.png")

graph_attr = {
    "fontsize": "16",
    "bgcolor": "white",
    "pad": "0.5",
    "nodesep": "1.0",
    "ranksep": "1.8"
}

with Diagram(
    "OCP Baseline - Observability Stack (Namespace-Based)",
    show=False,
    direction="TB",
    filename="output/baseline-ocp-02-observability-stack",
    graph_attr=graph_attr
):

    api = APIServer("\nOpenShift\nAPI Server")

    # ========== LAYER 1: EMBEDDED MONITORING ==========
    with Cluster("LAYER 1: Embedded Monitoring (Built-in)"):

        with Cluster("openshift-monitoring"):
            with Cluster("Cluster Monitoring"):
                cluster_prom = Prometheus("\nPrometheus\n(Platform Metrics)")
                cluster_alert = Prometheus("\nAlertmanager\n(Platform Alerts)")

        with Cluster("openshift-user-workload-monitoring"):
            with Cluster("User Defined Workload Monitoring"):
                udwm_prom = Prometheus("\nPrometheus\n(User Metrics)")
                thanos = Prometheus("\nThanos Querier\n(Unified)")

    # ========== LAYER 2: ADD-ON OPERATORS ==========
    with Cluster("LAYER 2: Add-on Observability Operators"):

        with Cluster("openshift-logging"):
            logging_operator = Custom("\nLogging Operator", OPERATOR_ICON)

            with Cluster("Log Collection & Storage"):
                log_collector = Loki("\nVector/Fluentd\n(Collector)")
                loki_stack = Loki("\nLokiStack\n(Storage)")

        with Cluster("openshift-tempo-operator"):
            tempo_operator = Custom("\nTempo Operator", OPERATOR_ICON)
            tempo = Jaeger("\nTempo\n(Distributed Tracing)")

        with Cluster("openshift-opentelemetry-operator"):
            otel_operator = Custom("\nOpenTelemetry\nOperator", OTEL_ICON)
            otel_collector = Jaeger("\nOTel Collector\n(OTLP)")

        with Cluster("openshift-cluster-observability-operator"):
            cluster_obs_operator = Custom("\nCluster Observability\nOperator", CLUSTER_OBS_ICON)

        with Cluster("netobserv"):
            network_obs_operator = Custom("\nNetwork Observability\nOperator", OPERATOR_ICON)
            flow_collector = Clickhouse("\nFlow Collector\n(eBPF)")

        with Cluster("openshift-operators (Grafana)"):
            grafana_operator = Custom("\nGrafana Operator", OPERATOR_ICON)
            grafana = Grafana("\nGrafana\n(Custom Dashboards)")

    # ========== APPLICATION WORKLOADS ==========
    with Cluster("Application Workloads"):
        platform_apps = Server("\nPlatform\nComponents")
        user_apps = Server("\nUser\nApplications")

    # ========== EXTERNAL INTEGRATION ==========
    with Cluster("External Integration"):
        external_storage = Server("\nExternal Storage\n(S3/NFS)")
        external_siem = Server("\nExternal SIEM\n(Splunk, Elastic)")

    # =========================================================
    # CONNECTIONS
    # =========================================================

    # --- OPERATOR MANAGEMENT (Orange) ---
    api >> Edge(color="orange") >> logging_operator
    api >> Edge(color="orange") >> tempo_operator
    api >> Edge(color="orange") >> otel_operator
    api >> Edge(color="orange") >> network_obs_operator
    api >> Edge(color="orange") >> grafana_operator
    api >> Edge(color="orange") >> cluster_obs_operator

    logging_operator >> Edge(color="orange") >> [log_collector, loki_stack]
    tempo_operator >> Edge(color="orange") >> tempo
    otel_operator >> Edge(color="orange") >> otel_collector
    network_obs_operator >> Edge(color="orange") >> flow_collector
    grafana_operator >> Edge(color="orange") >> grafana

    # --- EMBEDDED MONITORING FLOW (Purple) ---
    cluster_prom >> Edge(color="purple") >> cluster_alert
    udwm_prom >> Edge(color="purple") >> thanos
    cluster_prom >> Edge(color="purple") >> thanos

    # --- DATA COLLECTION (Blue) ---
    platform_apps >> Edge(color="blue", style="dotted", label="platform metrics") >> cluster_prom
    user_apps >> Edge(color="blue", style="dotted", label="user metrics") >> udwm_prom
    user_apps >> Edge(color="blue", style="dotted", label="logs") >> log_collector
    user_apps >> Edge(color="blue", style="dotted", label="traces") >> otel_collector

    # Log flow
    log_collector >> Edge(color="blue", label="forward") >> loki_stack

    # OTel distribution
    otel_collector >> Edge(color="purple", label="traces") >> tempo
    otel_collector >> Edge(color="purple", label="metrics") >> udwm_prom
    otel_collector >> Edge(color="purple", label="logs") >> loki_stack

    # --- VISUALIZATION (Purple queries) ---
    grafana >> Edge(color="purple", style="dashed", label="query") >> thanos
    grafana >> Edge(color="purple", style="dashed", label="query") >> loki_stack
    grafana >> Edge(color="purple", style="dashed", label="query") >> tempo
    grafana >> Edge(color="purple", style="dashed", label="query") >> flow_collector

    # --- EXTERNAL INTEGRATION ---
    loki_stack >> Edge(style="dotted", label="export") >> external_storage
    log_collector >> Edge(style="dotted", label="forward") >> external_siem

    # --- CLUSTER OBSERVABILITY COORDINATION ---
    cluster_obs_operator >> Edge(color="orange", style="dashed", label="configure") >> grafana
    cluster_obs_operator >> Edge(color="orange", style="dashed", label="configure") >> thanos

    # --- ALERTS (Red) ---
    cluster_alert >> Edge(color="red", style="bold", label="platform alerts") >> external_siem

print("✓ Generated: output/baseline-ocp-02-observability-stack.png")
print("  → Namespace-based: openshift-monitoring → openshift-logging → netobserv")
print("  → Color-coded: Orange=management, Purple=observability, Blue=data, Red=alerts")
