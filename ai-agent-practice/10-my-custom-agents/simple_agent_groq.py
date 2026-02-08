# Simple Agent with Groq (Free Cloud API)
# Fast, powerful models with generous free tier
# Get free API key at: https://console.groq.com

import json
import os
from typing import Dict, List, Any, Callable

# Try to import Groq
try:
    from groq import Groq
except ImportError:
    print("Please install groq: pip install groq")
    print("Get free API key at: https://console.groq.com")
    exit(1)

# ==========================================
# CONFIGURATION
# ==========================================

# Available free models on Groq:
# - llama-3.1-70b-versatile (Best quality, 70B parameters)
# - llama-3.1-8b-instant (Fast, good quality)
# - mixtral-8x7b-32768 (Great for long context)
# - gemma-7b-it (Google's model)

MODEL = "llama-3.1-70b-versatile"  # Best overall model

# Initialize Groq client
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("❌ Please set GROQ_API_KEY environment variable")
    print("   Get free key at: https://console.groq.com")
    print("   Then set it:")
    print("   Windows PowerShell: $env:GROQ_API_KEY='your-key'")
    print("   Windows Git Bash: export GROQ_API_KEY='your-key'")
    exit(1)

client = Groq(api_key=api_key)

# ==========================================
# DEFINE YOUR TOOLS HERE
# ==========================================

def search_web(query: str) -> str:
    """Search the web for information (placeholder)"""
    return f"[Web search placeholder] Searching for: {query}\nTip: Connect this to SerpAPI or similar"

def calculate(expression: str) -> str:
    """Calculate a mathematical expression safely"""
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
# TOOL DEFINITIONS FOR LLM
# ==========================================

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the web for information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Calculate mathematical expressions",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string"}
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read file contents",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string"}
                },
                "required": ["file_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write/create a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string"},
                    "content": {"type": "string"}
                },
                "required": ["file_path", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_directory",
            "description": "List directory contents",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "default": "."}
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
1. Think step by step
2. Use tools when needed
3. Continue until complete
4. Provide clear final answers

Available tools: search_web, calculate, read_file, write_file, list_directory"""

class GroqAgent:
    def __init__(self, model: str = MODEL, max_iterations: int = 10):
        self.model = model
        self.max_iterations = max_iterations
        self.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    def run(self, user_input: str) -> str:
        """Run the agent with user input"""
        print(f"\n🎯 Task: {user_input}\n")
        self.messages.append({"role": "user", "content": user_input})
        
        iteration = 0
        while iteration < self.max_iterations:
            iteration += 1
            print(f"\n{'='*60}")
            print(f"🔄 Iteration {iteration}/{self.max_iterations}")
            print('='*60)
            
            print("🤖 Thinking...")
            
            try:
                response = client.chat.completions.create(
                    model=self.model,
                    messages=self.messages,
                    tools=TOOLS,
                    tool_choice="auto"
                )
            except Exception as e:
                return f"❌ API Error: {str(e)}"
            
            message = response.choices[0].message
            
            # Check if tool calls
            if message.tool_calls:
                # Add assistant message with tool calls
                self.messages.append({
                    "role": "assistant",
                    "content": message.content or "",
                    "tool_calls": [tc.model_dump() for tc in message.tool_calls]
                })
                
                # Execute each tool
                for tool_call in message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments)
                    
                    print(f"\n🔧 Using tool: {tool_name}")
                    print(f"   Arguments: {tool_args}")
                    
                    if tool_name in TOOL_MAP:
                        try:
                            result = TOOL_MAP[tool_name](**tool_args)
                            print(f"   Result: {result[:300]}...")
                        except Exception as e:
                            result = f"Error: {str(e)}"
                            print(f"   ❌ Error: {result}")
                    else:
                        result = f"Unknown tool: {tool_name}"
                    
                    # Add tool result
                    self.messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(result)
                    })
            else:
                # Final answer
                answer = message.content
                print(f"\n✅ Final Answer:\n{answer}")
                self.messages.append({"role": "assistant", "content": answer})
                return answer
        
        return "Max iterations reached."

# ==========================================
# RUN
# ==========================================

def main():
    print("="*60)
    print("🤖 SIMPLE AGENT WITH GROQ (Free Cloud API)")
    print("="*60)
    print(f"\nModel: {MODEL}")
    print("Free tier: 20 req/min, 1M tokens/day")
    print("Get key: https://console.groq.com\n")
    
    agent = GroqAgent(model=MODEL)
    
    examples = [
        "Calculate 15 * 23 + 47",
        "List files in current directory",
        "Create hello.txt with 'Hello World'",
    ]
    
    print("Examples:")
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
