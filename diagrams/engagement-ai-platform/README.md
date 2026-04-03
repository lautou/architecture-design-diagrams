# AI Platform Engagement Diagrams

This directory contains **customer-specific** architecture diagrams for AI platform engagements. These diagrams compose and adapt the baseline reference diagrams for actual customer deployments.

## Structure

```
engagement-ai-platform/
├── 00-overview/              # High-level landscape and topology
├── 01-production/            # Production environment
├── 02-preproduction/         # Pre-production (QA/Test shared)
├── 03-sandbox/               # Sandbox development environment
└── common/                   # Shared services across environments
```

## Diagram Categories

### 00 - Overview

#### Environment Landscape
**File:** `00-overview/environment-landscape.py`
**Purpose:** Shows the relationship between all environments
**Includes:**
- Production, Pre-production, Sandbox clusters
- Shared services (GitOps, Registry, Monitoring, IDP)
- User access patterns
- Image promotion flow
- Environment isolation boundaries

**Customize:** Number of environments, isolation strategy, shared services approach

#### Cluster Topology
**File:** `00-overview/cluster-topology.py`
**Purpose:** Shows cluster distribution strategy and rationale
**Includes:**
- Cluster sizing per environment
- HA configurations (control plane, workers)
- Network isolation patterns
- Access controls

**Customize:** Cluster count, sizing, isolation model based on budget/compliance/team structure

### 01 - Production

#### Functional Architecture
**File:** `01-production/functional-architecture.py`
**Purpose:** Production functional components and integrations
**Includes:**
- References to baseline OCP diagrams (observability, security, etc.)
- RHOAI production configuration
- Production ML applications
- Enterprise integrations (IDP, PKI, Firewall)
- TrustyAI model monitoring
- Compliance and audit logging

**Customize:** Production-specific requirements, HA, security, compliance

#### Infrastructure Architecture
**File:** `01-production/infrastructure-architecture.py`
**Purpose:** Production physical/infrastructure components
**Includes:**
- Load balancers (external, internal)
- Control plane HA (3 masters)
- Worker nodes (CPU and GPU)
- Storage (SAN, NAS, S3)
- Infrastructure services (DNS, NTP, Proxy, LDAP)
- Backup and DR

**Customize:** On-prem vs cloud, network zones, storage backends, compute types

### 02 - Pre-Production

**Files:**
- `02-preproduction/functional-architecture.py`
- `02-preproduction/infrastructure-architecture.py`

**Purpose:** Pre-production environment (typically shared QA/Test)

**Current State:** Template placeholders
**Customize:** Expand with namespace isolation, reduced HA, QA/Test-specific workflows

### 03 - Sandbox

**Files:**
- `03-sandbox/functional-architecture.py`
- `03-sandbox/infrastructure-architecture.py`

**Purpose:** Sandbox for data scientist experimentation

**Current State:** Template placeholders
**Customize:** Self-service features, relaxed policies, cost-optimized infrastructure

### Common - Shared Services

#### Shared Services
**File:** `common/shared-services.py`
**Purpose:** Cross-environment shared infrastructure
**Includes:**
- Fleet GitOps (multi-cluster management)
- Central container registry
- Aggregated observability
- Centralized backup (Velero/OADP)

**Customize:** Which services are shared vs. per-environment

#### Integration Patterns
**File:** `common/integration-patterns.py`
**Purpose:** Reusable integration patterns
**Includes:**
- IDP/SSO integration pattern
- External storage integration
- Certificate management pattern
- Monitoring/observability integration

**Customize:** Adapt to customer's enterprise standards

## How to Use

### 1. Start with Overview Diagrams
Generate the landscape and topology first to align on high-level approach:
```bash
./venv/bin/python3 diagrams/engagement-ai-platform/00-overview/environment-landscape.py
./venv/bin/python3 diagrams/engagement-ai-platform/00-overview/cluster-topology.py
```

### 2. Customize for Customer
Edit diagrams to match customer specifics:
- Number of environments
- Cluster topology (dedicated vs shared)
- Sizing (node counts, CPU/GPU ratios)
- Network zones and isolation
- Storage backends
- External integrations

### 3. Expand Environment-Specific Diagrams
The pre-prod and sandbox diagrams are currently templates. Expand them based on customer requirements:

```bash
# Example: Expand sandbox functional architecture
vim diagrams/engagement-ai-platform/03-sandbox/functional-architecture.py
# Add: self-service namespace creation, quota management, developer workflows
```

### 4. Reference Baseline Diagrams
Point to baseline diagrams for detailed component views:
```python
# In customer diagram, reference baseline
with Cluster("OCP Platform - Production Config"):
    # Reference: baseline-reference/ocp/01-core-infrastructure.py
    core_infra = Service("Core Infrastructure\n(See baseline-ocp-01)")
```

## Customization Workflow

### For a New Customer Engagement:

1. **Copy this directory**
   ```bash
   cp -r diagrams/engagement-ai-platform diagrams/customer-acme-ai-platform
   ```

2. **Update overview diagrams** with customer's environment strategy

3. **Expand production diagrams** with production requirements

4. **Flesh out pre-prod and sandbox** based on actual customer needs

5. **Adjust shared services** based on what's actually shared

6. **Add customer-specific integrations**
   - Specific IDP product (Okta, Azure AD, etc.)
   - Storage vendor (NetApp, Pure Storage, AWS S3, etc.)
   - Monitoring tools (Splunk, Datadog, Dynatrace, etc.)
   - Network security (Palo Alto, Cisco, etc.)

## Template vs. Reality

**Current State:** These are TEMPLATES showing common patterns

**Your Task:** Adapt to reflect actual customer architecture decisions

**Key Questions to Answer:**
- How many environments? (prod, non-prod, sandbox, others?)
- Dedicated or shared clusters?
- On-premises, cloud, or hybrid?
- What shared services are centralized?
- What are the specific integration points?
- What are sizing requirements?
- What are compliance/security requirements?

## Best Practices

### Environment Isolation
- **Production:** Strict isolation, no direct access from other environments
- **Pre-production:** May share resources but isolated from sandbox
- **Sandbox:** MUST NOT impact production or pre-production

### Diagram Focus
- **Functional:** Component relationships, data flows, integration points
- **Infrastructure:** Physical/virtual resources, network topology, storage backend

### No Pod-Level Details
Keep diagrams at the operator/service level for readability

### Customer-Specific Naming
Use customer's terminology for systems and zones

## Integration with Baseline References

These diagrams **reference** but don't duplicate baseline diagrams:

```
Engagement Diagram (Customer View)
    ↓ references
Baseline Diagram (Complete Component View)
```

For detailed component discussions, use baseline diagrams.
For customer-specific architecture, use engagement diagrams.

## Generated Outputs

All diagrams generate to: `output/engagement-*.png`

View them:
```bash
ls -lh output/engagement-*.png
```

## Next Steps

1. Review generated templates
2. Align with customer on environment strategy (overview diagrams)
3. Expand production diagrams with actual requirements
4. Customize pre-prod and sandbox based on customer needs
5. Document decisions in CLAUDE.md or architecture decision records

## Questions to Resolve with Customer

- How many environments?
- Dedicated clusters or shared?
- GPU requirements per environment?
- Storage backend preferences?
- Network security requirements?
- Compliance requirements (SOC2, HIPAA, etc.)?
- Disaster recovery requirements?
- Multi-region deployment?

Document answers and reflect in diagrams.
