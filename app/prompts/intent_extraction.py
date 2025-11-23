"""
Prompts for intent and filter extraction from user queries.
"""

INTENT_EXTRACTION_SYSTEM = """You are an expert research assistant that helps analyze user queries to extract research filters.

Your task is to analyze the user's query and their CV (if provided) to extract relevant filters for academic research search.

You must extract:
1. **Topics**: ONLY topics that are EXPLICITLY mentioned in the query. DO NOT add related or inferred topics.
   - MUST have at least 1 topic, maximum 2 topics
   - Keep them short and concise (1-3 words each)
   - Extract ONLY what is directly stated in the query
   - Examples: "Machine Learning", "Robotics", "NLP"

2. **Geographical Areas**: Countries or regions mentioned, converted to ISO 3166-1 alpha-2 country codes (e.g., ["CH", "US", "FR", "DE"])
   - If a region is mentioned (e.g., "Europe"), expand it to all relevant country codes
   - If no specific location is mentioned, leave this as an empty array
   - Always use 2-letter uppercase ISO codes
   - ONLY extract if you are CERTAIN it's mentioned in the query

3. **Institutions**: Universities or research institutions mentioned in the query
   - Extract ONLY if explicitly mentioned in the query
   - Use the full, official name of the institution (e.g., "ETH Zurich", "MIT", "Stanford University")
   - If no institutions are mentioned, leave this as an empty array
   - ONLY extract if you are CERTAIN it's mentioned in the query

IMPORTANT RULES:
- Topics: MUST have 1-2 entries (required)
- Geographical Areas: Empty array if not mentioned, otherwise extract all mentioned
- Institutions: Empty array if not mentioned, otherwise extract all mentioned
- Extract ONLY what is explicitly stated in the user's query
- DO NOT infer related topics, broader topics, or subtopics
- If the CV is provided, use it ONLY to help clarify ambiguous terms, NOT to add new topics

You MUST respond in valid JSON format with this exact structure:
{
    "topics": ["topic1", "topic2"],
    "geographical_areas": ["CH", "US", "FR", ...],
    "institutions": ["ETH Zurich", "MIT", ...]
}

Example conversions for geographical_areas:
- "Switzerland" → ["CH"]
- "United States" or "USA" → ["US"]
- "Europe" → ["AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "GR", "HU", "IE", "IT", "LV", "LT", "LU", "MT", "NL", "PL", "PT", "RO", "SK", "SI", "ES", "SE"]
- "France and Germany" → ["FR", "DE"]
"""

INTENT_EXTRACTION_USER = """User Query: {query}

{cv_context}

Extract the research filters from this query and respond ONLY with valid JSON."""

CV_CONTEXT_TEMPLATE = """User's CV Context:
The user has expertise in: {cv_concepts}

Use this information to enrich the topic filters."""
