"""
OpenAlex API client for retrieving academic research data.

Documentation: https://docs.openalex.org
"""
import requests
from typing import List, Dict, Any, Optional
import time


class OpenAlexClient:
    """Client for interacting with OpenAlex API."""

    BASE_URL = "https://api.openalex.org"

    def __init__(self, email: Optional[str] = None):
        """
        Initialize OpenAlex client.

        Args:
            email: Optional email for polite pool (faster API access)
        """
        self.session = requests.Session()
        if email:
            # Polite pool gets faster response times
            self.session.params = {"mailto": email}

    def search_concepts(self, topic: str) -> Optional[str]:
        """
        Search for a concept by topic name and return its ID.

        Args:
            topic: Topic name to search for (e.g., "Machine Learning")

        Returns:
            Concept ID if found, None otherwise

        API: GET /concepts?search={topic}
        """
        url = f"{self.BASE_URL}/concepts"
        params = {"search": topic}

        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            results = data.get("results", [])

            if results:
                # Return the ID of the first result
                concept_id = results[0].get("id")
                return concept_id

            return None

        except requests.RequestException as e:
            print(f"Error searching concept '{topic}': {e}")
            return None

    def get_concept_ids_from_topics(self, topics: List[str]) -> List[str]:
        """
        Convert a list of topics to OpenAlex concept IDs.

        Args:
            topics: List of topic names

        Returns:
            List of concept IDs (filters out None values)
        """
        concept_ids = []

        for topic in topics:
            concept_id = self.search_concepts(topic)
            if concept_id:
                concept_ids.append(concept_id)
            # Small delay to be polite to the API
            time.sleep(0.2)

        return concept_ids

    def search_works_by_concepts(
        self,
        concept_ids: List[str],
        per_page: int = 25,
        page: int = 1
    ) -> Dict[str, Any]:
        """
        Search for works (papers) by concept IDs.

        Args:
            concept_ids: List of OpenAlex concept IDs
            per_page: Number of results per page (max 200)
            page: Page number

        Returns:
            Raw JSON response from OpenAlex

        API: GET /works?filter=concepts.id:{id1},concepts.id:{id2}
        """
        url = f"{self.BASE_URL}/works"

        # Build filter string: concepts.id:ID1,concepts.id:ID2
        concept_filters = ",".join([f"concepts.id:{cid}" for cid in concept_ids])

        params = {
            "filter": concept_filters,
            "per-page": per_page,
            "page": page
        }

        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()

            return response.json()

        except requests.RequestException as e:
            print(f"Error searching works: {e}")
            return {"results": [], "meta": {}}

    def search_papers_by_topics(
        self,
        topics: List[str],
        per_page: int = 25
    ) -> Dict[str, Any]:
        """
        High-level method: Search for papers by topic names.

        This combines concept search and works search into one operation.

        Args:
            topics: List of topic names (e.g., ["Robotics", "AI"])
            per_page: Number of results to return

        Returns:
            Raw JSON response with papers
        """
        # Step 1: Convert topics to concept IDs
        concept_ids = self.get_concept_ids_from_topics(topics)

        if not concept_ids:
            print(f"Warning: No concept IDs found for topics: {topics}")
            return {"results": [], "meta": {}}

        # Step 2: Search for works using concept IDs
        return self.search_works_by_concepts(concept_ids, per_page=per_page)

    def extract_author_id(self, author_url: str) -> str:
        """
        Extract author ID from OpenAlex author URL.

        Args:
            author_url: Full URL like "https://openalex.org/A5068353058"

        Returns:
            Author ID like "A5068353058"
        """
        return author_url.split("/")[-1]

    def get_author(self, author_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed author information by ID.

        Args:
            author_id: Author ID (e.g., "A5068353058")

        Returns:
            Author JSON data or None if error

        API: GET /authors/{id}
        """
        # Clean the ID if it contains the full URL
        if "/" in author_id:
            author_id = self.extract_author_id(author_id)

        url = f"{self.BASE_URL}/authors/{author_id}"

        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()

        except requests.RequestException as e:
            print(f"Error fetching author {author_id}: {e}")
            return None

    def get_author_works(
        self,
        author_id: str,
        per_page: int = 3
    ) -> Dict[str, Any]:
        """
        Get works (papers) by a specific author.

        Args:
            author_id: Author ID (e.g., "A5068353058")
            per_page: Number of papers to return (default: 3)

        Returns:
            Raw JSON response with author's papers

        API: GET /works?filter=author.id:{id}
        """
        # Clean the ID if it contains the full URL
        if "/" in author_id:
            author_id = self.extract_author_id(author_id)

        url = f"{self.BASE_URL}/works"
        params = {
            "filter": f"author.id:{author_id}",
            "per-page": per_page
        }

        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()

        except requests.RequestException as e:
            print(f"Error fetching works for author {author_id}: {e}")
            return {"results": [], "meta": {}}


# Global client instance
openalex_client = OpenAlexClient()
