"""
Extraction agent for retrieving and mapping professor data from papers.
"""
import time
from typing import List, Tuple
from app.agents.models import AgentContext
from app.schemas.agent import GraphNode, BasicProfessor
from app.utils.openalex_client import openalex_client
from app.utils.professor_mapper import (
    extract_author_ids_from_papers,
    map_author_to_graph_node,
    map_author_to_basic_professor
)


class ExtractionAgent:
    """
    Agent responsible for extracting professor information from papers.

    Process:
    1. Extract author IDs from first max_nodes papers (first 2 authors per paper)
    2. Fetch detailed author data for each ID
    3. Fetch first 3 papers for each author
    4. Map to GraphNode (full data) and BasicProfessor (display data)
    """

    def __init__(self):
        self.client = openalex_client

    def extract_professors(
        self,
        context: AgentContext
    ) -> Tuple[List[GraphNode], List[BasicProfessor]]:
        """
        Extract professors from papers.

        Args:
            context: Agent context with papers_data

        Returns:
            Tuple of (full professor nodes, basic professors for display)
        """
        if not context.papers_data:
            return [], []

        # Step 1: Extract author IDs from first max_nodes papers
        author_ids = extract_author_ids_from_papers(
            papers=context.papers_data,
            max_papers=context.max_nodes,
            authors_per_paper=2
        )

        if not author_ids:
            return [], []

        # Step 2 & 3: Fetch author data and their papers
        professor_nodes = []
        basic_professors = []

        for author_id in author_ids:
            # Fetch author details
            author_data = self.client.get_author(author_id)

            if not author_data:
                continue

            # Fetch author's papers (first 3)
            author_works_response = self.client.get_author_works(author_id, per_page=3)
            author_papers = author_works_response.get("results", [])

            # Map to GraphNode (full data for graph)
            professor_node = map_author_to_graph_node(author_data, author_papers)
            professor_nodes.append(professor_node)

            # Map to BasicProfessor (display data for frontend)
            basic_prof = map_author_to_basic_professor(author_data)
            basic_professors.append(basic_prof)

            # Small delay to be polite to the API
            time.sleep(0.3)

        return professor_nodes, basic_professors
