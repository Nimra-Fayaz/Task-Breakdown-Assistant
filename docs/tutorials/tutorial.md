# Task Breakdown Assistant Tutorial

## Introduction

This tutorial will guide you through using the Task Breakdown Assistant to generate detailed, beginner-friendly guides for complex tasks. Whether you're learning programming, working on hardware projects, or tackling any complex assignment, this tool breaks down tasks into manageable step-by-step instructions.

## Prerequisites

Before starting, ensure you have:

- Python 3.10 or higher
- Node.js 18 or higher
- Poetry (Python package manager)
- Ollama installed (or API keys for Gemini/OpenAI)
- Basic command-line knowledge

## Step 1: Installation

### Backend Setup

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

3. Configure environment variables:
   ```bash
   # Windows PowerShell
   Copy-Item env.example .env

   # Linux/Mac
   cp env.example .env
   ```

4. Edit the `.env` file and add your configuration:
   ```
   AI_SERVICE=ollama
   OLLAMA_MODEL=llama3.2
   DATABASE_URL=sqlite:///./task_breakdown.db
   ```

### Frontend Setup

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install npm dependencies:
   ```bash
   npm install
   ```

## Step 2: Starting the Application

### Start Backend Server

Open a terminal and run:
```bash
cd backend
poetry run uvicorn task_breakdown.main:app --reload
```

You should see output similar to:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

**Keep this terminal open!** The backend must be running for the application to work.

### Start Frontend Server

Open a **new terminal** (don't close the backend terminal) and run:
```bash
cd frontend
npm run dev
```

You should see:
```
VITE v5.x.x  ready in xxx ms
➜  Local:   http://localhost:5173/
```

**Your application is now running!** Open http://localhost:5173 in your browser.

## Step 3: Using the Application

### Example 1: Creating a Simple Python Program

1. Open http://localhost:5173 in your browser
2. In the task input field, enter:
   ```
   Create a hello world program in Python
   ```
3. Click the **"Generate Step-by-Step Guide"** button
4. Wait for the AI to generate the guide (typically 10-30 seconds)
5. Review the generated steps which will include:
   - **Step 1**: Install Python (if not installed)
   - **Step 2**: Create a new Python file
   - **Step 3**: Write the hello world code
   - **Step 4**: Run the program
   - **Step 5**: Verify the output

Each step includes:
- Detailed instructions
- Code snippets with syntax highlighting
- Expected results
- Verification steps to ensure success

### Example 2: Setting Up ESP32 Hardware Project

1. Enter this task description:
   ```
   Set up ESP32 to blink an LED connected to GPIO pin 2
   ```
2. Click **"Generate Step-by-Step Guide"**
3. The generated guide will include:
   - Complete hardware requirements list
   - Pin-by-pin wiring instructions with diagrams descriptions
   - Arduino IDE setup and configuration
   - Complete code with line-by-line explanations
   - Step-by-step upload instructions
   - Common troubleshooting tips

After following a guide, you can rate it to help improve the system:

1. Scroll to the bottom of the guide display
2. Select a rating from 1 to 5 stars:
   - 1 star: Poor, not helpful
   - 2 stars: Below average
   - 3 stars: Average, somewhat helpful
   - 4 stars: Good, very helpful
   - 5 stars: Excellent, extremely helpful
3. Click **"Submit Rating"**

Your ratings help identify high-quality guides and improve the AI's future outputs!

## Step 4: Advanced Usage

### Using Different AI Services

The application supports three AI services:

**Ollama (Local, Free - Recommended for Beginners):**
- No API keys needed
- Runs completely locally on your computer
- Completely free forever
- Best for privacy and learning
- Slower than cloud services

**Gemini (Free Tier Available):**
- Faster responses than Ollama
- Good quality outputs
- Free tier with generous limits
- Requires API key from https://aistudio.google.com/app/apikey
- Limited free requests per day

**OpenAI (Paid):**
- Fastest responses
- Highest quality outputs
- Requires API key from https://platform.openai.com/api-keys
- Requires payment

**To switch AI services**, update your `.env` file:

For Gemini:
```bash
AI_SERVICE=gemini
GEMINI_API_KEY=your_api_key_here
```

For OpenAI:
```bash
AI_SERVICE=openai
OPENAI_API_KEY=your_api_key_here
```

Then restart the backend server.

### Using the REST API Directly

You can also use the application's REST API without the frontend:

**Create a task and get a guide:**
```bash
curl -X POST "http://localhost:8000/api/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Task",
    "description": "Create a REST API with FastAPI"
  }'
```

**Get task with guide steps:**
```bash
curl "http://localhost:8000/api/tasks/1"
```

**Get only guide steps:**
```bash
curl "http://localhost:8000/api/guides/1"
```

**Create a rating:**
```bash
curl -X POST "http://localhost:8000/api/ratings/" \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": 1,
    "rating": 5,
    "comment": "Great guide! Very detailed and easy to follow."
  }'
```

**Get rating statistics:**
```bash
curl "http://localhost:8000/api/ratings/1"
```

**Explore interactive API documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Troubleshooting

### Backend Won't Start

**Problem**: Port 8000 already in use
```
OSError: [Errno 48] error while attempting to bind on address
```
**Solution**: Change to a different port:
```bash
poetry run uvicorn task_breakdown.main:app --reload --port 8001
```
Then update your frontend API URL accordingly.

**Problem**: Module not found errors
```
ModuleNotFoundError: No module named 'fastapi'
```
**Solution**: Install dependencies:
```bash
cd backend
poetry install
```

**Problem**: Database errors
```
sqlalchemy.exc.OperationalError
```
**Solution**:
1. Check `.env` file has correct DATABASE_URL
2. Delete `task_breakdown.db` if corrupted and restart

### Frontend Shows Errors

**Problem**: "Failed to fetch" or CORS errors in browser console
**Solution**:
1. Ensure backend is running on http://localhost:8000
2. Check backend terminal for errors
3. Verify CORS is enabled in `main.py`

**Problem**: Blank page or white screen
**Solution**:
1. Open browser console (press F12)
2. Check for JavaScript errors
3. Verify backend is running and accessible
4. Try hard refresh (Ctrl+Shift+R or Cmd+Shift+R)

**Problem**: npm install fails
**Solution**:
1. Delete `node_modules` folder and `package-lock.json`
2. Run `npm install` again
3. Ensure Node.js version is 18 or higher: `node --version`

### AI Service Not Working

**Problem**: Ollama not responding
```
Error: Failed to connect to Ollama
```
**Solution**:
1. Verify Ollama is installed: `ollama --version`
2. Test Ollama directly: `ollama run llama3.2 "test"`
3. Restart Ollama service if needed
4. Check Ollama is running: `ollama list`

**Problem**: Gemini/OpenAI API errors
```
Error: Invalid API key
```
**Solution**:
1. Verify API key is correctly set in `.env` file
2. Check for extra spaces or quotes around the key
3. Ensure API key is active and valid
4. Check you have credits/quota available

**Problem**: AI generates incomplete guides
**Solution**:
1. Try a more specific task description
2. Break complex tasks into smaller sub-tasks
3. Switch to a different AI service (e.g., OpenAI)

## Best Practices

### Writing Good Task Descriptions

1. **Be specific and detailed**:
   - Good: "Create a REST API with FastAPI that handles user authentication using JWT tokens and stores data in PostgreSQL"
   - Bad: "Make an API"

2. **Include technology preferences**:
   - Good: "Build a React frontend with TypeScript and Tailwind CSS"
   - Bad: "Build a website"

3. **Mention your skill level if relevant**:
   - Good: "Explain how to deploy a Flask app to Heroku for beginners"
   - Bad: "Deploy Flask app"

### Following Guides Effectively

1. **Follow steps in order**: Steps may have dependencies on previous ones
2. **Read completely before starting**: Understand the full process
3. **Verify each step**: Use the verification steps provided
4. **Don't skip prerequisites**: They're included for a reason
5. **Rate guides**: Help improve the system for everyone

### Managing Your Tasks

1. **Save important task IDs**: Use them to retrieve guides later
2. **Use the API**: Integrate with your own workflows
3. **Export guides**: Copy the text for offline reference
4. **Rate after completing**: Share your experience

## Tips for Different Use Cases

### For Students
- Use detailed assignment descriptions
- Break large projects into smaller tasks
- Rate guides to help fellow students
- Use Ollama (free) for unlimited learning

### For Developers
- Get quick setup guides for new technologies
- Generate boilerplate code explanations
- Use API integration for automation
- Switch to OpenAI for highest quality

### For Hardware Projects
- Include specific component names and models
- Mention pin numbers and connections
- Specify voltage requirements
- Rate hardware guides to improve accuracy

## Next Steps

Now that you know how to use the Task Breakdown Assistant:

1. **Explore the API documentation**: Visit http://localhost:8000/docs
2. **Try different task types**: Software, hardware, mixed projects
3. **Experiment with AI services**: Compare Ollama, Gemini, and OpenAI
4. **Rate guides you use**: Help improve the system
5. **Contribute on GitHub**: Report issues or suggest features

## Conclusion

The Task Breakdown Assistant transforms complex tasks into manageable, step-by-step instructions. Whether you're a student learning new concepts, a developer exploring new technologies, or a maker working on hardware projects, this tool provides the detailed guidance you need to succeed.

The AI-powered breakdowns ensure you never feel lost or overwhelmed—every step is explained in detail, with verification checks and expected outcomes.

**Happy learning and building!**

---

**Need help?**
- API Docs: http://localhost:8000/docs
- GitHub Issues: https://github.com/Nimra-Fayaz/Task-Breakdown-Assistant/issues
- Check logs: `backend/app.log`
