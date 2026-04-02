# Red Hat OpenShift Architecture Diagrams

A comprehensive repository of OpenShift and RHOAI (Red Hat OpenShift AI) architecture diagrams using diagram-as-code principles.

## Overview

This repository uses [Diagrams](https://diagrams.mingrammer.com/) - a Python library for creating cloud system architecture diagrams programmatically.

## Prerequisites

- Python 3.8+
- Graphviz

### Install Graphviz

**Fedora/RHEL:**
```bash
sudo dnf install graphviz
```

**Ubuntu/Debian:**
```bash
sudo apt-get install graphviz
```

**macOS:**
```bash
brew install graphviz
```

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd add
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Generate a diagram by running the Python script:

```bash
python diagrams/openshift/basic-cluster.py
```

Diagrams will be generated in the `output/` directory.

## Repository Structure

```
.
├── diagrams/
│   ├── openshift/          # Core OpenShift architecture diagrams
│   ├── rhoai/              # RHOAI-specific diagrams
│   ├── networking/         # Network architecture diagrams
│   ├── storage/            # Storage architecture diagrams
│   ├── security/           # Security architecture diagrams
│   └── integrations/       # Integration patterns
├── custom_icons/           # Custom Red Hat/OpenShift icons
├── output/                 # Generated diagram outputs (gitignored)
├── docs/                   # Documentation and examples
└── templates/              # Reusable diagram templates
```

## Creating Diagrams

### Example: Basic OpenShift Cluster

```python
from diagrams import Diagram, Cluster
from diagrams.k8s.controlplane import APIServer, Scheduler
from diagrams.k8s.compute import Pod

with Diagram("OpenShift Basic Cluster", show=False, direction="TB"):
    with Cluster("Control Plane"):
        api = APIServer("API Server")
        scheduler = Scheduler("Scheduler")
    
    with Cluster("Worker Nodes"):
        pods = [Pod("Pod") for _ in range(3)]
    
    api >> scheduler >> pods
```

## Diagram Categories

- **OpenShift Core**: Basic cluster, multi-cluster, control plane architecture
- **RHOAI**: ML/AI workflow, model serving, data science pipelines
- **Networking**: SDN, ingress/egress, service mesh
- **Storage**: PV/PVC, OCS, external storage integration
- **Security**: RBAC, network policies, compliance
- **Integrations**: CI/CD, monitoring, logging

## Contributing

1. Create diagrams in the appropriate category folder
2. Use descriptive filenames (kebab-case)
3. Add comments explaining complex architecture decisions
4. Generate output and verify before committing
5. Update this README if adding new categories

## Best Practices

- Keep diagrams focused on a single concept
- Use clusters to group related components
- Add labels for clarity
- Maintain consistent naming conventions
- Document non-obvious design decisions in comments

## License

[Specify your license]

## References

- [Diagrams Documentation](https://diagrams.mingrammer.com/)
- [OpenShift Documentation](https://docs.openshift.com/)
- [RHOAI Documentation](https://access.redhat.com/documentation/en-us/red_hat_openshift_ai/)
