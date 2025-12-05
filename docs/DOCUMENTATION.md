# Code Documentation

This document explains the code documentation in the Task Breakdown Assistant project and how to generate reference documentation.

## Docstrings Overview

The project uses Python docstrings (Google/NumPy style) throughout the codebase to document:
- Modules
- Classes
- Functions
- API endpoints

### Documented Files

All key files have comprehensive docstrings:

1. **`backend/task_breakdown/main.py`** - FastAPI application initialization
   - Module docstring: "Main FastAPI application."
   - Function docstrings for all endpoints

2. **`backend/task_breakdown/services/ai_service.py`** - AI service
   - Module docstring: "AI service for generating detailed task breakdowns."
   - Comprehensive function docstrings with Args, Returns sections

3. **`backend/task_breakdown/api/tasks.py`** - Tasks API
   - Module docstring: "Task API endpoints."
   - Detailed endpoint docstrings

4. **`backend/task_breakdown/api/ratings.py`** - Ratings API
   - Module docstring: "Rating API endpoints."
   - Endpoint docstrings with descriptions

5. **`backend/task_breakdown/api/guides.py`** - Guides API
   - Module docstring: "Guide API endpoints."
   - Endpoint docstrings

6. **`backend/task_breakdown/models.py`** - Database models
   - Class docstrings for Task, GuideStep, Rating models

7. **`backend/task_breakdown/schemas.py`** - Pydantic schemas
   - Class docstrings for all request/response schemas

8. **`backend/task_breakdown/database.py`** - Database configuration
   - Module docstring: "Database configuration and session management."
   - Function docstrings

9. **`backend/task_breakdown/config/logging_config.py`** - Logging configuration
   - Module docstring: "Logging configuration for the application."
   - Function docstrings with Args, Returns sections

## How to Generate Reference Documentation

### Method 1: FastAPI Auto-Generated Documentation (Recommended)

FastAPI automatically generates interactive API documentation from your docstrings and type hints.

**Steps:**

1. Start the backend server:
   ```bash
   cd backend
   poetry run uvicorn task_breakdown.main:app --reload
   ```

2. Open your browser and visit:
   - **Swagger UI**: http://localhost:8000/docs
   - **ReDoc**: http://localhost:8000/redoc

**What you get:**
- Interactive API documentation
- All endpoints with descriptions
- Request/response schemas
- Try-it-out functionality
- Automatically generated from docstrings and type hints

**Example:**
```
GET /api/tasks/{task_id}
Description: Get a specific task with its guide steps.
Parameters: task_id (integer, required)
Responses: 200 (TaskWithGuideResponse), 404 (Not Found), 500 (Internal Server Error)
```

### Method 2: Sphinx Documentation (Advanced)

For more comprehensive documentation including all modules, classes, and functions.

**Installation:**

```bash
cd backend
poetry add --group dev sphinx sphinx-rtd-theme sphinx-autodoc-typehints
```

**Generate documentation:**

1. Initialize Sphinx (first time only):
   ```bash
   poetry run sphinx-quickstart docs --sep -p "Task Breakdown Assistant" -a "Nimra Fayaz" -v "0.1.0" --release "0.1.0" --language en
   ```

2. Configure Sphinx (`docs/source/conf.py`):
   ```python
   import os
   import sys
   sys.path.insert(0, os.path.abspath('../..'))

   extensions = [
       'sphinx.ext.autodoc',
       'sphinx.ext.viewcode',
       'sphinx.ext.napoleon',
       'sphinx_autodoc_typehints',
   ]
   ```

3. Generate HTML documentation:
   ```bash
   poetry run sphinx-build -b html docs/source docs/build/html
   ```

4. View documentation:
   ```bash
   # Open in browser
   open docs/build/html/index.html  # macOS
   start docs/build/html/index.html  # Windows
   xdg-open docs/build/html/index.html  # Linux
   ```

### Method 3: pydoc (Built-in)

Python's built-in documentation generator.

**Generate HTML for a module:**

```bash
cd backend
poetry run python -m pydoc -w task_breakdown.main
poetry run python -m pydoc -w task_breakdown.services.ai_service
poetry run python -m pydoc -w task_breakdown.api.tasks
```

This creates `.html` files that you can open in a browser.

## Docstring Examples

### Module Docstring
```python
"""AI service for generating detailed task breakdowns."""
```

### Function Docstring with Args/Returns
```python
def generate_task_breakdown(task_description: str) -> dict:
    """
    Generate a detailed, beginner-friendly task breakdown using AI.

    Args:
        task_description: The task/assignment description

    Returns:
        Dictionary with task metadata and guide steps
    """
```

### Class Docstring
```python
class Task(Base):
    """Task model - stores task descriptions and metadata."""
```

### API Endpoint Docstring
```python
async def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """
    Create a new task and generate AI-powered breakdown.

    This endpoint takes a task description and uses AI to generate
    a detailed, beginner-friendly step-by-step guide.
    """
```

## Quick Reference

| Component | Documentation Location |
|-----------|----------------------|
| API Endpoints | http://localhost:8000/docs |
| Interactive API | http://localhost:8000/redoc |
| Source Code | All `.py` files have docstrings |
| Schemas | `backend/task_breakdown/schemas.py` |
| Models | `backend/task_breakdown/models.py` |
| Services | `backend/task_breakdown/services/` |
