import io
import PyPDF2
import json
from typing import List
from app.core.llm_factory import get_llm_config
from pyagentspec import Agent
from wayflowcore.agentspec import AgentSpecLoader


class CVService:
    """
    Service for processing CVs.
    """

    def __init__(self):
        self.llm_config = get_llm_config()

        # Create AgentSpec agent for CV concept extraction
        self.spec_agent = Agent(
            name="cv_concept_extractor",
            system_prompt="You are an expert academic researcher helper. Output valid JSON only.",
            llm_config=self.llm_config
        )

        # Load with Wayflow
        self.agent = AgentSpecLoader().load_component(self.spec_agent)

    def extract_text_from_pdf(self, file_content: bytes) -> str:
        """
        Extract text from a PDF file content.
        """
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            raise ValueError("Could not extract text from PDF file")

    def extract_concepts_from_text(self, text: str) -> List[str]:
        """
        Extract research concepts/keywords from CV text using LLM.
        """
        # Truncate text if too long to avoid token limits (rough estimate)
        max_chars = 10000
        if len(text) > max_chars:
            text = text[:max_chars] + "..."

        prompt = f"""
Analyze the following CV text and extract a list of 5-10 key research concepts, scientific topics, or technical skills relevant to academic research.
Return ONLY a JSON object with a "concepts" field containing an array of strings. Do not include any other text.

Example format:
{{"concepts": ["Machine Learning", "Neural Networks", "Computer Vision"]}}

CV Text:
{text}
"""

        try:
            # Start conversation
            conv = self.agent.start_conversation()
            conv.append_user_message(prompt)

            # Execute
            conv.execute()

            # Get response
            messages = conv.get_messages()
            if not messages:
                print("No response from agent")
                return []

            # Get last message
            last_message = messages[-1]
            content = last_message.content.strip()

            # Try to extract JSON if wrapped in markdown code blocks
            if content.startswith("```"):
                # Remove markdown code blocks
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:].strip()

            # Parse JSON response
            try:
                data = json.loads(content)
                # Handle different potential JSON structures
                if isinstance(data, list):
                    return data
                elif "concepts" in data:
                    return data["concepts"]
                elif "topics" in data:
                    return data["topics"]
                else:
                    # Fallback: try to find any list in values
                    for val in data.values():
                        if isinstance(val, list):
                            return val
                    return []
            except json.JSONDecodeError:
                # Fallback if not valid JSON
                print(f"Failed to parse JSON from LLM: {content}")
                return []

        except Exception as e:
            print(f"Error extracting concepts: {e}")
            # Return empty list instead of failing completely
            return []

# Global instance
cv_service = CVService()
