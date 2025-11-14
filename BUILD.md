# Build Instructions

This document provides detailed instructions for building, testing, and running the Task Breakdown Assistant project. This demonstrates the build tool usage.

This project demonstrates:

**Build Tool Usage**
- **Dependency Management**: Poetry (Python) and npm (JavaScript)
- **Compilation**: TypeScript compilation and Python packaging
- **Version Management**: Semantic versioning in both build tools
- **Packaging**: Python wheels (.whl) and static web bundles

**Replicable Build**
- Simple commands: `poetry install` and `npm install`
- Fully automated dependency resolution

**Documentation**
- Clear build, test, and run instructions
- Build tool configuration details

**Configuration Files**
- Detailed metadata in `pyproject.toml` and `package.json`
- Sufficient information for external reviewers

---

## Quick Build Commands

### Backend (Python + Poetry)

**Install dependencies:**
```bash
cd backend
poetry install
```

**Build package:**
```bash
poetry build
```

This creates:
- `dist/task_breakdown_assistant-0.1.0.tar.gz` (source distribution)
- `dist/task_breakdown_assistant-0.1.0-py3-none-any.whl` (wheel package)

**Install from built package:**
```bash
pip install dist/task_breakdown_assistant-0.1.0-py3-none-any.whl
```

### Frontend (TypeScript + npm)

**Install dependencies:**
```bash
cd frontend
npm install
```

**Build for production:**
```bash
npm run build
```

This creates:
- `dist/` directory with optimized production build
- Compiled TypeScript to JavaScript
- Bundled and minified assets

---

## Build Tool Configuration Details

### Backend: Poetry (`pyproject.toml`)

**Dependency Management:**
- All Python dependencies defined in `[tool.poetry.dependencies]`
- Development dependencies in `[tool.poetry.group.dev.dependencies]`
- Automatic dependency resolution and lock file (`poetry.lock`)

**Version Management:**
- Version specified in `[tool.poetry]` section: `version = "0.1.0"`
- Update with: `poetry version patch|minor|major`
- Semantic versioning (MAJOR.MINOR.PATCH)

**Packaging:**
- Build system: `poetry-core`
- Package metadata includes:
  - Name, version, description
  - Authors, license, homepage
  - Keywords, classifiers
  - Repository URL

**Compilation:**
- Python package structure defined in `packages = [{include = "task_breakdown"}]`
- Builds both source distribution (`.tar.gz`) and wheel (`.whl`)

### Frontend: npm (`package.json`)

**Dependency Management:**
- Production dependencies in `dependencies`
- Development dependencies in `devDependencies`
- Automatic dependency resolution via `package-lock.json`

**Version Management:**
- Version in `package.json`: `"version": "0.1.0"`
- Update with: `npm version patch|minor|major`
- Semantic versioning (MAJOR.MINOR.PATCH)

**Compilation:**
- TypeScript compilation: `tsc` (via `npm run build`)
- Vite bundling: `vite build`
- Build script: `"build": "tsc && vite build"`

**Packaging:**
- Builds static web application bundle
- Optimized for production (minification, tree-shaking)
- Ready for deployment to static hosting

---

## Testing

### Backend Tests

**Run tests:**
```bash
cd backend
poetry run pytest
```

**Run with coverage:**
```bash
poetry run pytest --cov=task_breakdown
```

### Frontend Tests

**Run linter:**
```bash
cd frontend
npm run lint
```

**Type checking:**
```bash
npm run build  # Includes TypeScript compilation
```

---

## Running the Application

### Development Mode

**Backend:**
```bash
cd backend
poetry install
poetry run uvicorn task_breakdown.main:app --reload
```

**Access:** http://localhost:8000
**API Docs:** http://localhost:8000/docs

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

**Access:** http://localhost:5173

### Production Mode

**Backend:**
```bash
cd backend
poetry install
poetry build
pip install dist/task_breakdown_assistant-0.1.0-py3-none-any.whl
uvicorn task_breakdown.main:app --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run build
# Serve dist/ directory with any static file server
# Example: npx serve dist
```

---

## Build Tool Metadata

### Backend (`pyproject.toml`)

**Project Metadata:**
- **Name**: `task-breakdown-assistant`
- **Version**: `0.1.0`
- **Description**: AI-powered task breakdown assistant with beginner-friendly detailed guides
- **Authors**: Nimra Fayaz
- **License**: MIT
- **Homepage**: https://github.com/Nimra-Fayaz/Task-Breakdown-Assistant
- **Repository**: https://github.com/Nimra-Fayaz/Task-Breakdown-Assistant
- **Keywords**: task-breakdown, ai, fastapi, guide, tutorial
- **Classifiers**: Development status, audience, license, Python versions, topics

**Dependencies:**
- Production: FastAPI, Uvicorn, SQLAlchemy, Pydantic, etc.
- Development: pytest, black, ruff

### Frontend (`package.json`)

**Project Metadata:**
- **Name**: `task-breakdown-frontend`
- **Version**: `0.1.0`
- **Description**: Frontend for Task Breakdown Assistant
- **Author**: Nimra Fayaz
- **License**: MIT
- **Keywords**: react, typescript, vite, task-breakdown, ai, frontend

**Dependencies:**
- Production: React, React DOM, Axios, React Router
- Development: TypeScript, Vite, ESLint, TypeScript ESLint plugins

---

## Related Documentation

- **Main README**: See `README.md` for project overview and complete setup instructions

