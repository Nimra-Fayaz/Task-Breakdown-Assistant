"""AI service for generating detailed task breakdowns."""

import os
import json
import requests
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

# Try to import OpenAI (optional)
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Try to import Google Gemini (optional)
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

# Determine which AI service to use
# Options: "ollama" (local, free), "gemini" (free tier), "openai" (paid)
AI_SERVICE = os.getenv("AI_SERVICE", "ollama").lower()  # Default to Ollama (local, free)

# Initialize clients
openai_client = None
gemini_model = None
ollama_client = None
ollama_model_name = os.getenv("OLLAMA_MODEL", "llama3.2")  # Default to llama3.2

# Function to check Ollama availability dynamically
def check_ollama_available():
    """Check if Ollama package and server are available."""
    try:
        import ollama
        # Test if Ollama server is running
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=3)
            if response.status_code == 200:
                # Check if llama3.2 model is available
                models = response.json().get('models', [])
                model_names = [m.get('name', '') for m in models]
                has_model = any('llama3.2' in name for name in model_names)
                if has_model:
                    return True, ollama
                else:
                    print("Warning: llama3.2 model not found. Run: ollama pull llama3.2")
                    return False, None
            else:
                return False, None
        except requests.exceptions.RequestException as e:
            print(f"Ollama server not accessible: {e}")
            return False, None
    except ImportError:
        print("Warning: ollama Python package not installed. Run: poetry install")
        return False, None

# Initialize Ollama if it's the selected service
if AI_SERVICE == "ollama":
    OLLAMA_AVAILABLE, ollama_module = check_ollama_available()
    if OLLAMA_AVAILABLE and ollama_module:
        ollama = ollama_module  # Make it available globally
        ollama_client = True
        print(f"Ollama client initialized (using model: {ollama_model_name})")
    else:
        ollama_client = None
        if not OLLAMA_AVAILABLE:
            print("Warning: ollama package not installed. Run: poetry install")
        else:
            print("Warning: Ollama server not running. Install from https://ollama.com and run: ollama serve")
    OLLAMA_AVAILABLE = OLLAMA_AVAILABLE  # Set the flag
elif AI_SERVICE == "openai" and OPENAI_AVAILABLE:
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key:
        openai_client = OpenAI(api_key=openai_api_key)
        print("OpenAI client initialized")
elif AI_SERVICE == "gemini" and GEMINI_AVAILABLE:
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if gemini_api_key:
        try:
            # Configure API key
            genai.configure(api_key=gemini_api_key)
            # Initialize model (using gemini-1.5-flash which is stable and free)
            gemini_model = genai.GenerativeModel('gemini-1.5-flash')
            print(f"Gemini client initialized successfully (API key length: {len(gemini_api_key)})")
        except Exception as e:
            print(f"Failed to initialize Gemini client: {e}")
            gemini_model = None
    else:
        print("GEMINI_API_KEY not found in environment variables")
        gemini_model = None
else:
    if AI_SERVICE == "gemini" and not GEMINI_AVAILABLE:
        print("Warning: google-generativeai package not installed. Run: poetry install")
    if AI_SERVICE == "ollama" and not OLLAMA_AVAILABLE:
        print("Warning: ollama package not installed. Run: poetry add ollama")


def generate_task_breakdown(task_description: str) -> Dict:
    """
    Generate a detailed, beginner-friendly task breakdown using AI.
    
    Args:
        task_description: The task/assignment description
        
    Returns:
        Dictionary with task metadata and guide steps
    """
    
    prompt = f"""You are an expert task breakdown assistant. Your job is to break down complex tasks into EXTREMELY DETAILED, beginner-friendly step-by-step guides. You handle BOTH software AND hardware/electronics tasks.

CRITICAL: You MUST stay focused on the EXACT task described. If the task is about Python, use Python. If it's about Node.js, use Node.js. If it's about hardware, focus on hardware. DO NOT mix technologies or create steps for different technologies than what was requested.

IMPORTANT: Provide the SAME level of detail as a personal tutor guiding someone step-by-step. Assume the user knows NOTHING and needs to be told:
- WHERE to go (exact locations, menus, buttons)
- WHAT to do (specific actions, clicks, commands)
- HOW to do it (exact steps, keyboard shortcuts, mouse clicks)
- WHAT to expect (exact output, visual confirmation)
- HOW to verify (check this, see that, confirm this)

Task Description: {task_description}

Given the task description above, create a comprehensive breakdown that DIRECTLY addresses this specific task. Use ONLY the technologies, tools, and languages mentioned in the task description. Do NOT add steps for unrelated technologies.

Requirements:

1. Each step must be EXTREMELY DETAILED and BEGINNER-FRIENDLY
   - Include OS-specific instructions (Windows: "Press Win+R", Mac: "Press Cmd+Space")
   - Include exact locations: "Click the Start button (bottom left)", "Open File menu (top left)"
   - Include exact actions: "Type this command", "Press Enter", "Click OK button"
   - Include visual confirmations: "You should see a black window", "A file named X should appear"

2. For SOFTWARE tasks: Include specific actions like:
   - "Open your terminal: Press Win+R (Windows), type 'cmd', press Enter"
   - "You should see: A black window with text like C:\\Users\\YourName>"
   - "Type this exact command: npm init -y"
   - "Press Enter"
   - "You should see: 'Wrote to package.json'"
   - "Navigate to folder: Type 'cd Desktop' and press Enter"
   - "Create a file called X: Right-click in folder, select 'New' > 'Text Document', rename to X"

3. For HARDWARE/ELECTRONICS tasks: Include specific physical actions like:
   - "Take the ESP32 board and locate pin X (it's labeled on the board, look for '3V3' text)"
   - "Connect the red wire from the sensor to pin 3V3 on the ESP32 (the pin is on the left side, third pin from top)"
   - "Insert the USB cable into the micro-USB port on the ESP32 (the port is on the side, looks like a small rectangle)"
   - "Make sure the LED is connected to GPIO pin 2 (count pins from left: GND, GPIO0, GPIO2 - use GPIO2)"
   - Include exact pin numbers, wire colors, connection points, physical locations
   - Describe physical orientation: "LED long leg (anode, positive) goes to GPIO pin 2, short leg (cathode, negative) goes to GND via 220Ω resistor"
   - Include visual descriptions: "The pin is labeled '3V3' in small white text", "The LED has two legs, one is longer"

4. Provide exact file paths, commands, code snippets (for software)
   - Full paths: "C:\\Users\\YourName\\Desktop\\my-project"
   - Exact commands: "python --version" (not "check python version")
   - Complete code blocks with line numbers

5. Provide wiring diagrams in text form, pin connections, component specifications (for hardware)
   - Text-based wiring: "ESP32 3V3 → DHT22 VCC (red wire)"
   - Pin specifications: "GPIO pin 4 (physical pin 4, labeled 'GPIO4' on board)"
   - Component specs: "220Ω resistor (red-red-brown bands)"

6. Include verification steps with exact expectations:
   - "You should see: 'Python 3.10.5' in the terminal"
   - "Check that: A file named 'package.json' appears in your folder"
   - "LED should blink: You'll see it turn on and off every second"
   - "Serial monitor shows: 'Temperature: 25.3°C' scrolling on screen"

7. Include troubleshooting tips and common errors:
   - "If you see 'command not found': Make sure Python is installed and added to PATH"
   - "If LED doesn't blink: Check wire connections, make sure LED polarity is correct (long leg to positive)"
   - "If port not found: Unplug and replug USB cable, check Device Manager"

8. Include safety warnings for hardware (voltage, polarity, etc.):
   - "WARNING: Never connect more than 3.3V to ESP32 GPIO pins"
   - "CAUTION: Check LED polarity - wrong connection can damage the LED"
   - "IMPORTANT: Always disconnect power before changing connections"

9. Estimate time for each step (be realistic)

10. Identify dependencies between steps:
    - "This step requires Step 1 to be completed first"
    - "You must finish Step 2 before starting Step 3"

REMINDER: The task is: {task_description}
Stay focused on this exact task. Use only the technologies mentioned in the task description.

Provide your response as a JSON object with this exact structure:
{{
    "title": "Brief title for the task",
    "complexity_score": <number 1-10>,
    "estimated_total_time": <total minutes>,
    "steps": [
        {{
            "step_number": 1,
            "title": "Step title",
            "description": "Brief description",
            "detailed_instructions": "EXTREMELY DETAILED instructions like a personal tutor. For SOFTWARE: Include OS-specific steps like '1. Open Command Prompt: Press Win+R (Windows key + R together), type 'cmd', press Enter. You should see a black window. 2. Navigate to folder: Type 'cd Desktop' and press Enter. You should see the prompt change to show Desktop path. 3. Type exact command: 'npm init -y' (type exactly as shown, including the dash and y), press Enter. 4. You should see: 'Wrote to package.json' message. 5. Verify: Type 'dir' and press Enter, you should see package.json in the list.' For HARDWARE: Include physical details like '1. Take the ESP32 board in your hand. Look at the board - you'll see pins along the edges with labels. 2. Locate the 3V3 pin: It's labeled '3V3' in small white text, usually on the left side of the board, third pin from the top. 3. Take a red jumper wire: Pick up a red wire (red indicates positive/voltage). 4. Connect one end: Insert one end of the red wire into the breadboard hole next to the 3V3 pin (or directly to the pin if using a breakout board). 5. Connect LED: Take an LED - notice it has two legs, one longer than the other. The longer leg is positive (anode). Connect the red wire to the LED's longer leg. 6. Add resistor: Take a 220Ω resistor (you can identify it by the colored bands: red-red-brown). Connect one end of the resistor to the LED's shorter leg (negative/cathode). 7. Connect to GPIO: Connect the other end of the resistor to GPIO pin 2 on the ESP32 (count pins: GND is pin 1, GPIO0 is pin 2, GPIO2 is pin 3 - use GPIO2 which is pin 3). 8. Connect GND: Take a black wire, connect one end to GND pin on ESP32, other end to the resistor/LED junction. 9. Verify connections: Double-check all connections are secure, no loose wires. 10. Power on: Connect USB cable to ESP32 - you should see a small LED on the board light up, indicating power.' Make it so a complete beginner with zero knowledge can follow every single step.",
            "estimated_time": <minutes>,
            "dependencies": [<step numbers this depends on>],
            "resources": ["URL or resource name"],
            "code_snippets": ["code example 1", "code example 2"],
            "tips": "Helpful tips for this step",
            "warnings": "Common mistakes or warnings",
            "verification_steps": "How to verify this step is complete (e.g., 'You should see a file named package.json in your folder')"
        }}
    ]
}}

Make sure the detailed_instructions are extremely detailed and beginner-friendly. Assume the user knows nothing about programming or the tools involved."""

    try:
        # Use Ollama (local, free), Gemini (free tier), or OpenAI (paid) based on configuration
        # Re-check Ollama availability at runtime
        if AI_SERVICE == "ollama":
            OLLAMA_AVAILABLE, ollama_module = check_ollama_available()
            if OLLAMA_AVAILABLE and ollama_module:
                ollama = ollama_module
                ollama_client = True
        
        if AI_SERVICE == "ollama" and ollama_client:
            print("Calling Ollama (local Llama) API...")  # Debug log
            full_prompt = f"""You are an expert personal tutor who breaks down complex tasks into EXTREMELY DETAILED, beginner-friendly step-by-step guides.

🚨 CRITICAL RULE - READ THIS FIRST: 
The user asked for: "{task_description}"
You MUST create steps ONLY for this exact task. 
- If they ask for Python → use Python commands, Python files (.py), Python syntax
- If they ask for Node.js → use Node.js commands, npm, package.json
- If they ask for hardware → use hardware components, wiring, pins
DO NOT mix technologies. DO NOT add steps for technologies not mentioned in the task.

Your instructions should be like guiding someone in person - tell them WHERE to go (exact locations, menus, buttons), WHAT to do (specific actions, clicks, commands), HOW to do it (exact steps, keyboard shortcuts), WHAT to expect (exact output, visual confirmation), and HOW to verify (check this, see that). 

For hardware tasks, provide detailed wiring instructions with exact pin numbers, wire colors, physical locations on the board, component specifications, and physical setup steps. 

For software tasks, include OS-specific instructions (Windows/Mac/Linux), exact commands, file paths, and visual confirmations. Use ONLY the programming language, framework, or tool mentioned in the task description.

Always assume the user knows NOTHING and needs to be told every single detail - like explaining to someone who has never used a computer before. Include visual descriptions, exact button locations, keyboard shortcuts, and what they should see at each step.

REMEMBER: The task is "{task_description}". Stay focused on this exact task only.

{prompt}

CRITICAL: You MUST respond with ONLY valid JSON. No markdown, no code blocks, no explanations, no text before or after. Start with {{ and end with }}.

IMPORTANT JSON RULES:
- Use double quotes for all strings: "text" not 'text'
- Escape quotes inside strings: "He said \"hello\""
- Use \\ for backslash, \\n for newline, \\t for tab
- Do NOT use single quotes or backticks in strings
- Do NOT use invalid escape sequences

Your response must be valid JSON in this EXACT format:
{{
    "title": "Brief title for the task",
    "complexity_score": 5,
    "estimated_total_time": 60,
    "steps": [
        {{
            "step_number": 1,
            "title": "Step title",
            "description": "Brief description",
            "detailed_instructions": "EXTREMELY DETAILED instructions. Use \\n for newlines, escape quotes with \\\"",
            "estimated_time": 10,
            "dependencies": [],
            "resources": [],
            "code_snippets": [],
            "tips": "Helpful tips",
            "warnings": null,
            "verification_steps": "How to verify"
        }}
    ]
}}

Remember: Start your response with {{ and end with }}. Use only valid JSON escape sequences.

CRITICAL FORMAT RULES:
- code_snippets must be an array of STRINGS: ["npm init -y", "git clone url"]
- Do NOT use objects: [{{"language": "bash", "code": "npm init -y"}}] is WRONG
- dependencies must be array of integers: [1, 2] not ["1", "2"]
- resources must be array of strings: ["https://example.com"]"""
            
            try:
                # Use generate with timeout options
                response = ollama.generate(
                    model=ollama_model_name, 
                    prompt=full_prompt,
                    options={'num_predict': 4000}  # Increased for better JSON generation
                )
                content = response['response']
                print("Ollama API call successful")  # Debug log
            except Exception as ollama_error:
                error_str = str(ollama_error)
                print(f"Ollama error: {error_str}")
                raise Exception(f"Ollama API error: {error_str[:200]}. Make sure Ollama is running: install from https://ollama.com and run 'ollama serve'")
        
        elif AI_SERVICE == "gemini" and gemini_model:
            print("Calling Google Gemini API (free)...")  # Debug log
            full_prompt = f"""You are an expert personal tutor who breaks down complex tasks into EXTREMELY DETAILED, beginner-friendly step-by-step guides. You handle both software development tasks AND hardware/electronics tasks (like ESP32, Arduino, Raspberry Pi, sensors, LEDs, etc.). Your instructions should be like guiding someone in person - tell them WHERE to go (exact locations, menus, buttons), WHAT to do (specific actions, clicks, commands), HOW to do it (exact steps, keyboard shortcuts), WHAT to expect (exact output, visual confirmation), and HOW to verify (check this, see that). For hardware tasks, provide detailed wiring instructions with exact pin numbers, wire colors, physical locations on the board, component specifications, and physical setup steps. For software tasks, include OS-specific instructions (Windows/Mac/Linux), exact commands, file paths, and visual confirmations. Always assume the user knows NOTHING and needs to be told every single detail - like explaining to someone who has never used a computer before. Include visual descriptions, exact button locations, keyboard shortcuts, and what they should see at each step.

{prompt}"""
            
            try:
                # Use gemini-1.5-flash (stable and free)
                response = gemini_model.generate_content(full_prompt)
                content = response.text
                print("Gemini API call successful")  # Debug log
            except Exception as model_error:
                # If model fails, try gemini-1.5-pro as fallback
                error_str = str(model_error)
                print(f"Model error: {error_str}. Trying gemini-1.5-pro...")
                
                try:
                    fallback_model = genai.GenerativeModel('gemini-1.5-pro')
                    response = fallback_model.generate_content(full_prompt)
                    content = response.text
                    print("Gemini API call successful (using gemini-1.5-pro)")
                except Exception as fallback_error:
                    error_str = str(fallback_error)
                    # Check if it's an API key error
                    if "api key" in error_str.lower() or "invalid" in error_str.lower() or "401" in error_str or "403" in error_str:
                        raise Exception(f"Invalid or unauthorized Gemini API key. Please check your API key at https://aistudio.google.com/app/apikey. Error: {error_str[:200]}")
                    raise Exception(f"Gemini API error: {error_str[:200]}. Please check Google AI Studio at https://aistudio.google.com/app/apikey")
            
        elif AI_SERVICE == "openai" and openai_client:
            print("Calling OpenAI API...")  # Debug log
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",  # Using cheaper model, can upgrade to gpt-4 if needed
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert personal tutor who breaks down complex tasks into EXTREMELY DETAILED, beginner-friendly step-by-step guides. You handle both software development tasks AND hardware/electronics tasks (like ESP32, Arduino, Raspberry Pi, sensors, LEDs, etc.). Your instructions should be like guiding someone in person - tell them WHERE to go (exact locations, menus, buttons), WHAT to do (specific actions, clicks, commands), HOW to do it (exact steps, keyboard shortcuts), WHAT to expect (exact output, visual confirmation), and HOW to verify (check this, see that). For hardware tasks, provide detailed wiring instructions with exact pin numbers, wire colors, physical locations on the board, component specifications, and physical setup steps. For software tasks, include OS-specific instructions (Windows/Mac/Linux), exact commands, file paths, and visual confirmations. Always assume the user knows NOTHING and needs to be told every single detail - like explaining to someone who has never used a computer before. Include visual descriptions, exact button locations, keyboard shortcuts, and what they should see at each step."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=4000
            )
            print("OpenAI API call successful")  # Debug log
            content = response.choices[0].message.content
        else:
            # Provide detailed error message with installation instructions
            error_details = []
            installation_help = ""
            
            if AI_SERVICE == "ollama":
                # Re-check at runtime
                OLLAMA_AVAILABLE_RT, ollama_module_rt = check_ollama_available()
                
                if not OLLAMA_AVAILABLE_RT:
                    # Check if it's package or server issue
                    try:
                        import ollama
                        # Package is available, but server isn't
                        error_details.append("Ollama server not running")
                        installation_help = "\n\n📋 TO FIX:\n1. Install Ollama from https://ollama.com\n2. Close and reopen PowerShell\n3. Run: ollama pull llama3.2\n4. Restart backend server"
                    except ImportError:
                        error_details.append("ollama Python package not installed")
                        installation_help = "\n\n📋 TO FIX: Run 'poetry install' in the backend folder"
                else:
                    error_details.append("Ollama initialization failed (check server logs)")
                    installation_help = "\n\n📋 TO FIX: Check that Ollama server is running and llama3.2 model is downloaded"
                    
            elif AI_SERVICE == "gemini":
                if not GEMINI_AVAILABLE:
                    error_details.append("google-generativeai package not installed (run: poetry install)")
                if not os.getenv("GEMINI_API_KEY"):
                    error_details.append("GEMINI_API_KEY not found in .env file")
                    installation_help = "\n\n📋 TO FIX: Get free API key from https://aistudio.google.com/app/apikey and add to .env"
                if GEMINI_AVAILABLE and os.getenv("GEMINI_API_KEY") and not gemini_model:
                    error_details.append("Failed to initialize Gemini model (check API key)")
            elif AI_SERVICE == "openai":
                if not OPENAI_AVAILABLE:
                    error_details.append("openai package not installed")
                if not os.getenv("OPENAI_API_KEY"):
                    error_details.append("OPENAI_API_KEY not found in .env file")
                    installation_help = "\n\n📋 TO FIX: Get API key from https://platform.openai.com/api-keys and add to .env"
            
            error_msg = "No AI service configured. "
            if error_details:
                error_msg += "Issues: " + "; ".join(error_details)
            else:
                error_msg += f"Please set {AI_SERVICE.upper()}_API_KEY in .env file"
            
            error_msg += installation_help
            
            raise Exception(error_msg)
        
        # Try to extract JSON from the response
        # Sometimes AI wraps JSON in markdown code blocks
        original_content = content
        
        # Remove markdown code blocks
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            # Try to find JSON between code blocks
            parts = content.split("```")
            for i, part in enumerate(parts):
                part = part.strip()
                if part.startswith("{") and "title" in part:
                    content = part
                    break
            else:
                # If no JSON found, try the first part that looks like JSON
                for part in parts:
                    part = part.strip()
                    if part.startswith("{"):
                        content = part
                        break
        
        # Try to find JSON object in the content
        if not content.startswith("{"):
            # Find the first { and last }
            start_idx = content.find("{")
            end_idx = content.rfind("}")
            if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                content = content[start_idx:end_idx+1]
        
        # Clean up common issues
        content = content.strip()
        # Remove any leading/trailing whitespace or newlines
        content = content.lstrip().rstrip()
        
        # Try to parse JSON
        try:
            result = json.loads(content)
            # Validate the result has required fields
            if "title" not in result or "steps" not in result:
                raise json.JSONDecodeError("Missing required fields", content, 0)
            return result
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {str(e)}")  # Debug log
            print(f"Response content (first 1000 chars): {original_content[:1000]}")  # Debug log
            print(f"Extracted content (first 500 chars): {content[:500]}")  # Debug log
            
            # Try to fix common JSON issues and retry
            try:
                import re
                content_fixed = content
                
                # Fix trailing commas
                content_fixed = re.sub(r',\s*}', '}', content_fixed)
                content_fixed = re.sub(r',\s*]', ']', content_fixed)
                
                # Fix invalid escape sequences (common issue: \ followed by non-escape char)
                # Replace invalid escapes with valid ones or remove them
                # But be careful not to break valid escapes like \n, \t, etc.
                def fix_escapes(text):
                    # Find all backslashes that are not part of valid escape sequences
                    # Valid escapes: \\, \", \/, \b, \f, \n, \r, \t, \uXXXX
                    result = []
                    i = 0
                    while i < len(text):
                        if text[i] == '\\':
                            if i + 1 < len(text):
                                next_char = text[i + 1]
                                # Valid escape sequences (single char)
                                if next_char in ['\\', '"', '/', 'b', 'f', 'n', 'r', 't']:
                                    result.append(text[i:i+2])
                                    i += 2
                                # Unicode escape sequence \uXXXX
                                elif next_char == 'u' and i + 5 < len(text):
                                    # Check if it's a valid unicode escape
                                    try:
                                        unicode_val = text[i+2:i+6]
                                        int(unicode_val, 16)  # Validate hex
                                        result.append(text[i:i+6])
                                        i += 6
                                    except:
                                        # Invalid unicode - remove backslash
                                        result.append(next_char)
                                        i += 2
                                # Invalid escape - escape the backslash or remove it
                                elif next_char in ['\'', '`']:
                                    # Common issue: \' or \` in strings - just remove the backslash
                                    result.append(next_char)
                                    i += 2
                                else:
                                    # Invalid escape - remove the backslash
                                    result.append(next_char)
                                    i += 2
                            else:
                                # Backslash at end - remove it
                                i += 1
                        else:
                            result.append(text[i])
                            i += 1
                    return ''.join(result)
                
                content_fixed = fix_escapes(content_fixed)
                
                # Try parsing again
                result = json.loads(content_fixed)
                if "title" not in result or "steps" not in result:
                    raise json.JSONDecodeError("Missing required fields", content_fixed, 0)
                print("✅ JSON fixed and parsed successfully!")
                return result
            except Exception as fix_error:
                print(f"JSON fix attempt failed: {str(fix_error)[:200]}")
                pass
            
            # If all else fails, raise an error instead of returning fallback
            raise Exception(f"Failed to parse AI response as JSON. The AI may have generated invalid JSON. Error: {str(e)[:200]}. Please try generating the guide again.")
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        error_str = str(e)
        
        # Check for specific API errors
        if "insufficient_quota" in error_str or "429" in error_str or "quota" in error_str.lower():
            if AI_SERVICE == "openai":
                raise Exception("OpenAI API quota exceeded. Switch to Gemini (free) by setting AI_SERVICE=gemini in .env and adding GEMINI_API_KEY")
            else:
                raise Exception("API quota exceeded. Please check your API key and account status")
        elif "invalid_api_key" in error_str.lower() or "incorrect api key" in error_str.lower() or ("api key" in error_str.lower() and "invalid" in error_str.lower()):
            raise Exception(f"Invalid {AI_SERVICE.upper()} API key. Please check your API key in the .env file. Get a new key from https://aistudio.google.com/app/apikey")
        elif "rate_limit" in error_str:
            raise Exception("API rate limit exceeded. Please wait a moment and try again")
        else:
            print(f"ERROR in generate_task_breakdown: {error_str}")  # Debug log
            print(f"Traceback: {error_trace}")  # Debug log
            raise Exception(f"Error generating task breakdown: {error_str}")


def generate_step_instructions(step_title: str, step_description: str, context: str = "") -> str:
    """
    Generate detailed instructions for a single step.
    
    Args:
        step_title: Title of the step
        step_description: Brief description
        context: Additional context about the task
        
    Returns:
        Detailed beginner-friendly instructions
    """
    
    prompt = f"""Generate extremely detailed, beginner-friendly instructions for this step:

Step Title: {step_title}
Step Description: {step_description}
Context: {context}

Provide step-by-step instructions that:
1. Are extremely detailed (assume user knows nothing)
2. Include specific actions ("Open terminal", "Type this command", "Create file X")
3. Include exact commands and code snippets
4. Include verification steps ("You should see...")
5. Include troubleshooting tips

Format as a numbered list with clear actions."""

    try:
        if AI_SERVICE == "ollama":
            OLLAMA_AVAILABLE, ollama_module = check_ollama_available()
            if OLLAMA_AVAILABLE and ollama_module:
                ollama = ollama_module
                full_prompt = f"""You are an expert at creating detailed, beginner-friendly instructions.

{prompt}"""
                response = ollama.generate(model=ollama_model_name, prompt=full_prompt)
                return response['response']
        elif AI_SERVICE == "gemini" and gemini_model:
            full_prompt = f"""You are an expert at creating detailed, beginner-friendly instructions.

{prompt}"""
            response = gemini_model.generate_content(full_prompt)
            return response.text
        elif AI_SERVICE == "openai" and openai_client:
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at creating detailed, beginner-friendly instructions."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content
        else:
            return f"1. {step_description}\n2. Follow the standard process for this type of task."
    except Exception as e:
        return f"1. {step_description}\n2. Follow the standard process for this type of task."

