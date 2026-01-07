# Multi-stage Dockerfile for Task Breakdown Assistant Backend
# Stage 1: Builder stage to install dependencies
FROM python:3.10-slim as builder

# Set working directory
WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry==1.7.1

# Copy dependency files and source code
COPY pyproject.toml poetry.lock ./
COPY task_breakdown /app/task_breakdown

# Configure Poetry to not create virtual environment (we're in a container)
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --no-dev --no-interaction --no-ansi

# Stage 2: Runtime stage
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install Poetry in runtime stage as well
RUN pip install --no-cache-dir poetry==1.7.1

# Copy installed dependencies from builder
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

# Copy application code
COPY task_breakdown /app/task_breakdown
COPY pyproject.toml poetry.lock ./

# Create directory for SQLite database
RUN mkdir -p /app/data

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DATABASE_URL=sqlite:///./data/task_breakdown.db

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Run the application using Python module (packages already installed globally)
CMD ["python", "-m", "uvicorn", "task_breakdown.main:app", "--host", "0.0.0.0", "--port", "8000"]
