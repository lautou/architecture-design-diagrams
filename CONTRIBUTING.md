# Contributing to OpenShift Architecture Diagrams

Thank you for contributing! This guide will help you create consistent, high-quality diagrams.

## Quick Start

1. **Choose the right category** for your diagram:
   - `diagrams/openshift/` - Core OpenShift cluster architectures
   - `diagrams/rhoai/` - AI/ML workload architectures
   - `diagrams/networking/` - Network configurations
   - `diagrams/storage/` - Storage architectures
   - `diagrams/security/` - Security patterns
   - `diagrams/integrations/` - Integration patterns (CI/CD, monitoring, etc.)

2. **Copy the template**:
   ```bash
   cp templates/diagram_template.py diagrams/<category>/<your-diagram>.py
   ```

3. **Follow naming conventions**:
   - Use kebab-case for filenames: `multi-zone-deployment.py`
   - Output should match: `filename="output/multi-zone-deployment"`
   - Use descriptive names that reflect the architecture

## Diagram Standards

### File Structure

Every diagram file should include:

```python
"""
Brief title of the diagram

Multi-line description explaining:
- What this architecture demonstrates
- Key components included
- Use cases or scenarios
"""

from diagrams import Diagram, Cluster, Edge
# ... imports

# Graph configuration
graph_attr = {
    "fontsize": "16",
    "bgcolor": "white",
    "pad": "0.5"
}

with Diagram(...):
    # Diagram code
    pass

print("✓ Generated: output/your-diagram.png")
```

### Best Practices

1. **Use Clusters for logical grouping**:
   ```python
   with Cluster("Control Plane"):
       api = APIServer("API Server")
   ```

2. **Label edges for clarity**:
   ```python
   api >> Edge(label="authenticate") >> etcd
   ```

3. **Add comments for complex logic**:
   ```python
   # Cross-cluster replication requires VPN connection
   cluster1 >> Edge(style="dashed") >> cluster2
   ```

4. **Keep diagrams focused**:
   - One diagram = one concept
   - If too complex, split into multiple diagrams
   - Use hierarchical clusters to manage complexity

5. **Use consistent naming**:
   - OpenShift projects → "Project: app-name"
   - Kubernetes namespaces → "Namespace: app-name"
   - External systems → "External: system-name"

### Styling Guidelines

#### Colors (use sparingly)
```python
Edge(color="red")      # Denied/blocked traffic
Edge(color="green")    # Allowed traffic
Edge(color="blue")     # Data flow
```

#### Line Styles
```python
Edge(style="dashed")   # Optional or conditional connections
Edge(style="dotted")   # Asynchronous or background processes
Edge(style="bold")     # Primary data flow
```

#### Directions
- `TB` (Top to Bottom): Default for hierarchical architectures
- `LR` (Left to Right): Better for workflows and pipelines
- `BT` (Bottom to Top): Rarely used
- `RL` (Right to Left): Rarely used

## Testing Your Diagram

Before submitting:

1. **Generate the diagram**:
   ```bash
   ./venv/bin/python3 diagrams/<category>/<your-diagram>.py
   ```

2. **Verify output**:
   - Check `output/<your-diagram>.png` exists
   - Visual quality is acceptable
   - Labels are readable
   - Layout makes logical sense

3. **Test with make**:
   ```bash
   make generate-all
   ```

## Commit Guidelines

1. **Commit message format**:
   ```
   Add [category]: brief description
   
   - Key points about the diagram
   - Any special considerations
   ```

   Example:
   ```
   Add networking: OVN-Kubernetes SDN architecture
   
   - Shows network policy enforcement
   - Includes ingress/egress flow
   - Demonstrates pod-to-pod communication
   ```

2. **Do not commit generated images** (they're in `.gitignore`)

3. **One diagram per commit** (unless related)

## Code Review Checklist

Before submitting a PR, ensure:

- [ ] Diagram generates without errors
- [ ] Follows file naming conventions
- [ ] Includes docstring with description
- [ ] Uses appropriate category folder
- [ ] Clusters are logically organized
- [ ] Edge labels are clear and concise
- [ ] No hardcoded absolute paths
- [ ] Print statement shows output location
- [ ] Follows styling guidelines

## Getting Help

- Check existing diagrams for examples
- Review the [Diagrams documentation](https://diagrams.mingrammer.com/)
- Open an issue for questions

## Advanced Topics

### Custom Icons

See `custom_icons/README.md` for adding Red Hat-specific icons.

### Reusable Components

For frequently used patterns, create helper functions:

```python
def create_ha_control_plane():
    """Returns a high-availability control plane cluster"""
    with Cluster("HA Control Plane"):
        masters = [Master(f"Master {i}") for i in range(3)]
        etcd_cluster = [Etcd(f"etcd {i}") for i in range(3)]
    return masters, etcd_cluster
```

### Complex Layouts

For complex diagrams, use `graph_attr` and `edge_attr`:

```python
graph_attr = {
    "splines": "spline",     # Curved lines
    "nodesep": "1.0",        # Horizontal spacing
    "ranksep": "1.0",        # Vertical spacing
    "fontsize": "14",
}
```

## Questions?

Open an issue or reach out to the maintainers.
