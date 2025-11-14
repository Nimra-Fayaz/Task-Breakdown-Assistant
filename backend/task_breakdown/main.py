"""Main FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from task_breakdown.api import tasks, guides, ratings
from task_breakdown.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Breakdown Assistant API",
    description="AI-powered task breakdown assistant with beginner-friendly detailed guides",
    version="0.1.0",
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite and React default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(guides.router, prefix="/api/guides", tags=["guides"])
app.include_router(ratings.router, prefix="/api/ratings", tags=["ratings"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Task Breakdown Assistant API",
        "version": "0.1.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}

