"""
RHOAI External Integration - Simplified (Direct Graphviz)

Shows RHOAI platform integration with external services:
- Central AI Platform
- User personas (Data Scientists, MLOps Engineers, Developers)
- Database services
- Storage services

Uses direct Graphviz with HTML table labels for perfect icon centering.
"""

from graphviz import Digraph
import os

# Get absolute paths for icons
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(BASE_DIR, '../../..')

# Platform and service icons
AI_PLATFORM_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Technology icons/Red Hat AI/Technology_icon-Red_Hat-AI-Standard-RGB.Large_icon_transparent.png")
STORAGE_STACK_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/Storage stack/Icon-Red_Hat-Storage_stack-A-Red-RGB.Large_icon_transparent.png")
BUCKET_ICON = os.path.join(PROJECT_ROOT, "custom_icons/Icons/Bucket/Icon-Red_Hat-Bucket-A-Red-RGB.Large_icon_transparent.png")
KEY_ICON = os.path.join(PROJECT_ROOT, "custom_icons/UI icons/rh-ui-icon-key-fill.Large_icon_transparent.png")

# User icons
USERS_ICON = os.path.join(PROJECT_ROOT, "custom_icons/UI icons/rh-ui-icon-users-fill.Large_icon_transparent.png")

# Helper function
def html_node(icon_path, label_text):
    """Create HTML table label for perfect centering"""
    return f'''<<table border="0">
<tr><td><img src="{icon_path}"/></td></tr>
<tr><td>{label_text}</td></tr>
</table>>'''

# Create diagram
dot = Digraph("RHOAI_External_Integration", filename="output/rhoai-external-integration")
dot.attr(rankdir="TB")
dot.attr(fontsize="14", bgcolor="white", pad="0.5", nodesep="1.5", ranksep="1.5")

# ========== ACTORS (TOP) ==========
with dot.subgraph(name='cluster_actors') as actors:
    actors.attr(rank='same')
    actors.node('data_scientist', label=html_node(USERS_ICON, 'Data Scientists'), shape='none')
    actors.node('mlops_engineer', label=html_node(USERS_ICON, 'MLOps Engineers'), shape='none')
    actors.node('developers', label=html_node(USERS_ICON, 'Developers'), shape='none')

# ========== AI PLATFORM (CENTER) ==========
with dot.subgraph(name='cluster_platform') as platform:
    platform.attr(label='Red Hat OpenShift AI Platform', margin='20', bgcolor='lightblue', style='rounded')
    platform.node('ai_platform', label=html_node(AI_PLATFORM_ICON, 'AI Platform'), shape='none')

# ========== SERVICES (BOTTOM) ==========
with dot.subgraph(name='cluster_services') as services:
    services.attr(rank='same')

    # Identity Provider
    with services.subgraph(name='cluster_idp') as idp:
        idp.attr(label='Identity Provider', margin='15', bgcolor='lightyellow', style='rounded')
        idp.node('identity_provider', label=html_node(KEY_ICON, 'IDP'), shape='none')

    # Database services
    with services.subgraph(name='cluster_databases') as db:
        db.attr(label='Database Services', margin='15', bgcolor='lightyellow', style='rounded')
        db.node('databases', label=html_node(STORAGE_STACK_ICON, 'Databases'), shape='none')

    # Storage services
    with services.subgraph(name='cluster_storage') as storage:
        storage.attr(label='Storage Services', margin='15', bgcolor='lightyellow', style='rounded')
        storage.node('storage', label=html_node(BUCKET_ICON, 'Object Storage'), shape='none')

# ========== CONNECTIONS ==========
# Users to platform
dot.edge('data_scientist', 'ai_platform', label='ML workflows')
dot.edge('mlops_engineer', 'ai_platform', label='model deployment')
dot.edge('developers', 'ai_platform', label='app integration')

# Platform to services
dot.edge('ai_platform', 'identity_provider', label='authentication')
dot.edge('ai_platform', 'databases', label='training data')
dot.edge('ai_platform', 'storage', label='models & artifacts')

# Render diagram
dot.render(format='png', view=False, quiet=True)

print("✓ Generated: output/rhoai-external-integration.png (Direct Graphviz with HTML tables)")
print("  → Simplified external integration: AI Platform + Actors + IDP/Database/Storage services")
print("  → All icons perfectly centered!")
