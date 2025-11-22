"""
Utility functions for mapping OpenAlex API responses to Paper objects.
"""
from typing import List, Dict, Any, Optional
from app.schemas.agent import Paper


def map_openalex_work_to_paper(work: Dict[str, Any]) -> Paper:
    """
    Map a single OpenAlex work to a Paper object.

    OpenAlex work structure:
    {
        "title": "...",
        "publication_year": 2023,
        "doi": "https://doi.org/10.1234/...",
        "primary_topic": {
            "display_name": "Machine Learning"
        },
        ...
    }

    Args:
        work: OpenAlex work JSON object

    Returns:
        Paper object
    """
    # Extract primary topic
    topic = None
    if work.get("primary_topic"):
        topic = work["primary_topic"].get("display_name")

    return Paper(
        title=work.get("title", "Untitled"),
        link=work.get("doi"),  # DOI field
        abstract="[Abstract to be populated]",  # Placeholder for now
        publication_year=work.get("publication_year"),
        topic=topic
    )


def map_openalex_works_to_papers(works: List[Dict[str, Any]]) -> List[Paper]:
    """
    Map a list of OpenAlex works to Paper objects.

    Args:
        works: List of OpenAlex work JSON objects

    Returns:
        List of Paper objects
    """
    return [map_openalex_work_to_paper(work) for work in works]


def get_preview_papers(works: List[Dict[str, Any]], limit: int = 4) -> List[Paper]:
    """
    Get a preview (first N) papers from OpenAlex works for frontend display.

    Args:
        works: List of OpenAlex work JSON objects
        limit: Number of papers to return (default: 4)

    Returns:
        List of up to `limit` Paper objects
    """
    preview_works = works[:limit]
    return map_openalex_works_to_papers(preview_works)
