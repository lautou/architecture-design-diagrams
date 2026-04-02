"""
OpenShift Data Foundation (ODF) Architecture

Demonstrates Red Hat OpenShift Data Foundation with:
- Ceph storage cluster
- Storage classes (Block, File, Object)
- Multi-Cloud Gateway
- Persistent volume provisioning
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.storage import PV, PVC, StorageClass
from diagrams.k8s.compute import Pod
from diagrams.onprem.storage import Ceph
from diagrams.onprem.network import Internet

graph_attr = {
    "fontsize": "16",
    "bgcolor": "white",
    "pad": "0.5"
}

with Diagram(
    "OpenShift Data Foundation (ODF) Architecture",
    show=False,
    direction="TB",
    filename="output/odf-architecture",
    graph_attr=graph_attr
):

    with Cluster("OpenShift Cluster"):

        with Cluster("Applications"):
            with Cluster("StatefulSet App"):
                app_pod = Pod("App Pod")
                app_pvc = PVC("Block PVC")
                app_pod >> app_pvc

            with Cluster("Shared Storage App"):
                shared_pods = [Pod(f"Pod {i}") for i in range(2)]
                shared_pvc = PVC("RWX File PVC")
                shared_pods >> shared_pvc

        with Cluster("ODF Storage Classes"):
            sc_block = StorageClass("ocs-storagecluster-ceph-rbd\n(Block/RWO)")
            sc_file = StorageClass("ocs-storagecluster-cephfs\n(File/RWX)")
            sc_object = StorageClass("ocs-storagecluster-ceph-rgw\n(Object/S3)")

        with Cluster("ODF Control Plane"):
            with Cluster("Operators"):
                odf_operator = Pod("ODF Operator")
                ceph_operator = Pod("Rook-Ceph Operator")
                noobaa_operator = Pod("NooBaa Operator")

        with Cluster("Ceph Storage Cluster"):
            with Cluster("MON Nodes"):
                mon = [Ceph(f"MON {i}") for i in range(3)]

            with Cluster("OSD Nodes"):
                osd = [Ceph(f"OSD {i}") for i in range(3)]

            with Cluster("MDS (CephFS)"):
                mds = [Ceph(f"MDS {i}") for i in range(2)]

            with Cluster("RGW (Object)"):
                rgw = [Ceph(f"RGW {i}") for i in range(2)]

        with Cluster("Multi-Cloud Gateway (MCG/NooBaa)"):
            mcg = Pod("NooBaa Core")
            s3_endpoint = Pod("S3 Endpoint")

    with Cluster("External Cloud Storage"):
        aws_s3 = Internet("AWS S3")
        azure_blob = Internet("Azure Blob")

    # Storage provisioning flow
    app_pvc >> sc_block >> Edge(label="provision") >> osd[0]
    shared_pvc >> sc_file >> Edge(label="provision") >> mds[0]

    # Operators manage storage
    odf_operator >> [ceph_operator, noobaa_operator]
    ceph_operator >> mon[0]
    ceph_operator >> osd[0]
    ceph_operator >> mds[0]
    ceph_operator >> rgw[0]
    noobaa_operator >> Edge(label="manage") >> mcg

    # Object storage
    sc_object >> rgw[0]
    mcg >> s3_endpoint

    # Multi-cloud gateway to external storage
    mcg >> Edge(label="tier/backup", style="dashed") >> aws_s3
    mcg >> Edge(label="tier/backup", style="dashed") >> azure_blob

    # MON manages cluster
    mon[0] >> Edge(label="orchestrate") >> osd[0]
    mon[0] >> Edge(label="orchestrate") >> mds[0]
    mon[0] >> Edge(label="orchestrate") >> rgw[0]

print("✓ Generated: output/odf-architecture.png")
