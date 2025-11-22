import time
import random
from app.services.state_manager import state_manager


def simulate_agent_run(run_id: str, query: str, max_nodes: int):
    """
    Background task that simulates agent thinking process.
    Adds mock logs step-by-step over ~10 seconds.
    """
    steps = [
        ("Intent Recognition", f"Identified topic: {query}"),
        ("Query Expansion", "Expanding search terms based on semantic similarity"),
        ("OpenAlex Search", f"Searching for papers related to '{query}'"),
        ("Citation Analysis", "Analyzing citation networks"),
        ("Graph Construction", f"Building graph with {max_nodes} nodes"),
        ("Relevance Scoring", "Ranking papers by relevance"),
        ("Finalization", "Graph construction complete")
    ]

    for step_name, step_message in steps:
        time.sleep(1.5)  # Simulate processing time
        state_manager.add_run_step(run_id, step_name, step_message)

    # Generate mock graph data
    graph_data = generate_mock_graph(max_nodes)
    state_manager.set_run_graph(run_id, graph_data)

    # Mark as completed
    state_manager.update_run_status(run_id, "completed")


def generate_mock_graph(max_nodes: int):
    """Generate mock graph data with nodes and links."""
    nodes = []
    links = []

    for i in range(max_nodes):
        nodes.append({
            "id": f"node-{i}",
            "label": f"Paper {i}: Research Topic {i}",
            "type": "paper",
            "x": random.uniform(-100, 100),
            "y": random.uniform(-100, 100),
            "z": random.uniform(-100, 100)
        })

    # Create some random links
    for i in range(max_nodes - 1):
        links.append({
            "source": f"node-{i}",
            "target": f"node-{i+1}",
            "label": "cites"
        })

    return {"nodes": nodes, "links": links}
