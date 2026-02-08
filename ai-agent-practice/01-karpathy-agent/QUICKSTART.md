# Karpathy's Agent - Quick Start Guide

## What Is This?

Andrej Karpathy's famous 130-line agent. **This is the single best starting point** for understanding agents.

- ✅ Only 130 lines of Python
- ✅ Zero dependencies (except OpenAI API)
- ✅ Can browse web, write code, run code, debug itself
- ✅ You can read and understand the entire thing in 5 minutes

---

## Setup (2 Minutes)

### 1. Clone the Repository
```bash
cd E:/KHOA/HAPPY_CODING/CODER_THAN_THANH/microservices&devops/ai-agent-practice/01-karpathy-agent
git clone https://github.com/karpathy/agentic.git
cd agentic
```

### 2. Install Dependencies
```bash
pip install openai
```

### 3. Set Your OpenAI API Key
```bash
# Windows (PowerShell)
$env:OPENAI_API_KEY="your-api-key-here"

# Windows (Git Bash)
export OPENAI_API_KEY="your-api-key-here"
```

Or create a `.env` file:
```
OPENAI_API_KEY=your-api-key-here
```

### 4. Read the Code (5 Minutes)

Open `agent.py` and read it. It's only 130 lines!

**Key sections to understand:**

```python
# 1. The tool definitions (lines ~20-60)
# Each tool has:
# - name: what it's called
# - description: what it does (LLM sees this)
# - input_schema: what parameters it needs

# 2. The system prompt (lines ~70-90)
# Tells the LLM how to behave
# "You are an agent that can use tools..."

# 3. The main loop (lines ~100-130)
# While True:
#   1. Ask LLM: "What tool do you want to use?"
#   2. Run the tool
#   3. Give result back to LLM
#   4. Repeat
```

---

## Run It

### Basic Example
```bash
python agent.py "What is the weather in New York?"
```

The agent will:
1. Realize it needs weather data
2. Use the web_search tool
3. Find weather information
4. Return the answer

### Code Example
```bash
python agent.py "Write a Python function to calculate fibonacci numbers"
```

The agent will:
1. Write the code
2. Save it to a file
3. Run it to verify it works
4. Show you the result

---

## Your First Exercise

### Add a "Read File" Tool

The agent doesn't have a tool to read local files. Let's add one!

**Step 1**: Open `agent.py`

**Step 2**: Add this tool definition after the existing tools:

```python
{
    "name": "read_file",
    "description": "Read the contents of a file",
    "input_schema": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Path to the file to read"
            }
        },
        "required": ["file_path"]
    }
}
```

**Step 3**: Add this function to handle the tool:

```python
def read_file(file_path: str) -> str:
    """Read and return the contents of a file"""
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"
```

**Step 4**: Update the tool dispatch (find where other tools are called):

```python
elif tool_name == "read_file":
    result = read_file(**arguments)
```

**Step 5**: Test it!

```bash
python agent.py "Read the file README.md and summarize it"
```

🎉 **Congratulations!** You just built your first agent tool!

---

## Understanding the Core Pattern

After running this, you'll understand:

```
┌─────────────────────────────────────────┐
│           THE AGENT LOOP                │
└─────────────────────────────────────────┘

1. USER INPUT
   "What is the weather in Tokyo?"
         ↓
2. LLM DECIDES
   "I need to search the web"
         ↓
3. TOOL EXECUTION
   web_search("Tokyo weather")
         ↓
4. OBSERVATION
   "Current weather in Tokyo: 22°C, sunny"
         ↓
5. FEEDBACK TO LLM
   "The search result says: 22°C, sunny"
         ↓
6. LLM RESPONDS
   "The weather in Tokyo is 22°C and sunny"
         ↓
   (Or go back to step 2 if more tools needed)
```

**That's it.** An agent is just this loop.

---

## Common Issues

### "No module named 'openai'"
```bash
pip install openai
```

### "API key not found"
Make sure you set the environment variable:
```bash
export OPENAI_API_KEY="your-key"
```

### "The agent keeps looping"
The agent has a max_iterations limit. You can increase it:
```python
max_iterations = 10  # Change this to 20 or higher
```

---

## Next Steps

After you understand this 130-line agent:

1. **Add more tools**:
   - Write to files
   - List directory contents
   - Execute shell commands
   - Query a database

2. **Modify the system prompt**:
   - Make it more specialized (e.g., "You are a code reviewer")
   - Add constraints (e.g., "Always ask for confirmation before running commands")

3. **Try the ReAct pattern** (go to `../02-react-pattern/`)

4. **Move to production frameworks** (go to `../07-langgraph-examples/`)

---

## The "Aha!" Moment

When you run this and see the agent:
1. Decide it needs to search
2. Actually call the search function
3. Get results
4. Formulate an answer

You'll realize: **There is no magic.** It's just code.

But also: **This is incredibly powerful.** A loop that can use tools is all you need.

---

**Time to complete**: 15 minutes  
**Lines of code to read**: 130  
**Dependencies**: 1 (openai)  
**Frameworks**: 0

**This is where every agent developer should start.**
