"""
Simple Agent with Google Gemini (Free Tier Available)
Get free API key at: https://aistudio.google.com/app/apikey

Free tier: 60 requests/minute, ample daily quota
Models: gemini-1.5-flash (fast), gemini-1.5-pro (powerful)
"""

import json
import os
from typing import Dict, List, Any, Callable

# Try to import Google Generative AI
try:
    import google.generativeai as genai
except ImportError:
    print("Please install Google Generative AI: pip install google-generativeai")
    print("Get free API key at: https://aistudio.google.com/app/apikey")
    exit(1)

# ==========================================
# CONFIGURATION
# ==========================================

# Available Gemini models:
# - gemini-1.5-flash: Fast, efficient (recommended for agents)
# - gemini-1.5-pro: Most capable, better reasoning
# - gemini-1.5-flash-8b: Smaller, faster

MODEL = "gemini-1.5-flash"  # Fast and capable for agents

# Initialize Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ Please set GEMINI_API_KEY environment variable")
    print("   Get free key at: https://aistudio.google.com/app/apikey")
    print("   Then set it:")
    print("   Windows PowerShell: $env:GEMINI_API_KEY='your-key'")
    print("   Windows Git Bash: export GEMINI_API_KEY='your-key'")
    exit(1)

genai.configure(api_key=api_key)

# ==========================================
# DEFINE YOUR TOOLS HERE
# ==========================================

def search_web(query: str) -> str:
    """Search the web for information"""
    return f"[Web search placeholder] Searching for: {query}"

def calculate(expression: str) -> str:
    """Calculate a mathematical expression"""
    try:
        allowed_chars = set('0123456789+-*/.() ')
        if not all(c in allowed_chars for c in expression):
            return "Error: Invalid characters"
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"

def read_file(file_path: str) -> str:
    """Read contents of a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            return f"File contents:\n{content}"
    except Exception as e:
        return f"Error reading file: {str(e)}"

def write_file(file_path: str, content: str) -> str:
    """Write content to a file"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"✅ Successfully wrote to {file_path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"

def list_directory(path: str = ".") -> str:
    """List files in a directory"""
    try:
        files = os.listdir(path)
        return f"Files in {path}:\n" + "\n".join(files)
    except Exception as e:
        return f"Error: {str(e)}"

# ==========================================
# TOOL DEFINITIONS FOR GEMINI
# ==========================================

# Gemini uses a different function declaration format
TOOLS = [
    {
        "name": "search_web",
        "description": "Search the web for information on any topic",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "calculate",
        "description": "Calculate mathematical expressions (e.g., '15 * 23')",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The mathematical expression"
                }
            },
            "required": ["expression"]
        }
    },
    {
        "name": "read_file",
        "description": "Read the contents of a file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file"
                }
            },
            "required": ["file_path"]
        }
    },
    {
        "name": "write_file",
        "description": "Write or create a file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path where to write"
                },
                "content": {
                    "type": "string",
                    "description": "Content to write"
                }
            },
            "required": ["file_path", "content"]
        }
    },
    {
        "name": "list_directory",
        "description": "List directory contents",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Directory path",
                    "default": "."
                }
            }
        }
    }
]

TOOL_MAP: Dict[str, Callable] = {
    "search_web": search_web,
    "calculate": calculate,
    "read_file": read_file,
    "write_file": write_file,
    "list_directory": list_directory
}

# ==========================================
# THE AGENT
# ==========================================

SYSTEM_PROMPT = """You are a helpful AI assistant with access to tools.

When given a task:
1. Think step by step about what needs to be done
2. Use the available tools when needed
3. Continue until the task is complete
4. Provide a clear final answer

Available tools:
- search_web: Search for information
- calculate: Perform math calculations  
- read_file: Read file contents
- write_file: Write/create files
- list_directory: List files in a folder

Use tools by calling them with the appropriate parameters."""

class GeminiAgent:
    def __init__(self, model: str = MODEL, max_iterations: int = 10):
        self.model_name = model
        self.max_iterations = max_iterations
        
        # Initialize Gemini model with tools
        self.model = genai.GenerativeModel(
            model_name=model,
            tools=TOOLS,
            system_instruction=SYSTEM_PROMPT
        )
        
        # Start chat session
        self.chat = self.model.start_chat(enable_automatic_function_calling=False)
    
    def run(self, user_input: str) -> str:
        """Run the agent with user input"""
        print(f"\n🎯 Task: {user_input}\n")
        
        iteration = 0
        while iteration < self.max_iterations:
            iteration += 1
            print(f"\n{'='*60}")
            print(f"🔄 Iteration {iteration}/{self.max_iterations}")
            print('='*60)
            
            print("🤖 Thinking...")
            
            try:
                # Send message to Gemini
                response = self.chat.send_message(user_input)
                
                # Check if there are function calls
                if response.candidates[0].content.parts:
                    part = response.candidates[0].content.parts[0]
                    
                    # Check if it's a function call
                    if hasattr(part, 'function_call') and part.function_call:
                        function_call = part.function_call
                        tool_name = function_call.name
                        tool_args = dict(function_call.args)
                        
                        print(f"\n🔧 Using tool: {tool_name}")
                        print(f"   Arguments: {tool_args}")
                        
                        # Execute the tool
                        if tool_name in TOOL_MAP:
                            try:
                                result = TOOL_MAP[tool_name](**tool_args)
                                print(f"   Result: {result[:300]}...")
                            except Exception as e:
                                result = f"Error: {str(e)}"
                                print(f"   ❌ Error: {result}")
                        else:
                            result = f"Unknown tool: {tool_name}"
                            print(f"   ❌ {result}")
                        
                        # Send result back to Gemini
                        user_input = f"Tool '{tool_name}' returned: {result}"
                        continue
                    
                    # Regular text response
                    answer = response.text
                    print(f"\n✅ Final Answer:\n{answer}")
                    return answer
                    
            except Exception as e:
                return f"❌ Error: {str(e)}"
        
        return "Max iterations reached."

# ==========================================
# RUN
# ==========================================

def main():
    print("="*60)
    print("🤖 SIMPLE AGENT WITH GOOGLE GEMINI")
    print("="*60)
    print(f"\nModel: {MODEL}")
    print("Free tier: 60 requests/min")
    print("Get key: https://aistudio.google.com/app/apikey\n")
    
    agent = GeminiAgent(model=MODEL)
    
    examples = [
        "Calculate 15 * 23 + 47",
        "What is 2 to the power of 10?",
        "List files in current directory",
        "Create hello.txt with 'Hello from Gemini!'",
        "Read the file hello.txt",
    ]
    
    print("📚 Examples:")
    for i, ex in enumerate(examples, 1):
        print(f"  {i}. {ex}")
    
    print("\nEnter task (or 'quit'):")
    
    while True:
        try:
            user_input = input("\n> ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            result = agent.run(user_input)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
