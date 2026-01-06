"""Pytest configuration and shared fixtures."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from task_breakdown.database import Base, get_db
from task_breakdown.main import app

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_task_breakdown.db"
test_engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def setup_database():
    """Set up test database before each test."""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def sample_task_data():
    """Sample task data for testing."""
    return {
        "title": "Test Task",
        "description": "Create a hello world program in Python",
    }


@pytest.fixture
def sample_breakdown_data():
    """Sample AI breakdown response for testing."""
    return {
        "title": "Test Task",
        "complexity_score": 5,
        "estimated_total_time": 60,
        "steps": [
            {
                "step_number": 1,
                "title": "Step 1",
                "description": "First step",
                "detailed_instructions": "Do this first",
                "estimated_time": 10,
                "dependencies": [],
                "resources": [],
                "code_snippets": ["print('Hello World')"],
                "tips": "Tip 1",
                "warnings": None,
                "verification_steps": "Check result",
            },
            {
                "step_number": 2,
                "title": "Step 2",
                "description": "Second step",
                "detailed_instructions": "Do this second",
                "estimated_time": 20,
                "dependencies": [1],
                "resources": ["https://example.com"],
                "code_snippets": [],
                "tips": None,
                "warnings": "Warning message",
                "verification_steps": "Verify step 2",
            },
        ],
    }
