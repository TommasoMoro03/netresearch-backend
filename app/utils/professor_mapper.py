"""
Utility functions for mapping OpenAlex author data to Professor/GraphNode objects.
"""
from typing import List, Dict, Any, Optional
from app.schemas.agent import GraphNode, BasicProfessor, Contact, Paper
from app.utils.paper_mapper import map_openalex_works_to_papers
from app.utils.openalex_client import openalex_client


def get_education_institution(author_data: Dict[str, Any]) -> Optional[str]:
    """
    Extract the education institution name from author's last_known_institutions.

    Args:
        author_data: OpenAlex author JSON

    Returns:
        Institution display_name or None
    """
    institutions = author_data.get("last_known_institutions", [])

    for inst in institutions:
        if inst.get("type") == "education":
            return inst.get("display_name")

    # If no education institution, return first institution
    if institutions:
        return institutions[0].get("display_name")

    return None


def map_author_to_graph_node(
    author_data: Dict[str, Any],
    author_papers: Optional[List[Dict[str, Any]]] = None
) -> GraphNode:
    """
    Map OpenAlex author data to a GraphNode (professor).

    Args:
        author_data: OpenAlex author JSON
        author_papers: Optional list of author's papers (first 3)

    Returns:
        GraphNode representing the professor
    """
    # Extract author ID from URL
    author_id = author_data.get("id", "").split("/")[-1]

    # Get institution
    institution = get_education_institution(author_data)

    # Map papers
    papers = []
    if author_papers:
        papers = map_openalex_works_to_papers(author_papers[:3])

    # Create contact (mock for now)
    contact = Contact(
        email=f"{author_data.get('display_name', 'unknown').lower().replace(' ', '.')}@example.com",
        website=author_data.get("ids", {}).get("orcid")
    )

    # Get h-index from summary_stats
    h_index = None
    summary_stats = author_data.get("summary_stats", {})
    if summary_stats:
        h_index = summary_stats.get("h_index")

    # Create description
    description = f"Researcher at {institution}" if institution else "Academic researcher"
    if author_data.get("works_count"):
        description += f" with {author_data['works_count']} publications"

    return GraphNode(
        id=author_id,
        name=author_data.get("display_name", "Unknown Author"),
        type="professor",
        institution=institution,
        description=description,
        contacts=contact,
        works_count=author_data.get("works_count"),
        cited_by_count=author_data.get("cited_by_count"),
        h_index=h_index,
        link_orcid=author_data.get("orcid"),
        papers=[paper.model_dump() for paper in papers] if papers else None
    )


def map_author_to_basic_professor(author_data: Dict[str, Any]) -> BasicProfessor:
    """
    Map OpenAlex author data to BasicProfessor (for frontend display during extraction).

    Args:
        author_data: OpenAlex author JSON

    Returns:
        BasicProfessor with minimal info
    """
    institution = get_education_institution(author_data)
    description = f"{author_data.get('works_count', 0)} publications, h-index: {author_data.get('summary_stats', {}).get('h_index', 'N/A')}"

    return BasicProfessor(
        name=author_data.get("display_name", "Unknown Author"),
        institution=institution,
        description=description
    )


def extract_author_ids_from_papers(papers: List[Dict[str, Any]], max_papers: int, authors_per_paper: int = 2) -> List[str]:
    """
    Extract author IDs from papers' authorships.

    Args:
        papers: List of OpenAlex work objects
        max_papers: Maximum number of papers to process
        authors_per_paper: Number of authors to extract per paper (default: 2)

    Returns:
        List of unique author IDs
    """
    author_ids = []
    seen_ids = set()

    for paper in papers[:max_papers]:
        authorships = paper.get("authorships", [])

        for authorship in authorships[:authors_per_paper]:
            author = authorship.get("author", {})
            author_id_url = author.get("id")

            if author_id_url:
                # Extract ID from URL
                author_id = openalex_client.extract_author_id(author_id_url)

                # Add if not seen before
                if author_id not in seen_ids:
                    author_ids.append(author_id)
                    seen_ids.add(author_id)

    return author_ids
