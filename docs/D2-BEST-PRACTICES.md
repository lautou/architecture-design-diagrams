# D2 Diagram Best Practices

**Document created:** 2026-04-13  
**Purpose:** Preserve best practices learned while creating AI Generation LLM RAG architecture diagram

---

## Layout Management

### Container Direction and Spacing

D2 has opinionated layout algorithms. Use these attributes to control layout:

```d2
container: {
  label: Container Name
  direction: down      # down = vertical, right = horizontal
  grid-gap: 10         # spacing between elements (5-30px typical)
}
```

**Common patterns:**
- **Horizontal lists** (legends, similar services): `direction: right`, `grid-gap: 20-30`
- **Vertical stacks** (pipeline steps, service lists): `direction: down`, `grid-gap: 10-15`
- **Compact containers** (logos, small groups): `grid-gap: 5`, smaller dimensions

### Forcing Layout with Invisible Edges

When `direction` attribute doesn't work, **force layout** with invisible connections:

```d2
container: {
  direction: down
  
  component-1: {...}
  component-2: {...}
  component-3: {...}
  
  # Force vertical stacking
  component-1 -> component-2: {style.opacity: 0}
  component-2 -> component-3: {style.opacity: 0}
}
```

**Why this works:** D2's layout engine respects edge connections. Invisible edges (`opacity: 0`) create layout constraints without visible lines.

**Use cases:**
- AI Pipeline server components (forced vertical layout for 6 components)
- Model servers (forced horizontal layout initially, then vertical)

### Icon Positioning in Containers

**Challenge:** D2 doesn't support precise icon positioning (e.g., "top-right corner")

**Solutions:**
1. **Element order matters** - First element often appears at top/left:
   ```d2
   container: {
     logo: {icon: "...", style.stroke: "transparent"}  # First = top
     main-content: {...}
   }
   ```

2. **Size control** - Make logos smaller to act as visual legends:
   ```d2
   logo: {
     icon: "../path/to/icon.svg"
     style.stroke: "transparent"
     width: 40
     height: 40
   }
   ```

3. **Direction control** - Use `direction` to control icon placement relative to other elements

**Best practice for logos:** Small, borderless icons (`style.stroke: "transparent"`) at 40x40 or 50x50, placed as first element

---

## Data Flow Conventions

### Push vs Pull Connectors

**Visual convention:**
- **Solid line** = Push (source actively sends to destination)
- **Dotted line** = Pull (destination retrieves from source)

```d2
# Push (solid)
source -> destination

# Pull (dotted)
source -> destination: {
  style.stroke-dash: 5
}
```

**Create a legend:**
```d2
legend: {
  label: "Data Flow Convention"
  direction: right
  grid-gap: 30

  push: {
    source: {label: "source"}
    destination: {label: "destination"}
    source -> destination
  }

  pull: {
    source: {label: "source"}
    destination: {label: "destination"}
    source -> destination: {style.stroke-dash: 5}
  }
}
```

---

## Icon Management

### Importing External Icons

**From Downloads:**
```bash
cp ~/Downloads/icon.png custom_icons/icon-name.png
```

**From URLs:**
```bash
curl -s "https://url/to/icon.svg" -o custom_icons/icon-name.svg
```

**Best practices:**
- Use descriptive names: `kserve-icon.svg`, `boto3-icon.png`, `huggingface-icon.png`
- Avoid spaces in paths (D2 can't read `custom_icons/UI icons/file.png`)
- Copy to flat structure: `custom_icons/icon-name.ext`
- Prefer SVG for logos, PNG for library icons

### Icon Paths in D2

**Always use relative paths from diagram location:**
```d2
icon: ../../../custom_icons/icon-name.svg
```

**Avoid:**
- Absolute paths (not portable)
- Paths with spaces (D2 bundler fails)

---

## Compact Layout Strategies

### Reducing Wasted Space

**Problem:** Large containers with few elements create wasted space

**Solutions:**

1. **Reduce grid-gap:**
   ```d2
   container: {
     grid-gap: 5    # Tighter spacing
   }
   ```

2. **Change direction:**
   ```d2
   # Before: horizontal spread
   container: {direction: right}
   
   # After: vertical stack (more compact)
   container: {direction: down}
   ```

3. **Force layout with invisible edges** (see above)

4. **Remove unnecessary containers** - Flatten structure when possible

**Example transformation:**
```d2
# BEFORE: Horizontal spread (wastes space)
ai-pipeline-server: {
  direction: right  # Default, spreads 6 components horizontally
  component-1: {...}
  component-2: {...}
  # ... 6 components total
}

# AFTER: Vertical stack (compact)
ai-pipeline-server: {
  direction: down
  grid-gap: 10
  component-1: {...}
  component-2: {...}
  # Force with invisible edges if needed
  component-1 -> component-2: {style.opacity: 0}
  # ...
}
```

---

## Nested Containers

### Multi-Level Architecture

**Pattern for platform → namespace → services:**
```d2
Red Hat OpenShift AI: {
  label: Red Hat OpenShift AI
  direction: down
  
  ai-project-namespace-x: {
    label: AI project namespace X
    direction: down
    
    service-1: {...}
    service-2: {...}
  }
}
```

**Container references in connections:**
```d2
# Use full path for nested elements
External.source -> Red Hat OpenShift AI.ai-project-namespace-x.service.component
```

---

## Technology Stack Representation

### System-impl Pattern (Kubeflow Pipelines)

**Pattern:** Each task has `system-driver` (Kubeflow) + `system-impl` (technology)

```d2
task-name: {
  label: task-name
  
  system-driver: {
    label: system-driver
    shape: rectangle
    icon: ../../../custom_icons/kubeflow-icon.png
  }
  
  system-impl: {
    label: system-impl
    shape: rectangle
    icon: ../../../custom_icons/technology-icon.png
  }
}
```

**Multiple technologies in one impl:**
```d2
system-impl: {
  label: system-impl
  
  boto3: {icon: ../../../custom_icons/boto3-icon.png}
  requests: {icon: ../../../custom_icons/requests-icon.png}
}
```

---

## Verification Workflow

**Always verify diagram after generation:**

```bash
# 1. Generate
d2 diagram.d2 output.png

# 2. Read with Claude Code to verify
Read output.png

# 3. Iterate until satisfied

# 4. Open once for final check
xdg-open output.png
```

**What to check:**
- ✅ No wasted space in containers
- ✅ Icons positioned correctly (logos at top, etc.)
- ✅ Data flow connectors visible (solid/dotted)
- ✅ Layout balanced (not one section dominating)
- ✅ All external services positioned around platform
- ✅ Text labels readable

---

## Common Pitfalls

### ❌ Don't Do This

1. **Paths with spaces:**
   ```d2
   icon: ../../../custom_icons/UI icons/file.png  # FAILS
   ```

2. **Assuming vertical layout works for all containers:**
   - Some containers (like Storage service) create massive vertical waste with `direction: down`
   - D2's layout engine may ignore height constraints and grid-gap settings
   - **Solution:** Try horizontal layout (`direction: right`) instead
   - Example: Storage service with 3 items was extremely tall vertically, became compact horizontally

2. **Relying only on `direction` without checking:**
   - D2 may ignore `direction` attribute
   - Always verify PNG output
   - Use invisible edges to force layout

3. **Forgetting to set container direction:**
   ```d2
   container: {
     # Missing direction - D2 chooses layout
     component-1: {...}
     component-2: {...}
   }
   ```

4. **Large logos/icons:**
   ```d2
   logo: {icon: "..."}  # Default size too large
   ```
   Use `width: 40, height: 40` for logos

5. **Not checking PNG output:**
   - Layout may differ from expectations
   - Always read and verify

---

## Architecture Diagram Structure

### Recommended Layout Pattern

**For platform + external services:**

```
┌─────────────────────────────────────────┐
│  External Services (top/sides)          │
│  ┌────────────────────────────┐        │
│  │ Platform Container         │        │
│  │  ┌──────────────────┐     │        │
│  │  │ Namespace        │     │        │
│  │  │  - Services      │     │        │
│  │  │  - Components    │     │        │
│  │  └──────────────────┘     │        │
│  └────────────────────────────┘        │
│  External Services (bottom)             │
│  Legend (bottom corner)                 │
└─────────────────────────────────────────┘
```

**Positioning:**
- **Platform:** Center (Red Hat OpenShift AI)
- **External services:** Surrounding (Storage, Databases, HF repos)
- **Legend:** Bottom-right or bottom-left corner
- **Data flows:** Dotted lines from external → platform (pull)

---

## File Organization

### Custom Icons Structure

```
custom_icons/
├── boto3-icon.png
├── requests-icon.png
├── python-icon.png
├── psycopg-icon.png
├── kserve-icon.svg
├── vllm-icon.png
├── huggingface-icon.png
├── docling.jpeg
├── kubeflow-icon.png
├── mariadb-icon.png
├── postgresql-icon.png
├── http-server-icon.png
└── Icons/
    ├── Bucket/
    │   └── Icon-Red_Hat-Bucket-A-Red-RGB.Large_icon_transparent.png
    └── ...
```

**Best practice:** Flatten when possible, avoid nested directories with spaces

---

## Performance Tips

### D2 Compilation

**Typical compile time:** 15-25 seconds for complex diagrams

**To speed up:**
- Reduce total number of nodes
- Minimize invisible edges (only use when necessary)
- Use simpler layouts when possible

---

## Summary Checklist

When creating D2 architecture diagrams:

- [ ] Use `direction` and `grid-gap` for layout control
- [ ] Force stubborn layouts with invisible edges (`style.opacity: 0`)
- [ ] Import icons to flat `custom_icons/` structure (no spaces)
- [ ] Use relative paths for icons
- [ ] Create data flow legend (solid = push, dotted = pull)
- [ ] Position logos as small borderless icons (40x40, first element)
- [ ] **Always read PNG output to verify layout**
- [ ] Iterate until space is efficiently used
- [ ] Open once with xdg-open for final check
- [ ] Document any new patterns learned

---

**End of Best Practices**
