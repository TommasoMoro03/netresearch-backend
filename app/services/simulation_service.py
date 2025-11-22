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

    # Mock data templates
    node_types = ["professor", "laboratory", "paper", "institution"]

    # Example professor node
    nodes.append({
        "id": "prof-1",
        "name": "Dr. Jane Smith",
        "type": "professor",
        "description": "Professor of Machine Learning and Computer Vision at MIT",
        "sources": [
            "https://example.com/jane-smith-profile",
            "https://scholar.google.com/citations?user=example"
        ],
        "contacts": [
            "jsmith@mit.edu",
            "https://janesmith.ai"
        ],
        "hierarchy": None
    })

    # Example laboratory node with hierarchy
    nodes.append({
        "id": "lab-1",
        "name": "AI Research Lab",
        "type": "laboratory",
        "description": "Leading laboratory in artificial intelligence and deep learning research",
        "sources": [
            "https://example.com/ai-lab",
            "https://ailab.mit.edu/publications"
        ],
        "contacts": [
            "contact@ailab.mit.edu",
            "https://ailab.mit.edu"
        ],
        "hierarchy": [
            {
                "full_name": "Dr. Jane Smith",
                "role": "Lab Director",
                "contact": "jsmith@mit.edu"
            },
            {
                "full_name": "Dr. John Doe",
                "role": "Senior Researcher",
                "contact": "https://linkedin.com/in/johndoe"
            },
            {
                "full_name": "Alice Johnson",
                "role": "PhD Student",
                "contact": "alice@mit.edu"
            }
        ]
    })

    # Example paper node
    nodes.append({
        "id": "paper-1",
        "name": "Advances in Neural Network Architectures",
        "type": "paper",
        "description": "A comprehensive study on modern neural network designs and their applications",
        "sources": [
            "https://arxiv.org/abs/1234.5678",
            "https://paperswithcode.com/paper/example"
        ],
        "contacts": [],
        "hierarchy": None
    })

    # Example institution node
    nodes.append({
        "id": "inst-1",
        "name": "Massachusetts Institute of Technology",
        "type": "institution",
        "description": "Private research university in Cambridge, Massachusetts",
        "sources": [
            "https://mit.edu",
            "https://csail.mit.edu"
        ],
        "contacts": [
            "https://mit.edu/contact"
        ],
        "hierarchy": None
    })

    # Generate additional mock nodes to reach max_nodes
    for i in range(4, max_nodes):
        node_type = random.choice(node_types)

        node = {
            "id": f"{node_type}-{i}",
            "name": f"Mock {node_type.title()} {i}",
            "type": node_type,
            "description": f"Description of {node_type} number {i}",
            "sources": [f"https://example.com/{node_type}-{i}"],
            "contacts": [f"contact{i}@example.com"],
            "hierarchy": None
        }

        # Add hierarchy if it's a lab
        if node_type == "laboratory":
            node["hierarchy"] = [
                {
                    "full_name": f"Dr. Leader {i}",
                    "role": "Lab Director",
                    "contact": f"leader{i}@example.com"
                },
                {
                    "full_name": f"Researcher {i}",
                    "role": "Senior Researcher",
                    "contact": f"researcher{i}@example.com"
                }
            ]

        nodes.append(node)

    # Create links between nodes
    links.append({
        "source": "prof-1",
        "target": "lab-1",
        "label": "works_at"
    })

    links.append({
        "source": "prof-1",
        "target": "paper-1",
        "label": "authored"
    })

    links.append({
        "source": "lab-1",
        "target": "inst-1",
        "label": "part_of"
    })

    # Add random links for remaining nodes
    for i in range(4, min(max_nodes, len(nodes))):
        source_idx = random.randint(0, i - 1)
        links.append({
            "source": nodes[source_idx]["id"],
            "target": nodes[i]["id"],
            "label": random.choice(["collaborates_with", "cites", "affiliated_with", "works_at"])
        })

    return {"nodes": nodes, "links": links}
