# Diagram Examples

This document provides examples and patterns for creating OpenShift architecture diagrams.

## Table of Contents

1. [Basic Patterns](#basic-patterns)
2. [Advanced Techniques](#advanced-techniques)
3. [OpenShift Specific Examples](#openshift-specific-examples)
4. [Styling Guide](#styling-guide)

## Basic Patterns

### Simple Node Connection

```python
from diagrams import Diagram
from diagrams.k8s.compute import Pod
from diagrams.k8s.network import Service

with Diagram("Simple Connection", show=False):
    pod = Pod("Application")
    svc = Service("Service")
    
    svc >> pod
```

### Multiple Connections

```python
from diagrams import Diagram, Edge
from diagrams.k8s.compute import Pod
from diagrams.k8s.network import Service

with Diagram("Fan Out", show=False):
    svc = Service("Load Balancer")
    pods = [Pod(f"Pod {i}") for i in range(3)]
    
    svc >> pods  # One-to-many
```

### Bidirectional Flow

```python
from diagrams import Diagram, Edge
from diagrams.k8s.compute import Pod
from diagrams.onprem.database import PostgreSQL

with Diagram("Bidirectional", show=False):
    app = Pod("Application")
    db = PostgreSQL("Database")
    
    app >> Edge(label="query") >> db
    app << Edge(label="result") << db
    
    # Or use bidirectional edge
    app - Edge(color="black") - db
```

## Advanced Techniques

### Conditional/Optional Connections

```python
from diagrams import Diagram, Edge, Cluster
from diagrams.k8s.compute import Pod

with Diagram("Optional Connection", show=False):
    with Cluster("Primary"):
        primary = Pod("Primary")
    
    with Cluster("Secondary (Optional)"):
        secondary = Pod("Secondary")
    
    primary >> Edge(style="dashed", label="optional replication") >> secondary
```

### Denied/Blocked Traffic

```python
from diagrams import Diagram, Edge
from diagrams.k8s.compute import Pod
from diagrams.k8s.network import NetworkPolicy

with Diagram("Blocked Traffic", show=False):
    frontend = Pod("Frontend")
    database = Pod("Database")
    policy = NetworkPolicy("Deny Policy")
    
    frontend >> Edge(color="red", style="dashed", label="DENIED") >> database
```

### Grouping with Clusters

```python
from diagrams import Diagram, Cluster
from diagrams.k8s.compute import Pod, Deployment

with Diagram("Nested Clusters", show=False):
    with Cluster("Cluster"):
        with Cluster("Namespace: production"):
            with Cluster("Deployment"):
                deploy = Deployment("App")
                pods = [Pod(f"Pod {i}") for i in range(3)]
                deploy >> pods
```

## OpenShift Specific Examples

### Project Isolation

```python
from diagrams import Diagram, Cluster
from diagrams.k8s.compute import Pod
from diagrams.k8s.network import Service, NetworkPolicy

with Diagram("OpenShift Project Isolation", show=False):
    with Cluster("Project: team-a"):
        netpol_a = NetworkPolicy("Deny All Ingress")
        svc_a = Service("Team A Service")
        pod_a = Pod("Team A Pod")
        netpol_a >> pod_a
        svc_a >> pod_a
    
    with Cluster("Project: team-b"):
        netpol_b = NetworkPolicy("Deny All Ingress")
        svc_b = Service("Team B Service")
        pod_b = Pod("Team B Pod")
        netpol_b >> pod_b
        svc_b >> pod_b
```

### Route vs Ingress

```python
from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.network import Ingress, Service
from diagrams.k8s.compute import Pod
from diagrams.onprem.client import Users

with Diagram("OpenShift Routes", show=False):
    users = Users("External Users")
    
    with Cluster("OpenShift"):
        router = Ingress("OpenShift Router\n(Route)")
        svc = Service("Service")
        pods = [Pod("Pod") for _ in range(2)]
        
        router >> svc >> pods
    
    users >> Edge(label="HTTPS://app.example.com") >> router
```

### ImageStream Workflow

```python
from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.vcs import Github
from diagrams.k8s.compute import Pod, Deployment
from diagrams.onprem.registry import Harbor

with Diagram("ImageStream Workflow", show=False, direction="LR"):
    github = Github("Source Code")
    
    with Cluster("OpenShift"):
        with Cluster("Build"):
            build = Pod("BuildConfig")
            imagestream = Harbor("ImageStream")
        
        with Cluster("Deploy"):
            deployment = Deployment("DeploymentConfig")
            pods = [Pod("Pod") for _ in range(2)]
    
    github >> Edge(label="webhook") >> build
    build >> Edge(label="push") >> imagestream
    imagestream >> Edge(label="trigger") >> deployment
    deployment >> pods
```

## Styling Guide

### Edge Styles

```python
from diagrams import Diagram, Edge
from diagrams.k8s.compute import Pod

with Diagram("Edge Styles", show=False):
    a = Pod("A")
    b = Pod("B")
    c = Pod("C")
    d = Pod("D")
    
    a >> Edge(style="solid") >> b      # Default
    a >> Edge(style="dashed") >> c     # Optional/conditional
    a >> Edge(style="dotted") >> d     # Async/background
    a >> Edge(style="bold") >> b       # Primary flow
```

### Edge Colors

```python
from diagrams import Diagram, Edge
from diagrams.k8s.compute import Pod

with Diagram("Edge Colors", show=False):
    src = Pod("Source")
    allowed = Pod("Allowed")
    denied = Pod("Denied")
    data = Pod("Data Flow")
    
    src >> Edge(color="green") >> allowed     # Success/allowed
    src >> Edge(color="red") >> denied        # Error/denied
    src >> Edge(color="blue") >> data         # Data flow
```

### Graph Attributes

```python
from diagrams import Diagram

graph_attr = {
    "fontsize": "16",           # Font size for text
    "bgcolor": "white",         # Background color
    "pad": "0.5",              # Padding around diagram
    "splines": "spline",       # Curved lines (vs polyline/ortho)
    "nodesep": "1.0",          # Horizontal node spacing
    "ranksep": "1.0",          # Vertical rank spacing
    "concentrate": "true",      # Merge edges when possible
}

with Diagram("Custom Styling", show=False, graph_attr=graph_attr):
    # Your diagram here
    pass
```

### Node Labels

```python
from diagrams import Diagram
from diagrams.k8s.compute import Pod

with Diagram("Node Labels", show=False):
    # Multiline labels using \n
    pod1 = Pod("Pod Name\nAdditional Info")
    
    # Long labels
    pod2 = Pod("Very Long Pod Name\nWith Multiple Lines\nOf Information")
```

## Tips and Tricks

### 1. Managing Complexity

For complex diagrams, break into functions:

```python
def create_control_plane():
    with Cluster("Control Plane"):
        api = APIServer("API")
        scheduler = Scheduler("Scheduler")
        return api, scheduler

def create_worker_nodes(count=3):
    pods = []
    for i in range(count):
        with Cluster(f"Worker {i+1}"):
            pod = Pod(f"Pod {i+1}")
            pods.append(pod)
    return pods

with Diagram("Modular Design", show=False):
    api, scheduler = create_control_plane()
    workers = create_worker_nodes(3)
    
    api >> scheduler >> workers
```

### 2. Reusing Patterns

Create a `common/` directory with reusable patterns:

```python
# common/patterns.py
from diagrams import Cluster
from diagrams.k8s.controlplane import APIServer, Scheduler

def ha_control_plane(name="Control Plane"):
    with Cluster(name):
        apis = [APIServer(f"API {i}") for i in range(3)]
        schedulers = [Scheduler(f"Scheduler {i}") for i in range(3)]
    return apis, schedulers
```

### 3. Testing Layouts

Try different directions to see what works best:

```python
# Horizontal
with Diagram("Horizontal", direction="LR", show=False):
    pass

# Vertical  
with Diagram("Vertical", direction="TB", show=False):
    pass
```

### 4. Output Formats

Generate multiple formats:

```python
from diagrams import Diagram

# PNG (default)
with Diagram("My Diagram", show=False, filename="output/diagram"):
    pass

# To generate SVG or PDF, change the extension manually
# or use outformat parameter (requires graphviz configuration)
```

## Resources

- [Diagrams Official Documentation](https://diagrams.mingrammer.com/)
- [Graphviz Attributes](https://graphviz.org/doc/info/attrs.html)
- [OpenShift Documentation](https://docs.openshift.com/)
