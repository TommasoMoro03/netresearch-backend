from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.email_service import email_service
from app.services.state_manager import state_manager

router = APIRouter(prefix="/api/email", tags=["Email"])

from enum import Enum

class EmailType(str, Enum):
    COLAB = "colab"
    REACH_OUT = "reach_out"

class EmailGenerateRequest(BaseModel):
    email_type: EmailType
    cv_id: str
    professor_name: str
    professor_context: str
    recipient_name: Optional[str] = None

class EmailGenerateResponse(BaseModel):
    content: str
    message: str

class EmailSendRequest(BaseModel):
    email_content: str
    recipient_email: str

class EmailSendResponse(BaseModel):
    status: str
    message: str

@router.post("/generate", response_model=EmailGenerateResponse)
async def generate_email(request: EmailGenerateRequest):
    """
    Generate an email based on type and context using LLM.
    """
    try:
        # Fetch CV data
        cv_data = state_manager.get_cv(request.cv_id)
        if not cv_data:
            raise HTTPException(status_code=404, detail="CV not found")
            
        # Extract CV info
        cv_text = cv_data.get("text_preview", "")
        cv_concepts = cv_data.get("concepts", [])
        
        # Generate email
        content = email_service.generate_email(
            email_type=request.email_type.value,
            professor_name=request.professor_name,
            professor_context=request.professor_context,
            cv_text=cv_text,
            cv_concepts=cv_concepts,
            recipient_name=request.recipient_name
        )
        
        return EmailGenerateResponse(
            content=content,
            message="Email generated successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/send", response_model=EmailSendResponse)
async def send_email(request: EmailSendRequest):
    """
    Send an email (TODO).
    """
    # TODO: Implement real sending logic
    return EmailSendResponse(
        status="pending",
        message="Email sending is not implemented yet (TODO)"
    )
