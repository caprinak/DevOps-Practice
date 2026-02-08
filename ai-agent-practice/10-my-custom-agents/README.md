# My Custom Agents

This folder contains ready-to-run agent templates you can customize.

## 🚀 Quick Start (Choose One)

### Option A: Ollama (Recommended - 100% Free, Local)
**Best for**: Privacy, offline use, no API keys

```bash
# 1. Install Ollama
winget install Ollama.Ollama

# 2. Download a model
ollama pull llama3.2

# 3. Run the agent
python simple_agent_ollama.py
```

### Option B: Groq (Free Cloud API)
**Best for**: Maximum speed, best model quality

```bash
# 1. Get free API key
# Visit: https://console.groq.com
# Sign up → Create API key

# 2. Set environment variable
$env:GROQ_API_KEY="your-key-here"

# 3. Install dependency
pip install groq

# 4. Run the agent
python simple_agent_groq.py
```

### Option C: OpenAI (If you have a key)
```bash
# 1. Set key
$env:OPENAI_API_KEY="your-key"

# 2. Install dependency
pip install openai

# 3. Run the agent
python simple_agent.py
```

---

## 📁 Files

| File | Backend | Cost | Best For |
|------|---------|------|----------|
| `simple_agent_ollama.py` | Local (Ollama) | Free | Privacy, learning |
| `simple_agent_groq.py` | Cloud (Groq) | Free tier | Speed, quality |
| `simple_agent.py` | OpenAI | Paid | Reliability |

---

## 🎯 What These Agents Can Do

All agents have these tools:

1. **calculate** - Math expressions
2. **read_file** - Read any file
3. **write_file** - Create/edit files
4. **list_directory** - List files/folders
5. **search_web** - Web search (placeholder - connect your own API)

---

## 💡 Example Tasks

Try these after starting an agent:

```
> Calculate 25 * 47 + 100

> List all files in the current directory

> Create a Python script that prints "Hello, World!" and save it as hello.py

> Read the file hello.py and explain what it does

> Write a todo list with 5 items and save it as todo.txt

> Calculate 2 to the power of 16
```

---

## 🛠️ Customize Your Agent

### Add a New Tool

1. **Define the function:**
```python
def my_custom_tool(param: str) -> str:
    """Description of what this tool does"""
    result = do_something(param)
    return f"Result: {result}"
```

2. **Add to TOOLS list:**
```python
{
    "name": "my_custom_tool",
    "description": "Description for the LLM",
    "parameters": {
        "type": "object",
        "properties": {
            "param": {"type": "string"}
        },
        "required": ["param"]
    }
}
```

3. **Add to TOOL_MAP:**
```python
TOOL_MAP = {
    "my_custom_tool": my_custom_tool,
    # ... other tools
}
```

4. **Done!** The agent can now use your tool.

### Example: Add a Timer Tool

```python
import time

def start_timer(seconds: int) -> str:
    """Start a countdown timer"""
    time.sleep(seconds)
    return f"⏰ Timer finished! {seconds} seconds elapsed"

# Add to TOOLS:
{
    "name": "start_timer",
    "description": "Start a countdown timer for specified seconds",
    "parameters": {
        "type": "object",
        "properties": {
            "seconds": {"type": "integer"}
        },
        "required": ["seconds"]
    }
}

# Add to TOOL_MAP:
"start_timer": start_timer
```

---

## 🎓 Learning Path

1. **Start with Ollama** - Run locally, understand the basics
2. **Try all example tasks** - See what the agent can do
3. **Add one custom tool** - Make it yours
4. **Switch to Groq** - Experience faster, smarter responses
5. **Build something useful** - Automate a task you do often

---

## 🐛 Troubleshooting

### "Ollama not found"
```bash
# Install Ollama
winget install Ollama.Ollama

# Or download from: https://ollama.com
```

### "Model not found"
```bash
# Download the model
ollama pull llama3.2
```

### "Groq API key not found"
```bash
# Set the environment variable
$env:GROQ_API_KEY="your-key"

# Verify it's set
$env:GROQ_API_KEY
```

### "Module not found"
```bash
# Install missing dependencies
pip install groq
# or
pip install openai
```

---

## 📚 Next Steps

- ✅ Run the agent
- ✅ Try the examples
- ✅ Add a custom tool
- ✅ Build an agent for your specific task
- 🔜 Move to LangGraph for production (see ../07-langgraph-examples/)

---

**Remember**: The best agents are under 300 lines. Keep it simple!
