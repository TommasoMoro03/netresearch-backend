from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import cv, agent, email, user, chat, audio

app = FastAPI(
    title="NetResearch Agent API",
    description="Backend API for NetResearch Agent - 3D Research Graph Visualization",
    version="1.0.0"
)

# CORS configuration for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://netresearch-frontend.vercel.app",
        "https://deepscience.ai",
        "https://app.deepscience.ai"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(agent.router)
app.include_router(user.router)
app.include_router(cv.router)
app.include_router(email.router)
app.include_router(chat.router)
app.include_router(audio.router)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "message": "DeepScience Agent API is running",
        "status": "healthy"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}
