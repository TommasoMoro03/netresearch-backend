from pydantic import BaseModel
from typing import List


class CVUploadResponse(BaseModel):
    cv_id: str
    filename: str
    message: str
    extracted_concepts: List[str]
