# Welcome to Task Breakdown Assistant

AI-powered task breakdown assistant that generates detailed, beginner-friendly step-by-step guides for complex tasks and assignments.

## Overview

This full-stack application helps users break down complex tasks into manageable, detailed steps with beginner-friendly instructions. It supports both software development tasks and hardware/electronics projects (ESP32, Arduino, Raspberry Pi).

## Key Features

- **AI-Powered Breakdown**: Uses Ollama (local Llama - free), Google Gemini (free tier), or OpenAI to analyze tasks
- **Extremely Detailed Instructions**: Like a personal tutor - tells you WHERE to go, WHAT to do, HOW to do it, WHAT to expect, and HOW to verify
- **Beginner-Friendly**: Each step includes specific instructions like "Press Win+R, type cmd, press Enter" with visual confirmations
- **Hardware Support**: Detailed wiring instructions for ESP32, Arduino, Raspberry Pi with pin-by-pin connections
- **OS-Specific**: Provides Windows/Mac/Linux specific instructions
- **Structured Output**: Organized format with step numbers, dependencies, time estimates, and resources
- **Persistent Storage**: Save guides to database, retrieve and reuse anytime
- **Rating System**: Community ratings to validate guide quality

## Quick Start

### Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- Poetry (Python package manager)
- AI Service (Ollama, Gemini, or OpenAI)

### Installation

**Backend:**
```bash
cd backend
poetry install
poetry run uvicorn task_breakdown.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

Visit http://localhost:5173 to access the application.

## Documentation

- **[Full Documentation](DOCUMENTATION.md)** - Complete setup and usage guide
- **[Tutorials](tutorials/tutorial.md)** - Step-by-step tutorials
- **[Build Instructions](../BUILD.md)** - Build and deployment guide

## Tech Stack

**Backend:**
- Python 3.10+
- FastAPI (web framework)
- SQLAlchemy (ORM)
- Poetry (dependency management)
- Ollama / Gemini / OpenAI (AI services)

**Frontend:**
- React 18
- TypeScript
- Vite (build tool)
- npm (dependency management)

## Downloads

Get the latest release from our [GitHub Releases](https://github.com/Nimra-Fayaz/Task-Breakdown-Assistant/releases) page.

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

## Author

Nimra Fayaz
