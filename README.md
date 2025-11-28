# Task Breakdown Assistant

AI-powered task breakdown assistant that generates detailed, beginner-friendly step-by-step guides for complex tasks and assignments. Perfect for students, developers, and anyone tackling complex projects.

## Overview

This full-stack application helps users break down complex tasks into manageable, detailed steps with beginner-friendly instructions. It supports both software development tasks and hardware/electronics projects (ESP32, Arduino, Raspberry Pi).

### Key Features

- **AI-Powered Breakdown**: Uses Ollama (local Llama - free), Google Gemini (free tier), or OpenAI to analyze tasks
- **Extremely Detailed Instructions**: Like a personal tutor - tells you WHERE to go, WHAT to do, HOW to do it, WHAT to expect, and HOW to verify
- **Beginner-Friendly**: Each step includes specific instructions like "Press Win+R, type cmd, press Enter" with visual confirmations
- **Hardware Support**: Detailed wiring instructions for ESP32, Arduino, Raspberry Pi with pin-by-pin connections
- **OS-Specific**: Provides Windows/Mac/Linux specific instructions
- **Structured Output**: Organized format with step numbers, dependencies, time estimates, and resources
- **Persistent Storage**: Save guides to database, retrieve and reuse anytime
- **Rating System**: Community ratings to validate guide quality

## Architecture

### Tech Stack

**Backend:**
- Python 3.10+
- FastAPI (web framework)
- SQLAlchemy (ORM)
- Poetry (dependency management & packaging)
- Ollama (local Llama - FREE), Google Gemini API (free tier), or OpenAI API (paid)

**Frontend:**
- React 18
- TypeScript
- Vite (build tool)
- npm/pnpm (dependency management)

## Prerequisites

Before starting, ensure you have:

1. **Python 3.10 or higher**
   - Check: `python --version` or `python3 --version`
   - Download: https://www.python.org/downloads/

2. **Node.js 18 or higher**
   - Check: `node --version`
   - Download: https://nodejs.org/

3. **Poetry** (Python package manager)
   - Install: https://python-poetry.org/docs/#installation
   - Check: `poetry --version`

4. **AI Service** (choose one):
   - **Ollama (Recommended - FREE)**: https://ollama.com
   - **Google Gemini API (Free tier)**: https://aistudio.google.com/app/apikey
   - **OpenAI API (Paid)**: https://platform.openai.com/api-keys

## Complete Setup Guide

### Step 1: Clone/Download the Project

```bash
# If using Git
git clone <repository-url>
cd task-breakdown-assistant

# Or download and extract the ZIP file
```

### Step 2: Set Up Ollama (Recommended - FREE)

**Why Ollama?** It's completely free, runs locally, and doesn't require API keys.

1. **Download Ollama:**
   - Visit: https://ollama.com
   - Download for your OS (Windows/Mac/Linux)
   - Install the downloaded file

2. **Verify Installation:**
   ```bash
   ollama --version
   ```
   If you get "command not found", restart your terminal/PowerShell.

3. **Download the AI Model:**
   ```bash
   ollama pull llama3.2
   ```
   This downloads the Llama 3.2 model (about 2GB). Wait for it to complete.

4. **Test Ollama:**
   ```bash
   ollama run llama3.2 "Hello, how are you?"
   ```
   If it responds, Ollama is working! Press Ctrl+C to exit.

**Alternative: Using Gemini (Free API)**
- Get API key from: https://aistudio.google.com/app/apikey
- Skip to Step 3 and use Gemini configuration instead

### Step 3: Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Install Python dependencies:**
   ```bash
   poetry install
   ```
   This installs all required Python packages. Wait for it to complete.

3. **Create environment file:**
   ```bash
   # Windows PowerShell
   Copy-Item env.example .env

   # Or manually create .env file
   ```

4. **Configure environment variables:**

   Open `.env` file in a text editor and add:

   **For Ollama (Recommended - FREE):**
   ```
   AI_SERVICE=ollama
   OLLAMA_MODEL=llama3.2
   DATABASE_URL=sqlite:///./task_breakdown.db
   ```

   **For Gemini (Free tier):**
   ```
   AI_SERVICE=gemini
   GEMINI_API_KEY=your_gemini_api_key_here
   DATABASE_URL=sqlite:///./task_breakdown.db
   ```

   **For OpenAI (Paid):**
   ```
   AI_SERVICE=openai
   OPENAI_API_KEY=your_openai_api_key_here
   DATABASE_URL=sqlite:///./task_breakdown.db
   ```

5. **Start the backend server:**
   ```bash
   poetry run uvicorn task_breakdown.main:app --reload
   ```

   You should see:
   ```
   INFO:     Uvicorn running on http://127.0.0.1:8000
   INFO:     Application startup complete.
   ```

   **Keep this terminal window open!** The backend must be running.

6. **Verify backend is working:**
   - Open browser: http://localhost:8000
   - You should see: `{"message": "Task Breakdown Assistant API"}`
   - API docs: http://localhost:8000/docs

### Step 4: Frontend Setup

**Open a NEW terminal window** (keep backend running in the first one)

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install JavaScript dependencies:**
   ```bash
   npm install
   ```
   This may take a few minutes. Wait for it to complete.

3. **Start the frontend development server:**
   ```bash
   npm run dev
   ```

   You should see:
   ```
   VITE v5.x.x  ready in xxx ms
   ➜  Local:   http://localhost:5173/
   ```

4. **Open the application:**
   - Open browser: http://localhost:5173
   - You should see the Task Breakdown Assistant interface

### Step 5: Test the Application

1. **In the web interface:**
   - Enter a task description, for example:
     - "Create a simple hello world program in Python"
     - "Set up ESP32 to blink an LED"
     - "Build a web application with user authentication"

2. **Click "Generate Step-by-Step Guide"**

3. **Wait for the AI to generate the guide** (may take 10-30 seconds)

4. **Review the generated guide:**
   - Each step should have detailed instructions
   - Instructions should be beginner-friendly
   - Should include code snippets, commands, or wiring details

## Build Instructions

**For detailed build instructions, see `BUILD.md`**

### Quick Build Commands

**Backend (Python + Poetry):**
```bash
cd backend
poetry install    # Install dependencies
poetry build      # Build package (creates .whl and .tar.gz)
```

**Frontend (TypeScript + npm):**
```bash
cd frontend
npm install       # Install dependencies
npm run build     # Build for production (creates dist/ directory)
```

### Build Outputs

**Backend:**
- `dist/task_breakdown_assistant-0.1.0.tar.gz` (source distribution)
- `dist/task_breakdown_assistant-0.1.0-py3-none-any.whl` (wheel package)

**Frontend:**
- `dist/` directory with optimized production build
- Compiled TypeScript to JavaScript
- Bundled and minified assets

## Testing

### Backend Tests
```bash
cd backend
poetry run pytest
```

### Frontend Linting
```bash
cd frontend
npm run lint
```

## Usage

1. **Start both servers:**
   - Backend: `cd backend && poetry run uvicorn task_breakdown.main:app --reload`
   - Frontend: `cd frontend && npm run dev`

2. **Open the app:**
   - Navigate to http://localhost:5173

3. **Enter a task:**
   - Paste your task/assignment description
   - Examples:
     - Software: "Build a web application with user authentication"
     - Hardware: "Set up ESP32 to blink an LED with temperature sensor"
     - Mixed: "Create an IoT project with ESP32 that sends data to a web server"
   - Click "Generate Step-by-Step Guide"

4. **Follow the guide:**
   - Each step includes detailed, beginner-friendly instructions
   - For software: exact commands, file paths, code snippets
   - For hardware: pin-by-pin connections, component specs, wiring diagrams
   - Includes tips, warnings, and verification steps

5. **Rate the guide:**
   - Help improve the system by rating guides (1-5 stars)
   - Add comments to help others

## Troubleshooting

### Backend Issues

**Problem: "poetry: command not found"**
- Solution: Install Poetry from https://python-poetry.org/docs/#installation
- Restart terminal after installation

**Problem: "ModuleNotFoundError: No module named 'ollama'"**
- Solution: Run `poetry install` in the backend directory

**Problem: "Ollama server not running"**
- Solution: Make sure Ollama is installed and running
- Test with: `ollama run llama3.2 "test"`
- If it fails, restart your computer and try again

**Problem: "Error generating task breakdown: No AI service configured"**
- Solution: Check your `.env` file in the backend directory
- Make sure `AI_SERVICE=ollama` (or gemini/openai) is set
- For Ollama: Make sure `ollama pull llama3.2` completed successfully

**Problem: Backend won't start**
- Solution: Check if port 8000 is already in use
- Change port: `poetry run uvicorn task_breakdown.main:app --reload --port 8001`
- Update frontend `vite.config.ts` to use port 8001

### Frontend Issues

**Problem: "npm: command not found"**
- Solution: Install Node.js from https://nodejs.org/
- Restart terminal after installation

**Problem: "Failed to fetch" or CORS errors**
- Solution: Make sure backend is running on http://localhost:8000
- Check backend terminal for errors
- Verify `.env` file is configured correctly

**Problem: Frontend shows blank page**
- Solution: Check browser console (F12) for errors
- Make sure backend is running
- Try refreshing the page

### Ollama Issues

**Problem: "ollama: command not found"**
- Solution: Install Ollama from https://ollama.com
- Restart terminal after installation
- On Windows: May need to restart computer

**Problem: "Error: model 'llama3.2' not found"**
- Solution: Run `ollama pull llama3.2`
- Wait for download to complete (about 2GB)
- Verify with: `ollama list`

**Problem: Ollama is slow**
- Solution: This is normal for local AI
- First generation may take 30-60 seconds
- Subsequent generations are faster
- Consider using Gemini API for faster responses

### General Issues

**Problem: Can't open .env file**
- Windows: Use Notepad or VS Code
- Command: `notepad backend\.env` or `code backend\.env`
- Make sure you're in the correct directory

**Problem: Port already in use**
- Backend: Change port in command: `--port 8001`
- Frontend: Vite will automatically use next available port
- Update frontend config if backend port changes

## API Endpoints

### Tasks
- `POST /api/tasks` - Create task and generate guide
- `GET /api/tasks` - List all tasks
- `GET /api/tasks/{id}` - Get task with guide
- `DELETE /api/tasks/{id}` - Delete task

### Guides
- `GET /api/guides/{task_id}` - Get guide steps

### Ratings
- `POST /api/ratings` - Create rating
- `GET /api/ratings/{task_id}` - Get rating statistics

**Full API documentation:** http://localhost:8000/docs

### Build Tool Usage

**Dependency Management:**
- **Backend**: Poetry manages all Python dependencies in `pyproject.toml`
- **Frontend**: npm manages all JavaScript dependencies in `package.json`
- Both use lock files for reproducible builds

**Compilation:**
- **Backend**: Poetry builds Python packages (wheels and source distributions)
- **Frontend**: TypeScript compilation (`tsc`) + Vite bundling (`vite build`)

**Version Management:**
- **Backend**: Version in `pyproject.toml`, managed with `poetry version patch|minor|major`
- **Frontend**: Version in `package.json`, managed with `npm version patch|minor|major`
- Both use semantic versioning (MAJOR.MINOR.PATCH)

**Packaging:**
- **Backend**: Creates Python wheel (`.whl`) and source distribution (`.tar.gz`)
- **Frontend**: Creates optimized static web bundle in `dist/` directory

### Replicable Build

**Simple commands for full replication:**
```bash
# Backend
cd backend && poetry install && poetry build

# Frontend
cd frontend && npm install && npm run build
```

Both commands are simple, standard, and fully automated.

### Configuration Files

**`pyproject.toml`** and **`package.json`** include:
- Project metadata (name, version, description, authors, license)
- Repository information
- Keywords and classifiers
- Dependency specifications with versions
- Build system configuration
- Script definitions

## Project Structure

```
.
├── backend/                 # Python FastAPI backend
│   ├── task_breakdown/      # Main application package
│   │   ├── api/            # API routes
│   │   ├── services/       # Business logic (AI service)
│   │   ├── models.py       # Database models
│   │   ├── schemas.py      # Pydantic schemas
│   │   └── main.py         # FastAPI app
│   ├── pyproject.toml       # Poetry configuration
│   ├── env.example         # Environment variables template
│   └── .env                # Your environment variables (create this)
│
├── frontend/               # React TypeScript frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── types.ts       # TypeScript types
│   │   └── App.tsx        # Main app
│   ├── package.json       # npm configuration
│   └── vite.config.ts     # Vite configuration
│
├── README.md              # This file
└── BUILD.md               # Detailed build instructions
```

## Author

Nimra Fayaz
