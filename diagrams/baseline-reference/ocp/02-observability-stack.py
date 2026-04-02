"""
OpenShift Container Platform - Observability Stack Baseline

This diagram shows the complete observability stack including:
- Embedded monitoring (Cluster Monitoring, User Defined Workload Monitoring)
- Add-on operators for enhanced observability
- Integration points for metrics, logs, and traces

Note: No pod-level representation - focus on logical components and data flows
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.controlplane import APIServer
from diagrams.k8s.network import Service
from diagrams.onprem.monitoring import Prometheus, Grafana
from diagrams.onprem.logging import Loki
from diagrams.onprem.tracing import Jaeger
from diagrams.onprem.database import Clickhouse

graph_attr = {
    "fontsize": "16",
    "bgcolor": "white",
    "pad": "0.5",
    "nodesep": "1.0",
    "ranksep": "1.2"
}

with Diagram(
    "OCP Baseline - Observability Stack",
    show=False,
    direction="TB",
    filename="output/baseline-ocp-02-observability-stack",
    graph_attr=graph_attr
):

    api = APIServer("OpenShift\nAPI Server")

    with Cluster("Embedded Monitoring (Built-in)"):
        with Cluster("Cluster Monitoring"):
            cluster_prom = Prometheus("Prometheus\n(Platform Metrics)")
            cluster_alert = Service("Alertmanager\n(Platform Alerts)")

            cluster_prom >> cluster_alert

        with Cluster("User Defined Workload Monitoring (UDWM)"):
            udwm_prom = Prometheus("Prometheus\n(User Workload Metrics)")
            udwm_thanos = Service("Thanos Querier\n(Unified Query)")

            udwm_prom >> udwm_thanos
            cluster_prom >> udwm_thanos

    with Cluster("Add-on Observability Operators"):

        with Cluster("Logging"):
            logging_operator = Service("OpenShift Logging\nOperator")
            log_collector = Service("Vector/Fluentd\n(Log Collection)")
            log_store = Loki("LokiStack\n(Log Storage)")

            logging_operator >> [log_collector, log_store]
            log_collector >> Edge(label="forward") >> log_store

        with Cluster("Distributed Tracing"):
            tempo_operator = Service("Tempo Operator")
            tempo = Jaeger("Tempo\n(Trace Storage)")

            tempo_operator >> tempo

        with Cluster("OpenTelemetry"):
            otel_operator = Service("OpenTelemetry\nOperator")
            otel_collector = Service("OTel Collector\n(Metrics, Logs, Traces)")

            otel_operator >> otel_collector
            otel_collector >> Edge(label="traces") >> tempo
            otel_collector >> Edge(label="metrics") >> udwm_prom
            otel_collector >> Edge(label="logs") >> log_store

        with Cluster("Enhanced Observability"):
            cluster_obs_operator = Service("Cluster Observability\nOperator")

            network_obs_operator = Service("Network Observability\nOperator")
            network_flow = Clickhouse("Flow Collector\n(Network Flows)")

            network_obs_operator >> network_flow

        with Cluster("Visualization"):
            grafana_operator = Service("Grafana Operator")
            grafana = Grafana("Grafana\n(Custom Dashboards)")

            grafana_operator >> grafana

    with Cluster("Application Workloads"):
        app_workloads = Service("Applications\n(Platform & User)")

    with Cluster("External Integration"):
        external_storage = Service("External Storage\n(S3/NFS for logs)")
        external_siem = Service("External SIEM\n(Splunk, Elastic, etc)")

    # API integration
    api >> [logging_operator, tempo_operator, otel_operator, network_obs_operator, grafana_operator, cluster_obs_operator]

    # Data collection from workloads
    app_workloads >> Edge(label="metrics") >> cluster_prom
    app_workloads >> Edge(label="user metrics") >> udwm_prom
    app_workloads >> Edge(label="logs") >> log_collector
    app_workloads >> Edge(label="traces") >> otel_collector

    # Grafana queries all sources
    grafana >> Edge(label="query", style="dashed") >> udwm_thanos
    grafana >> Edge(label="query", style="dashed") >> log_store
    grafana >> Edge(label="query", style="dashed") >> tempo
    grafana >> Edge(label="query", style="dashed") >> network_flow

    # External integration
    log_store >> Edge(label="export", style="dotted") >> external_storage
    log_collector >> Edge(label="forward", style="dotted") >> external_siem

    # Cluster observability coordinates
    cluster_obs_operator >> Edge(label="configure", style="dashed") >> [grafana, udwm_thanos, log_store]

print("✓ Generated: output/baseline-ocp-02-observability-stack.png")
