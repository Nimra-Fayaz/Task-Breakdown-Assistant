"""Main FastAPI application."""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from task_breakdown.api import guides, ratings, tasks
from task_breakdown.config.logging_config import get_logger, setup_logging
from task_breakdown.database import Base, engine

# Setup logging configuration after imports but before app initialization
setup_logging(log_level=logging.INFO)

# Get logger for this module
logger = get_logger(__name__)

# Create database tables
logger.info("Initializing database tables")
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables initialized successfully")
    logger.debug("All database models registered and tables created")
except Exception as e:
    logger.critical(f"Failed to create database tables: {e}")
    raise

app = FastAPI(
    title="Task Breakdown Assistant API",
    description="AI-powered task breakdown assistant with beginner-friendly detailed guides",
    version="0.1.0",
)

logger.info("FastAPI application initialized")

# CORS middleware for frontend
logger.debug("Configuring CORS middleware")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
    ],  # Vite and React default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger.debug("CORS middleware configured for frontend access")

# Include routers
logger.debug("Registering API routers")
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
logger.debug("Tasks router registered at /api/tasks")
app.include_router(guides.router, prefix="/api/guides", tags=["guides"])
logger.debug("Guides router registered at /api/guides")
app.include_router(ratings.router, prefix="/api/ratings", tags=["ratings"])
logger.debug("Ratings router registered at /api/ratings")
logger.info("All API routers registered successfully")


@app.get("/")
async def root():
    """Root endpoint."""
    logger.debug("Root endpoint accessed")
    logger.info("API root endpoint called")
    return {
        "message": "Task Breakdown Assistant API",
        "version": "0.1.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    logger.debug("Health check endpoint accessed")
    try:
        # Basic health check - verify database connection
        from sqlalchemy import text

        from task_breakdown.database import engine

        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Health check passed - database connection OK")
        return {"status": "healthy"}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        logger.critical(
            "Critical: Health check failed - database connection unavailable"
        )
        return {"status": "unhealthy", "error": str(e)}, 503
