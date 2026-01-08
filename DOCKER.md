# Docker Multi-Container Setup

Guide for running the Task Breakdown Assistant using Docker Compose.

## Overview

This application uses Docker Compose to orchestrate three containers:
- **Frontend**: React application with Nginx (Port 5173)
- **Backend**: FastAPI REST API (Port 8000)
- **Ollama**: Local AI service with llama3.2 model (Port 11434)

Data is persisted using Docker volumes for the database and AI models.

## Prerequisites

- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- Docker Compose v2.0 or higher
- At least 5GB free disk space

## Setup and Run

### Step 1: Start All Services

Navigate to the project directory and run:

```bash
docker-compose up -d
```

This command builds images, creates containers, and starts all services. First-time startup takes 3-5 minutes.

### Step 2: Download AI Model

After containers start, download the required AI model:

```bash
docker exec task-breakdown-ollama ollama pull llama3.2
```

This downloads approximately 2GB and takes 3-5 minutes.

### Step 3: Access the Application

Open your browser and navigate to:
- **Web Interface**: http://localhost:5173
- **API Documentation**: http://localhost:8000/docs

## Usage

### Verify Services are Running

```bash
docker-compose ps
```

All three containers should show as running.

### View Logs

```bash
docker-compose logs -f
```

### Stop Services

```bash
docker-compose down
```

## Testing the Application

1. Open http://localhost:5173
2. Enter a task description (e.g., "Create a Python hello world program")
3. Click "Generate Step-by-Step Guide"
4. Wait 30-90 seconds for AI generation
5. View the detailed step-by-step guide

## Configuration

Environment variables are configured in `docker-compose.yml`:
- `AI_SERVICE=ollama` - Uses local Ollama service
- `OLLAMA_MODEL=llama3.2` - AI model to use
- `DATABASE_URL=sqlite:///./data/task_breakdown.db` - Database location

## Troubleshooting

### Check Service Health

```bash
curl http://localhost:8000/health
```

Expected response: `{"status":"healthy"}`

### View Specific Service Logs

```bash
docker-compose logs backend
docker-compose logs frontend
docker-compose logs ollama
```

### Restart Services

```bash
docker-compose restart
```

### Port Conflicts

If ports are already in use, modify the ports in `docker-compose.yml`:

```yaml
ports:
  - "3000:80"  # Change frontend port
```

## Docker Compose Configuration

The `docker-compose.yml` file defines:
- Three services (frontend, backend, ollama)
- A shared network for inter-container communication
- Two volumes for data persistence

### Architecture

```
Frontend (Nginx) -> Backend (FastAPI) -> Ollama (AI Service)
       |                    |
   Port 5173           Port 8000
                            |
                      SQLite Database
```

## License

MIT License

## Author

Nimra Fayaz
