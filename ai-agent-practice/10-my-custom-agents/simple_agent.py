# Simple Agent Template
# A minimal agent you can customize for your own tasks
# Based on the ReAct pattern (Reasoning + Acting)

import json
import os
from typing import Dict, List, Any, Callable

# Try to import OpenAI
try:
    from openai import OpenAI
except ImportError:
    print("Please install openai: pip install openai")
    exit(1)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ==========================================
# DEFINE YOUR TOOLS HERE
# ==========================================

def search_web(query: str) -> str:
    """Search the web for information"""
    # In a real implementation, you'd use an actual search API
    # For now, this is a placeholder
    return f"Search results for '{query}': [This is a placeholder. Connect to real search API]"

def calculate(expression: str) -> str:
    """Calculate a mathematical expression"""
    try:
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Error calculating: {str(e)}"

def read_file(file_path: str) -> str:
    """Read contents of a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def write_file(file_path: str, content: str) -> str:
    """Write content to a file"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to {file_path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"

# ==========================================
# TOOL DEFINITIONS FOR LLM
# ==========================================

TOOLS = [
    {
        "type": "function",
        "function": {
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
                    "expression": {
                        "type": "string",
                        "description": "The mathematical expression to evaluate"
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
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
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write content to a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the file"
                    },
                    "content": {
                        "type": "string",
                        "description": "Content to write"
                    }
                },
                "required": ["file_path", "content"]
            }
        }
    }
]

# Map tool names to functions
TOOL_MAP: Dict[str, Callable] = {
    "search_web": search_web,
    "calculate": calculate,
    "read_file": read_file,
    "write_file": write_file
}

# ==========================================
# THE AGENT
# ==========================================

SYSTEM_PROMPT = """You are a helpful AI assistant that can use tools to accomplish tasks.

When given a task:
1. Think step by step about what needs to be done
2. Use the available tools when needed
3. After using a tool, you'll see the result and can decide next steps
4. Continue until the task is complete
5. Provide a final answer

Available tools:
- search_web: Search for information on the web
- calculate: Perform mathematical calculations
- read_file: Read file contents
- write_file: Write content to files

Be thorough but efficient. If a task requires multiple steps, explain your reasoning."""

class SimpleAgent:
    def __init__(self, max_iterations: int = 10):
        self.max_iterations = max_iterations
        self.messages: List[Dict[str, Any]] = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
    
    def run(self, user_input: str) -> str:
        """Run the agent with user input"""
        print(f"\n🎯 Task: {user_input}\n")
        
        # Add user message
        self.messages.append({"role": "user", "content": user_input})
        
        iteration = 0
        while iteration < self.max_iterations:
            iteration += 1
            print(f"\n--- Iteration {iteration} ---")
            
            # Ask LLM what to do
            print("🤖 Thinking...")
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # Use gpt-4o-mini for cost efficiency
                messages=self.messages,
                tools=TOOLS,
                tool_choice="auto"
            )
            
            message = response.choices[0].message
            
            # Check if LLM wants to use a tool
            if message.tool_calls:
                # LLM wants to use tool(s)
                self.messages.append({
                    "role": "assistant",
                    "content": message.content or "",
                    "tool_calls": [tc.model_dump() for tc in message.tool_calls]
                })
                
                # Execute each tool call
                for tool_call in message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments)
                    
                    print(f"\n🔧 Using tool: {tool_name}")
                    print(f"   Arguments: {tool_args}")
                    
                    # Execute the tool
                    if tool_name in TOOL_MAP:
                        try:
                            result = TOOL_MAP[tool_name](**tool_args)
                            print(f"   Result: {result[:200]}...")  # Truncate long results
                        except Exception as e:
                            result = f"Error: {str(e)}"
                            print(f"   Error: {result}")
                    else:
                        result = f"Unknown tool: {tool_name}"
                        print(f"   Error: {result}")
                    
                    # Add tool result to conversation
                    self.messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(result)
                    })
            
            else:
                # LLM provided final answer
                final_answer = message.content
                print(f"\nDone! Final Answer:\n{final_answer}")
                self.messages.append({"role": "assistant", "content": final_answer})
                return final_answer
        
        return "Max iterations reached without completion."

# ==========================================
# RUN THE AGENT
# ==========================================

if __name__ == "__main__":
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: Please set OPENAI_API_KEY environment variable")
        print("   export OPENAI_API_KEY='your-key-here'")
        exit(1)
    
    # Example tasks you can try
    example_tasks = [
        "Calculate 15 * 23 + 47",
        "Search for information about Python dictionaries",
        "Create a file called hello.txt with 'Hello, World!' inside",
        "Read the file hello.txt",
    ]
    
    print("=" * 60)
    print("SIMPLE AGENT TEMPLATE")
    print("=" * 60)
    print("\nExample tasks you can try:")
    for i, task in enumerate(example_tasks, 1):
        print(f"{i}. {task}")
    
    print("\nEnter your task (or 'quit' to exit):")
    
    # Create agent
    agent = SimpleAgent(max_iterations=10)
    
    while True:
        try:
            user_input = input("\n> ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if not user_input:
                continue
            
            # Run the agent
            result = agent.run(user_input)
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: Error: {str(e)}")
