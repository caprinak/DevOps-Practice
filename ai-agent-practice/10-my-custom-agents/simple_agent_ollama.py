# Simple Agent with Ollama (Local LLM - No API Key Needed!)
# This agent runs entirely on your computer using Ollama

import json
import requests
import os
from typing import Dict, List, Any, Callable

# ==========================================
# CONFIGURATION
# ==========================================

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2"  # You can change this to any model you have installed

# ==========================================
# DEFINE YOUR TOOLS HERE
# ==========================================

def search_web(query: str) -> str:
    """Search the web for information (placeholder - implement with real search API)"""
    return f"[Web search placeholder] Searching for: {query}\nTip: Connect this to a real search API like SerpAPI or DuckDuckGo"

def calculate(expression: str) -> str:
    """Calculate a mathematical expression safely"""
    try:
        # Only allow safe math operations
        allowed_chars = set('0123456789+-*/.() ')
        if not all(c in allowed_chars for c in expression):
            return "Error: Invalid characters in expression"
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Error calculating: {str(e)}"

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
        return f"Error listing directory: {str(e)}"

# ==========================================
# TOOL DEFINITIONS FOR LLM
# ==========================================

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
        "description": "Calculate mathematical expressions (e.g., '15 * 23', '100 + 50')",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The mathematical expression to evaluate"
                }
            },
            "required": ["expression"]
        }
    },
    {
        "name": "read_file",
        "description": "Read the contents of a file from the filesystem",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file (e.g., 'README.md', 'src/main.py')"
                }
            },
            "required": ["file_path"]
        }
    },
    {
        "name": "write_file",
        "description": "Write or create a file with the given content",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path where to write the file"
                },
                "content": {
                    "type": "string",
                    "description": "Content to write to the file"
                }
            },
            "required": ["file_path", "content"]
        }
    },
    {
        "name": "list_directory",
        "description": "List all files and folders in a directory",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Directory path (default: current directory)",
                    "default": "."
                }
            }
        }
    }
]

# Map tool names to functions
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

SYSTEM_PROMPT = f"""You are a helpful AI assistant that can use tools to accomplish tasks.

You have access to the following tools:
1. search_web - Search for information
2. calculate - Perform math calculations
3. read_file - Read file contents
4. write_file - Write/create files
5. list_directory - List files in a folder

When given a task:
1. Think about what needs to be done
2. Use the available tools when needed
3. Continue until the task is complete
4. Provide a clear final answer

To use a tool, respond with a JSON object like this:
{{"tool": "tool_name", "parameters": {{"param1": "value1"}}}}

If no tool is needed, just respond normally."""

class OllamaAgent:
    def __init__(self, model: str = MODEL, max_iterations: int = 10):
        self.model = model
        self.max_iterations = max_iterations
        self.messages: List[Dict[str, str]] = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
    
    def check_ollama(self) -> bool:
        """Check if Ollama is running"""
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def list_models(self) -> List[str]:
        """List available Ollama models"""
        try:
            response = requests.get("http://localhost:11434/api/tags")
            models = response.json().get("models", [])
            return [m["name"] for m in models]
        except:
            return []
    
    def chat_with_ollama(self, messages: List[Dict[str, str]]) -> str:
        """Send messages to Ollama and get response"""
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False
        }
        
        try:
            response = requests.post(OLLAMA_URL, json=payload, timeout=60)
            response.raise_for_status()
            return response.json()["message"]["content"]
        except requests.exceptions.ConnectionError:
            return "ERROR: Cannot connect to Ollama. Is it running?"
        except Exception as e:
            return f"ERROR: {str(e)}"
    
    def parse_tool_call(self, text: str) -> tuple:
        """Parse tool call from LLM response"""
        try:
            # Try to find JSON in the response
            if "{" in text and "}" in text:
                # Extract JSON
                start = text.find("{")
                end = text.rfind("}") + 1
                json_str = text[start:end]
                data = json.loads(json_str)
                
                if "tool" in data and "parameters" in data:
                    return data["tool"], data["parameters"]
        except:
            pass
        return None, None
    
    def run(self, user_input: str) -> str:
        """Run the agent with user input"""
        print(f"\n🎯 Task: {user_input}\n")
        
        # Add user message
        self.messages.append({"role": "user", "content": user_input})
        
        iteration = 0
        while iteration < self.max_iterations:
            iteration += 1
            print(f"\n{'='*60}")
            print(f"🔄 Iteration {iteration}/{self.max_iterations}")
            print('='*60)
            
            # Get response from Ollama
            print("🤖 Thinking...")
            response = self.chat_with_ollama(self.messages)
            
            if response.startswith("ERROR:"):
                print(f"❌ {response}")
                return response
            
            print(f"\n💭 LLM Response:\n{response}\n")
            
            # Check if LLM wants to use a tool
            tool_name, tool_params = self.parse_tool_call(response)
            
            if tool_name and tool_name in TOOL_MAP:
                print(f"🔧 Using tool: {tool_name}")
                print(f"   Parameters: {tool_params}")
                
                # Execute the tool
                try:
                    result = TOOL_MAP[tool_name](**tool_params)
                    print(f"\n📊 Result:\n{result[:500]}...")  # Truncate long results
                except Exception as e:
                    result = f"Error: {str(e)}"
                    print(f"   ❌ Error: {result}")
                
                # Add tool result to conversation
                tool_result_msg = f"Tool '{tool_name}' result:\n{result}"
                self.messages.append({"role": "user", "content": tool_result_msg})
            else:
                # LLM provided final answer
                print(f"\n✅ Final Answer:\n{response}")
                self.messages.append({"role": "assistant", "content": response})
                return response
        
        return "Max iterations reached without completion."

# ==========================================
# RUN THE AGENT
# ==========================================

def print_header():
    print("="*60)
    print("🤖 SIMPLE AGENT WITH OLLAMA (Local LLM)")
    print("="*60)
    print(f"\nModel: {MODEL}")
    print("Status: 100% Local - No API key needed!")
    print("\nMake sure Ollama is running:")
    print("  1. Install: winget install Ollama.Ollama")
    print("  2. Download model: ollama pull llama3.2")
    print("  3. Run this script!\n")

def print_examples():
    print("\n📚 Example tasks you can try:")
    examples = [
        "Calculate 15 * 23 + 47",
        "What is 2 to the power of 10?",
        "List all files in the current directory",
        "Create a file called hello.txt with 'Hello, World!' inside",
        "Read the file hello.txt and tell me what's in it",
        "Write a Python script that prints numbers 1 to 10 and save it as count.py",
    ]
    for i, ex in enumerate(examples, 1):
        print(f"  {i}. {ex}")

def main():
    print_header()
    
    # Create agent
    agent = OllamaAgent(model=MODEL, max_iterations=10)
    
    # Check if Ollama is running
    print("🔍 Checking Ollama...")
    if not agent.check_ollama():
        print("\n❌ ERROR: Cannot connect to Ollama!")
        print("\nPlease make sure Ollama is installed and running:")
        print("  1. Install: winget install Ollama.Ollama")
        print("  2. Download model: ollama pull llama3.2")
        print("  3. Start Ollama (it runs in background)")
        print("\nThen run this script again.")
        return
    
    print("✅ Ollama is running!")
    
    # List available models
    models = agent.list_models()
    if models:
        print(f"📦 Available models: {', '.join(models)}")
        if MODEL not in models:
            print(f"\n⚠️  Model '{MODEL}' not found!")
            print(f"Download it with: ollama pull {MODEL}")
            print(f"Or change MODEL variable in this script to: {models[0]}")
            return
    else:
        print("⚠️  No models found. Download one with: ollama pull llama3.2")
        return
    
    print(f"✅ Using model: {MODEL}\n")
    
    print_examples()
    
    print("\n" + "="*60)
    print("Enter your task (or 'quit' to exit):")
    print("="*60)
    
    while True:
        try:
            user_input = input("\n> ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            # Run the agent
            result = agent.run(user_input)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
