"""
RHOAI on OCP - Integration Architecture

Shows RHOAI platform running on OpenShift Container Platform with OCP services.

Structure:
- OpenShift Container Platform (outer cluster)
  - OCP Platform Services (6 categories):
    - Compute And Acceleration Services: NVIDIA GPU Operator, NFD, Kueue, Leader Worker Set
    - Observability Services: Cluster Monitoring, UDWM, Grafana, Cluster Observability, Logging, Loki, OpenTelemetry, Tempo, Network Observability
    - Security & Identity Services: cert-manager, Authorino, Limitador, DNS, RHCL (kuadrant-system), OpenShift Service Mesh
    - Developer Services: Builds, Pipelines, GitOps
    - Storage Services: OpenShift Data Foundation
    - Core Components (20 essential OpenShift components in 2-row grid):
      * Row 1 (10): Control Plane (API Server, Authentication, Etcd, Controller, Scheduler) + Networking (DNS, Ingress, OVN, Multus) + Console
      * Row 2 (10): Management (OLM, Insights, Marketplace) + Storage/Registry (Image Registry, Cluster Storage) + Infrastructure (Machine API, Machine Config, Tuned) + Security (Service CA, Cloud Credential)
  - Red Hat OpenShift AI Platform (runs on OCP):
    - redhat-ods-applications: RHOAI operator
    - redhat-ods-monitoring: RHOAI monitoring stack
    - rhods-notebooks: Jupyter workbench, Code Server workbench
    - ai-project-A through ai-project-H: Sample AI workloads

Core Components are simplified to show only essential dependencies for RHOAI integration.
All icons use OpenShift icon (no operator/namespace rectangles in Core Components).

Layout: 4-row layout with distributed anchor points:
- Row 1: RHOAI Platform (11 namespaces with white rounded rectangles)
- Row 2: Compute And Acceleration Services (4), Observability Services (9)
- Row 3: Security & Identity Services (6), Developer Services (3), Storage Services (1) - ordered largest to smallest
- Row 4: Core Components (20 components in 2-row grid: 10 + 10)

Technical Notes:
- Uses distributed invisible vertical edges to force row layout
- Core Components use internal vertical edges to create 2-row grid (10 items per row)
- Simplified from 50 namespaces to 20 essential components for integration diagram clarity
- SVG icons not supported (use PNG instead to avoid massive rendering)
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
OPERATOR_BLACK_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Technology icons/operator/Technology_icon-Red_Hat-operator-Black-RGB.Large_icon_transparent.png")

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
    "RHOAI on OCP Integration",
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

            # Compute And Acceleration Services
            with Cluster("Compute And Acceleration Services", graph_attr={"margin": "10", "bgcolor": "lightyellow"}):
                with Cluster("NVIDIA GPU\nOperator", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                    gpu_operator = Custom("\nNVIDIA GPU\nOperator", NVIDIA_ICON)

                with Cluster("OpenShift\nNFD", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                    nfd = Custom("\nNode Feature\nDiscovery Operator", NFD_ICON)

                with Cluster("OpenShift\nKueue\nOperator", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                    kueue = Custom("\nRed Hat Build Of\nKueue Operator", KUEUE_ICON)

                with Cluster("OpenShift\nLeader Worker Set\nOperator", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                    lws = Custom("\nRed Hat Build Of\nLeader Worker Set\nOperator", LWS_ICON)

            # Observability
            with Cluster("Observability Services", graph_attr={"margin": "10", "bgcolor": "lightyellow"}):
                with Cluster("OpenShift\nMonitoring", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                    cluster_monitoring = Custom("\nCluster Monitoring", MONITORING_ICON)

                with Cluster("OpenShift User\nWorkload\nMonitoring", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                    udwm = Custom("\nUser Defined\nWorkload Monitoring", MONITORING_ICON)

                with Cluster("Grafana\nOperator", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                    grafana = Custom("\nGrafana\nOperator", GRAFANA_ICON)

                with Cluster("OpenShift\nObservability\nOperator", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                    cluster_observability = Custom("\nCluster Observability\nOperator", CLUSTER_OBSERVABILITY_ICON)

                with Cluster("OpenShift\nLogging", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                    openshift_logging = Custom("\nOpenShift\nLogging Operator", LOGGING_ICON)

                with Cluster("OpenShift\nOperators\nRedHat", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                    loki = Custom("\nLoki\nOperator", LOKI_ICON)

                with Cluster("OpenShift\nOpenTelemetry\nOperator", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                    opentelemetry = Custom("\nRed Hat Build Of\nOpenTelemetry", OPENTELEMETRY_ICON)

                with Cluster("OpenShift\nTempo Operator", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                    tempo = Custom("\nTempo\nOperator", TEMPO_ICON)

                with Cluster("OpenShift\nNetObserv\nOperator", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                    netobserv = Custom("\nNetwork\nObservability\nOperator", NETWORK_OBSERVABILITY_ICON)

            # Security & Identity Services (moved first - largest section with 6 items)
            with Cluster("Security & Identity Services", graph_attr={"margin": "10", "bgcolor": "lightyellow"}):
                with Cluster("Cert Manager\nOperator", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                    cert_manager = Custom("\nCert Manager For\nRed Hat OpenShift", CERT_MANAGER_ICON)

                with Cluster("Kuadrant\nSystem", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                    authorino = Custom("\nAuthorino\nOperator", AUTHORINO_ICON)
                    limitador = Custom("\nLimitador\nOperator", LIMITADOR_ICON)
                    dns = Custom("\nDNS\nOperator", DNS_ICON)
                    connectivity_link = Custom("\nRed Hat\nConnectivity Link\nOperator", RHCL_ICON)

                with Cluster("OpenShift\nOperators", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                    ossm = Custom("\nOpenShift\nService Mesh", OSSM_ICON)

            # Developer Services
            with Cluster("Developer Services", graph_attr={"margin": "10", "bgcolor": "lightyellow"}):
                with Cluster("OpenShift\nBuilds", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                    builds = Custom("\nBuilds For\nRed Hat OpenShift", BUILDS_ICON)

                with Cluster("OpenShift\nPipelines", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                    pipelines = Custom("\nOpenShift\nPipelines Operator", PIPELINES_ICON)

                with Cluster("OpenShift\nGitOps\nOperator", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                    gitops = Custom("\nOpenShift\nGitOps Operator", GITOPS_ICON)

            # Storage Services
            with Cluster("Storage Services", graph_attr={"margin": "10", "bgcolor": "lightyellow"}):
                with Cluster("OpenShift\nStorage", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                    odf = Custom("\nOpenShift Data\nFoundation\nOperator", ODF_ICON)

            # Core Components (simplified - 20 essential components in 2 rows)
            with Cluster("Core Components", graph_attr={"margin": "10", "bgcolor": "lightyellow"}):
                # Row 1: Control Plane + Networking (10 items)
                api_server = Custom("\nAPI Server", OPENSHIFT_ICON)
                authentication = Custom("\nAuthentication", OPENSHIFT_ICON)
                etcd = Custom("\nEtcd", OPENSHIFT_ICON)
                controller = Custom("\nController", OPENSHIFT_ICON)
                scheduler = Custom("\nScheduler", OPENSHIFT_ICON)
                dns_core = Custom("\nDNS", OPENSHIFT_ICON)
                ingress = Custom("\nIngress", OPENSHIFT_ICON)
                ovn = Custom("\nOVN", OPENSHIFT_ICON)
                multus = Custom("\nMultus", OPENSHIFT_ICON)
                console = Custom("\nConsole", OPENSHIFT_ICON)

                # Row 2: Management + Storage + Infrastructure + Security (10 items)
                olm = Custom("\nOLM", OPENSHIFT_ICON)
                insights = Custom("\nInsights", OPENSHIFT_ICON)
                marketplace = Custom("\nMarketplace", OPENSHIFT_ICON)
                image_registry = Custom("\nImage Registry", OPENSHIFT_ICON)
                cluster_storage = Custom("\nCluster Storage", OPENSHIFT_ICON)
                machine_api = Custom("\nMachine API", OPENSHIFT_ICON)
                machine_config = Custom("\nMachine Config", OPENSHIFT_ICON)
                tuned = Custom("\nTuned", OPENSHIFT_ICON)
                service_ca = Custom("\nService CA", OPENSHIFT_ICON)
                cloud_credential = Custom("\nCloud Credential", OPENSHIFT_ICON)

                # Stack Row 2 below Row 1 using vertical edges
                api_server >> Edge(style="invis") >> olm
                authentication >> Edge(style="invis") >> insights
                etcd >> Edge(style="invis") >> marketplace
                controller >> Edge(style="invis") >> image_registry
                scheduler >> Edge(style="invis") >> cluster_storage
                dns_core >> Edge(style="invis") >> machine_api
                ingress >> Edge(style="invis") >> machine_config
                ovn >> Edge(style="invis") >> tuned
                multus >> Edge(style="invis") >> service_ca
                console >> Edge(style="invis") >> cloud_credential

        # RHOAI Platform (runs on OCP)
        with Cluster("Red Hat OpenShift AI Platform", graph_attr={"margin": "15", "bgcolor": "lightblue"}):
            with Cluster("RedHat ODS\nApplications", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                rhoai_platform = Custom("\nRed Hat\nOpenShift AI", RHOAI_ICON)

            with Cluster("RedHat ODS\nMonitoring", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                rhoai_monitoring = Custom("\nRHOAI\nMonitoring", CLUSTER_OBSERVABILITY_ICON)

            with Cluster("RHODS\nNotebooks", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                jupyter_workbench = Custom("\nJupyter\nWorkbench", JUPYTER_ICON)
                vscode_workbench = Custom("\nCode Server\nWorkbench", VSCODE_ICON)

            with Cluster("AI Project A", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                ai_workload_a = Custom("\nAI\nWorkload", AI_MODEL_ICON)

            with Cluster("AI Project B", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                ai_workload_b = Custom("\nAI\nWorkload", AI_MODEL_ICON)

            with Cluster("AI Project C", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                ai_workload_c = Custom("\nAI\nWorkload", AI_MODEL_ICON)

            with Cluster("AI Project D", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                ai_workload_d = Custom("\nAI\nWorkload", AI_MODEL_ICON)

            with Cluster("AI Project E", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                ai_workload_e = Custom("\nAI\nWorkload", AI_MODEL_ICON)

            with Cluster("AI Project F", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                ai_workload_f = Custom("\nAI\nWorkload", AI_MODEL_ICON)

            with Cluster("AI Project G", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                ai_workload_g = Custom("\nAI\nWorkload", AI_MODEL_ICON)

            with Cluster("AI Project H", graph_attr={"margin": "10", "bgcolor": "white", "style": "rounded", "labeljust": "c"}):
                ai_workload_h = Custom("\nAI\nWorkload", AI_MODEL_ICON)

    # Force 6-row layout with distributed anchor points

    # Force Row 2 (OCP Compute & Observability) below Row 1 (RHOAI)
    rhoai_platform >> Edge(style="invis") >> gpu_operator
    rhoai_monitoring >> Edge(style="invis") >> nfd
    jupyter_workbench >> Edge(style="invis") >> kueue
    vscode_workbench >> Edge(style="invis") >> lws
    ai_workload_a >> Edge(style="invis") >> cluster_monitoring
    ai_workload_b >> Edge(style="invis") >> udwm
    ai_workload_c >> Edge(style="invis") >> grafana
    ai_workload_d >> Edge(style="invis") >> cluster_observability
    ai_workload_e >> Edge(style="invis") >> openshift_logging
    ai_workload_f >> Edge(style="invis") >> loki
    ai_workload_g >> Edge(style="invis") >> opentelemetry
    ai_workload_h >> Edge(style="invis") >> tempo

    # Force Row 3 (OCP Security/Developer/Storage) below Row 2
    gpu_operator >> Edge(style="invis") >> cert_manager
    nfd >> Edge(style="invis") >> authorino
    kueue >> Edge(style="invis") >> builds
    lws >> Edge(style="invis") >> pipelines
    cluster_monitoring >> Edge(style="invis") >> gitops
    udwm >> Edge(style="invis") >> odf
    grafana >> Edge(style="invis") >> ossm
    netobserv >> Edge(style="invis") >> connectivity_link

    # Force Row 4 (Core Components) below Row 3 - distributed anchors
    cert_manager >> Edge(style="invis") >> api_server
    authorino >> Edge(style="invis") >> authentication
    limitador >> Edge(style="invis") >> etcd
    builds >> Edge(style="invis") >> controller
    pipelines >> Edge(style="invis") >> scheduler
    gitops >> Edge(style="invis") >> dns_core
    odf >> Edge(style="invis") >> ingress
    ossm >> Edge(style="invis") >> console

print("✓ Generated: output/rhoai-ocp-integration.png")
print("  → 4-row layout: RHOAI Platform (Row 1) + OCP Services (Rows 2-4)")
print("  → Row 1: RHOAI (11 namespaces) - redhat-ods-applications, redhat-ods-monitoring, rhods-notebooks, ai-project-A through ai-project-H")
print("  → Row 2: Compute & Acceleration (4), Observability (9)")
print("  → Row 3: Security & Identity (6), Developer (3), Storage (1)")
print("  → Row 4: Core Components (20 essential components in 2-row grid)")
print("  →   Row 4.1 (10): Control Plane + Networking + Console")
print("  →   Row 4.2 (10): Management + Storage + Infrastructure + Security")
