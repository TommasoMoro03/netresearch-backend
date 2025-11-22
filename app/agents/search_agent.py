"""
Search agent for retrieving papers from OpenAlex.
"""
from typing import List, Dict, Any
from app.agents.models import AgentContext
from app.utils.openalex_client import openalex_client


class SearchAgent:
    """
    Agent responsible for searching papers based on extracted filters.
    """

    def __init__(self):
        self.client = openalex_client

    def search_papers(self, context: AgentContext) -> Dict[str, Any]:
        """
        Search for papers using extracted filters.

        Fetches 2 * max_nodes papers for later filtering based on geographical requirements.

        Args:
            context: Agent context with filters and max_nodes

        Returns:
            Raw JSON response from OpenAlex API

        Process:
        1. For each topic in filters, search for concept ID
        2. Combine all concept IDs
        3. Search for works using combined concept IDs (fetch 2 * max_nodes)
        """
        if not context.filters or not context.filters.topics:
            return {"results": [], "meta": {}}

        # Fetch 2 * max_nodes papers for later filtering
        per_page = context.max_nodes * 2

        # Use the high-level search method
        results = self.client.search_papers_by_topics(
            topics=context.filters.topics,
            per_page=per_page
        )

        return results

    def get_concept_ids(self, topics: List[str]) -> List[str]:
        """
        Get OpenAlex concept IDs for a list of topics.

        Args:
            topics: List of topic names

        Returns:
            List of concept IDs
        """
        return self.client.get_concept_ids_from_topics(topics)
