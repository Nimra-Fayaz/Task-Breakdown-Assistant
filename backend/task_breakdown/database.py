"""Database configuration and session management."""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from task_breakdown.config.logging_config import get_logger

load_dotenv()

logger = get_logger(__name__)

# Database URL from environment or default to SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./task_breakdown.db")

logger.debug(
    f"Database URL configured: {DATABASE_URL.split('@')[-1] if '@' in DATABASE_URL else DATABASE_URL}"
)

# Create engine
try:
    if DATABASE_URL.startswith("sqlite"):
        logger.debug("Creating SQLite database engine")
        engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    else:
        logger.debug("Creating database engine (non-SQLite)")
        engine = create_engine(DATABASE_URL)
    logger.info("Database engine created successfully")
except Exception as e:
    logger.critical(f"Failed to create database engine: {e}")
    raise

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
logger.debug("Database session factory created")

# Base class for models
Base = declarative_base()


def get_db():
    """Dependency for getting database session."""
    logger.debug("Creating new database session")
    db = SessionLocal()
    try:
        yield db
        logger.debug("Database session committed successfully")
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        # Check for specific critical database errors
        error_str = str(e).lower()
        if "connection" in error_str or "unavailable" in error_str:
            logger.critical(f"Critical database connection error: {e}")
        elif "integrity constraint" in error_str:
            logger.warning(f"Database integrity constraint violation: {e}")
        raise
    finally:
        db.close()
        logger.debug("Database session closed")
