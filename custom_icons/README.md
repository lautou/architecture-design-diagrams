# Custom Icons for Red Hat OpenShift

This directory contains custom icons for Red Hat and OpenShift-specific components not included in the default Diagrams library.

## Adding Custom Icons

1. **Download icon files** (PNG format recommended, 256x256px optimal)
   - Red Hat Product icons: [Red Hat brand assets](https://www.redhat.com/en/about/brand/standards/icons)
   - OpenShift icons: Can be extracted from OpenShift documentation or console

2. **Place icons in this directory**
   ```
   custom_icons/
   ├── openshift-logo.png
   ├── rhoai-logo.png
   ├── acm-icon.png
   └── quay-icon.png
   ```

3. **Use in diagrams**
   ```python
   from diagrams.custom import Custom
   
   custom_component = Custom("RHOAI", "./custom_icons/rhoai-logo.png")
   ```

## Recommended Icon Sources

- **OpenShift Console**: Inspect element and download SVG/PNG icons
- **Red Hat Brand**: https://www.redhat.com/en/about/brand/standards
- **PatternFly Icons**: https://www.patternfly.org/v4/guidelines/icons/
- **Kubernetes Icons**: Built into Diagrams library

## Icon Guidelines

- **Format**: PNG or SVG (PNG preferred for consistency)
- **Size**: 256x256 pixels (will be auto-scaled)
- **Background**: Transparent background recommended
- **Naming**: Use kebab-case (e.g., `red-hat-logo.png`)

## Example Usage

```python
from diagrams import Diagram, Cluster
from diagrams.custom import Custom
from diagrams.k8s.compute import Pod

with Diagram("Custom Icon Example", show=False):
    rhoai = Custom("RHOAI Platform", "./custom_icons/rhoai-logo.png")
    pod = Pod("ML Workload")
    
    rhoai >> pod
```

## Available Custom Icons

Once you add icons, list them here:

- [ ] OpenShift Container Platform logo
- [ ] RHOAI logo
- [ ] Advanced Cluster Management (ACM)
- [ ] Red Hat Quay
- [ ] Red Hat Service Mesh
- [ ] OpenShift Data Foundation
- [ ] Red Hat Build of OpenJDK
- [ ] Red Hat Integration
