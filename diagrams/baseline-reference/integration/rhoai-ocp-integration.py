"""
RHOAI on OCP - Integration Architecture

Shows RHOAI platform running on OpenShift Container Platform with OCP services.

Structure:
- OpenShift Container Platform (outer cluster)
  - OCP Platform Services (5 categories with namespace rectangles):
    - Compute & Acceleration: NVIDIA GPU Operator, NFD, Kueue, Leader Worker Set
    - Observability: Cluster Monitoring, UDWM, Grafana, Cluster Observability, Logging, Loki, OpenTelemetry, Tempo, Network Observability
    - Security & Identity Services: cert-manager, Authorino, Limitador, DNS, RHCL (kuadrant-system), OpenShift Service Mesh
    - Developer Services: Builds, Pipelines, GitOps (Builds/Pipelines for MLOps)
    - Storage Services: OpenShift Data Foundation
  - Red Hat OpenShift AI Platform (runs on OCP):
    - redhat-ods-applications: RHOAI operator
    - redhat-ods-monitoring: RHOAI monitoring stack
    - ai-project-A: Sample AI workload
    - ai-project-B: Sample AI workload

Each operator is shown within its deployment namespace as a white rounded rectangle.

Layout: 3-row layout with distributed anchor points:
- Row 1: Compute & Acceleration, Observability
- Row 2: Security & Identity Services, Developer Services, Storage Services
- Row 3: RHOAI Platform

Technical Notes:
- Uses 8 distributed invisible vertical edges to force 3-row layout
- Single-node namespace clusters may show slight left-alignment due to Graphviz
  constraint solver behavior (trade-off between perfect centering vs stable layout)
- Namespace cluster attributes: margin=10, bgcolor=white, style=rounded, labeljust=c
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom
import os

# Calculate absolute paths for custom icons
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(BASE_DIR, '../../..')
OPERATOR_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Technology icons/operator/Technology_icon-Red_Hat-operator-Standard-RGB.Large_icon_transparent.png")
MONITORING_ICON = os.path.join(PROJECT_ROOT, "custom_icons/UI icons/rh-ui-icon-monitoring-fill.Large_icon_transparent.png")
BUILDS_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Technology icons/Builds for Red Hat OpenShift/Technology_icon-Red_Hat-builds_for_Red_Hat_OpenShift-Standard-RGB.Large_icon_transparent.png")
TEMPO_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/Tempo/tempo-400x400.png")
OSSM_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/OSSM/ossm-400x400.png")
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
CLUSTER_OBSERVABILITY_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Technology icons/Cluster observability/Technology_icon-Red_Hat-cluster_observability-Red-RGB.Large_icon_transparent.png")

graph_attr = {
    "fontsize": "9",
    "bgcolor": "white",
    "pad": "0.5",
    "nodesep": "1.0",
    "ranksep": "1.0",
    "dpi": "300"
}

node_attr = {
    "margin": "0.5,0.3"
}

with Diagram(
    "RHOAI on OCP - Integration Architecture",
    show=False,
    direction="TB",
    filename="output/rhoai-ocp-integration",
    graph_attr=graph_attr,
    node_attr=node_attr
):

    # ========== OCP PLATFORM ==========
    with Cluster("OpenShift Container Platform", graph_attr={"margin": "20", "bgcolor": "lightgray"}):

        # OCP Platform Services
        with Cluster("OCP Platform Services", graph_attr={"margin": "15", "bgcolor": "lightgreen"}):

            # Compute & Acceleration
            with Cluster("Compute & Acceleration", graph_attr={"margin": "10", "bgcolor": "lightyellow"}):
                with Cluster("nvidia-gpu-operator", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                    gpu_operator = Custom("\nNVIDIA GPU\nOperator", NVIDIA_ICON)

                with Cluster("openshift-nfd", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                    nfd = Custom("\nNode Feature\nDiscovery Operator", NFD_ICON)

                with Cluster("openshift-kueue-operator", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                    kueue = Custom("\nRed Hat build of\nKueue Operator", KUEUE_ICON)

                with Cluster("openshift-lws-operator", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                    lws = Custom("\nRed Hat build of\nLeader Worker Set\nOperator", LWS_ICON)

            # Observability
            with Cluster("Observability", graph_attr={"margin": "10", "bgcolor": "lightyellow"}):
                with Cluster("openshift-monitoring", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                    cluster_monitoring = Custom("\nCluster Monitoring", MONITORING_ICON)

                with Cluster("openshift-user-workload-monitoring", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                    udwm = Custom("\nUser-Defined\nWorkload Monitoring", MONITORING_ICON)

                with Cluster("grafana-operator", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                    grafana = Custom("\nGrafana\nOperator", GRAFANA_ICON)

                with Cluster("openshift-observability-operator", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                    cluster_observability = Custom("\nCluster Observability\nOperator", OBSERVABILITY_ICON)

                with Cluster("openshift-logging", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                    openshift_logging = Custom("\nOpenShift\nLogging Operator", LOGGING_ICON)

                with Cluster("openshift-operators-redhat", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                    loki = Custom("\nLoki\nOperator", LOKI_ICON)

                with Cluster("openshift-opentelemetry-operator", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                    opentelemetry = Custom("\nRed Hat build of\nOpenTelemetry", OPENTELEMETRY_ICON)

                with Cluster("openshift-tempo-operator", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                    tempo = Custom("\nTempo\nOperator", TEMPO_ICON)

                with Cluster("openshift-netobserv-operator", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                    netobserv = Custom("\nNetwork\nObservability\nOperator", NETWORK_OBSERVABILITY_ICON)

            # Security & Identity Services
            with Cluster("Security & Identity Services", graph_attr={"margin": "10", "bgcolor": "lightyellow"}):
                with Cluster("cert-manager-operator", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                    cert_manager = Custom("\ncert-manager for\nRed Hat OpenShift", CERT_MANAGER_ICON)

                with Cluster("kuadrant-system", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                    authorino = Custom("\nAuthorino\nOperator", AUTHORINO_ICON)
                    limitador = Custom("\nLimitador\nOperator", LIMITADOR_ICON)
                    dns = Custom("\nDNS\nOperator", DNS_ICON)
                    connectivity_link = Custom("\nRed Hat\nConnectivity Link\nOperator", RHCL_ICON)

                with Cluster("openshift-operators", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                    ossm = Custom("\nOpenShift\nService Mesh", OSSM_ICON)

            # Developer Services
            with Cluster("Developer Services", graph_attr={"margin": "10", "bgcolor": "lightyellow"}):
                with Cluster("openshift-builds", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                    builds = Custom("\nBuilds for\nRed Hat OpenShift", BUILDS_ICON)

                with Cluster("openshift-pipelines", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                    pipelines = Custom("\nOpenShift\nPipelines Operator", PIPELINES_ICON)

                with Cluster("openshift-gitops-operator", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                    gitops = Custom("\nOpenShift\nGitOps Operator", GITOPS_ICON)

            # Storage Services
            with Cluster("Storage Services", graph_attr={"margin": "10", "bgcolor": "lightyellow"}):
                with Cluster("openshift-storage", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                    odf = Custom("\nOpenShift Data\nFoundation\nOperator", ODF_ICON)

        # RHOAI Platform (runs on OCP)
        with Cluster("Red Hat OpenShift AI Platform", graph_attr={"margin": "15", "bgcolor": "lightblue"}):
            with Cluster("redhat-ods-applications", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                rhoai_platform = Custom("\nRed Hat\nOpenShift AI", RHOAI_ICON)

            with Cluster("redhat-ods-monitoring", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                rhoai_monitoring = Custom("\nRHOAI\nMonitoring", CLUSTER_OBSERVABILITY_ICON)

            with Cluster("ai-project-A", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                ai_workload_a = Custom("\nAI workload", AI_MODEL_ICON)

            with Cluster("ai-project-B", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                ai_workload_b = Custom("\nAI workload", AI_MODEL_ICON)

            # All 4 namespaces in the same horizontal row
            rhoai_platform - Edge(style="invis") - rhoai_monitoring - Edge(style="invis") - ai_workload_a - Edge(style="invis") - ai_workload_b

    # Force 3-row layout
    # Row 1: Compute & Acceleration, Observability
    # Row 2: Security & Identity Services, Developer Services, Storage Services
    # Row 3: RHOAI Platform

    # Force Row 2 below Row 1 - distributed anchor points across full width
    gpu_operator >> Edge(style="invis") >> cert_manager
    nfd >> Edge(style="invis") >> authorino
    kueue >> Edge(style="invis") >> builds
    lws >> Edge(style="invis") >> pipelines
    cluster_monitoring >> Edge(style="invis") >> gitops
    udwm >> Edge(style="invis") >> odf
    grafana >> Edge(style="invis") >> ossm
    netobserv >> Edge(style="invis") >> connectivity_link

    # Force Row 3 (RHOAI) below Row 2 - single anchor to preserve horizontal alignment
    cert_manager >> Edge(style="invis") >> rhoai_platform

print("✓ Generated: output/rhoai-ocp-integration.png")
print("  → OCP Platform contains OCP Platform Services + RHOAI")
print("  → RHOAI namespaces: redhat-ods-applications + redhat-ods-monitoring + ai-project-A + ai-project-B")
print("  → 5 service categories: Compute, Observability, Security & Identity Services, Developer, Storage Services")
