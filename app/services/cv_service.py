import io
import PyPDF2
import openai
import json
from typing import List
from app.core.config import settings

class CVService:
    """
    Service for processing CVs.
    """

    def __init__(self):
        config = settings.get_openai_client_config()
        self.client = openai.OpenAI(**config)
        self.model = settings.MODEL_NAME

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
        Return ONLY a JSON array of strings. Do not include any other text.
        
        CV Text:
        {text}
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert academic researcher helper. Output valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                response_format={"type": "json_object"} 
            )
            
            content = response.choices[0].message.content
            
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
                # Fallback if not valid JSON (should be rare with response_format)
                print(f"Failed to parse JSON from LLM: {content}")
                return []
                
        except Exception as e:
            print(f"Error extracting concepts: {e}")
            # Return empty list instead of failing completely
            return []

# Global instance
cv_service = CVService()
