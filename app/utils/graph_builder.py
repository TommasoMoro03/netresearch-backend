"""
Utility functions for building graph data (nodes and links).
"""
from typing import List, Dict, Any
from collections import defaultdict
from app.schemas.agent import GraphNode, GraphLink, Contact, Institution


def build_graph_links(professor_nodes: List[Dict[str, Any]]) -> List[GraphLink]:
    """
    Build links between professors based on institution hierarchy.

    Logic:
    1. Group professors by institution ID
    2. Select boss (highest h-index) for each institution
    3. Connect boss to all other professors in the same institution
    4. Create a "User" node
    5. Connect User to all bosses

    Args:
        professor_nodes: List of professor GraphNode dicts

    Returns:
        List of GraphLink objects
    """
    links = []

    # Convert dicts back to GraphNode objects for easier access
    professors = [GraphNode(**node) for node in professor_nodes]

    # Group professors by institution ID
    institution_groups: Dict[str, List[GraphNode]] = defaultdict(list)

    for prof in professors:
        if prof.institution and prof.institution.id:
            institution_groups[prof.institution.id].append(prof)

    # Find boss for each institution and create links
    bosses = []

    for inst_id, profs in institution_groups.items():
        if not profs:
            continue

        # Find boss (highest h-index)
        boss = max(profs, key=lambda p: p.h_index if p.h_index is not None else -1)
        bosses.append(boss)

        # Connect boss to all other professors in the institution
        for prof in profs:
            if prof.id != boss.id:
                links.append(GraphLink(
                    source=boss.id,
                    target=prof.id,
                    label="supervises"
                ))

    # Create User node (will be added to nodes list separately)
    # Connect User to all bosses
    user_id = "user-node"
    for boss in bosses:
        links.append(GraphLink(
            source=user_id,
            target=boss.id,
            label="interested_in"
        ))

    return links


def create_user_node() -> GraphNode:
    """
    Create a User node for the graph.

    Returns:
        GraphNode representing the user
    """
    return GraphNode(
        id="user-node",
        name="User",
        type="user",
        institution=None,
        description="You - the researcher exploring this network",
        contacts=Contact(email=None, website=None),
        works_count=None,
        cited_by_count=None,
        h_index=None,
        link_orcid=None,
        papers=None
    )
