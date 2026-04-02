# Quick Start Guide

Get up and running with OpenShift Architecture Diagrams in 5 minutes.

## Prerequisites

- **Python 3.8+** installed
- **Graphviz** installed (see below)
- **Git** (optional, for version control)

## Installation Steps

### 1. Install Graphviz

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

### 2. Clone or Download This Repository

```bash
# If using git
git clone <repository-url>
cd add

# Or extract the downloaded archive
unzip openshift-diagrams.zip
cd openshift-diagrams
```

### 3. Run Automated Setup

```bash
./setup.sh
```

This script will:
- Check Python and Graphviz installation
- Create a virtual environment
- Install Python dependencies
- Generate a test diagram

### 4. Activate Virtual Environment

```bash
source venv/bin/activate
```

## Generate Your First Diagram

### Option 1: Generate All Diagrams

```bash
make generate-all
```

### Option 2: Generate a Single Diagram

```bash
python3 diagrams/openshift/basic-cluster.py
```

### Option 3: Create Your Own

```bash
# Copy the template
cp templates/diagram_template.py diagrams/openshift/my-cluster.py

# Edit it
vim diagrams/openshift/my-cluster.py

# Generate it
python3 diagrams/openshift/my-cluster.py
```

## View Generated Diagrams

All diagrams are saved in the `output/` directory:

```bash
ls -lh output/
```

Open them with your image viewer:

```bash
# Linux
xdg-open output/openshift-basic-cluster.png

# macOS
open output/openshift-basic-cluster.png

# Windows
start output/openshift-basic-cluster.png
```

## Available Example Diagrams

After running `make generate-all`, you'll have these diagrams:

1. **openshift-basic-cluster.png** - Basic OpenShift cluster architecture
2. **openshift-multicluster-hub-spoke.png** - Multi-cluster with ACM
3. **rhoai-ml-workflow.png** - RHOAI ML/AI workflow
4. **openshift-sdn-architecture.png** - OVN-Kubernetes networking
5. **odf-architecture.png** - OpenShift Data Foundation storage
6. **cicd-pipeline.png** - CI/CD with Pipelines and GitOps

## Project Structure

```
.
├── diagrams/              # Diagram source files (.py)
│   ├── openshift/         # OpenShift core diagrams
│   ├── rhoai/             # RHOAI diagrams
│   ├── networking/        # Network diagrams
│   ├── storage/           # Storage diagrams
│   ├── security/          # Security diagrams (add your own)
│   └── integrations/      # Integration patterns
├── output/                # Generated images (.png)
├── templates/             # Diagram templates
├── custom_icons/          # Custom Red Hat icons
├── docs/                  # Documentation
├── setup.sh               # Automated setup script
├── Makefile               # Build automation
└── requirements.txt       # Python dependencies
```

## Next Steps

1. **Explore Examples**: Review the example diagrams in `diagrams/` directory
2. **Read Documentation**: 
   - `README.md` - Main documentation
   - `CONTRIBUTING.md` - Contribution guidelines
   - `docs/EXAMPLES.md` - Detailed examples and patterns
3. **Create Your Diagrams**: Use templates and examples as a starting point
4. **Share**: Commit your diagrams to git for collaboration

## Common Commands

```bash
# Generate all diagrams
make generate-all

# Clean generated files
make clean

# Create new diagram from template
cp templates/diagram_template.py diagrams/<category>/<name>.py

# Deactivate virtual environment
deactivate
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'diagrams'"
- Make sure virtual environment is activated: `source venv/bin/activate`
- Or reinstall dependencies: `pip install -r requirements.txt`

### "graphviz executables not found"
- Install Graphviz system package (see step 1)
- Verify installation: `which dot` (should return a path)

### "Permission denied: ./setup.sh"
- Make script executable: `chmod +x setup.sh`

### Diagrams look wrong or overlapping
- Try different `direction` parameter: `TB`, `LR`, `BT`, `RL`
- Adjust `graph_attr` spacing: `nodesep` and `ranksep`
- See `docs/EXAMPLES.md` for styling tips

## Getting Help

- Check `docs/EXAMPLES.md` for detailed examples
- Review existing diagrams for patterns
- Visit [Diagrams Documentation](https://diagrams.mingrammer.com/)
- Open an issue in the repository

## License

[Your License Here]
