# Running AI Agents Without OpenAI API Key

## 🆓 Free/Open Source Alternatives

You have 4 great options that cost $0:

---

## Option 1: Ollama (Recommended - 100% Free, 100% Local)

Run LLMs locally on your own computer. No API keys, no internet required after download.

### Setup (5 minutes)

**Step 1: Install Ollama**
```bash
# Windows
# Download from: https://ollama.com/download/windows
# Or use winget:
winget install Ollama.Ollama
```

**Step 2: Download a Model**
```bash
# Download Llama 3.2 (3B parameters, fast, good for agents)
ollama pull llama3.2

# Or download a bigger model for better quality
ollama pull llama3.1:8b

# Or download Mistral (very good for coding)
ollama pull mistral
```

**Step 3: Test It**
```bash
ollama run llama3.2
# Chat with it, then type /bye to exit
```

**Step 4: Use with Our Agent**

I've created an Ollama-compatible version: `simple_agent_ollama.py`

```bash
cd 10-my-custom-agents
python simple_agent_ollama.py
```

---

## Option 2: Google Gemini (Free Tier - Very Generous)

Google's Gemini API has a very generous free tier with high rate limits.

### Setup (2 minutes)

**Step 1: Get Free API Key**
1. Go to: https://aistudio.google.com/app/apikey
2. Sign in with Google account
3. Create API key (instant, no credit card)

**Step 2: Set Environment Variable**
```bash
# Windows PowerShell
$env:GEMINI_API_KEY="your-gemini-key"

# Windows Git Bash
export GEMINI_API_KEY="your-gemini-key"
```

**Step 3: Install & Run**
```bash
pip install google-generativeai
cd 10-my-custom-agents
python simple_agent_gemini.py
```

**Free Tier Limits:**
- 60 requests/minute
- Generous daily token quota
- gemini-1.5-flash: Fast, efficient
- gemini-1.5-pro: Most capable

---

## Option 3: Groq (Free Tier - Fast API)

Groq provides free API access with generous limits. Uses Llama and Mixtral models.

### Setup (2 minutes)

**Step 1: Get Free API Key**
1. Go to: https://console.groq.com
2. Sign up (free)
3. Create API key

**Step 2: Set Environment Variable**
```bash
# Windows PowerShell
$env:GROQ_API_KEY="your-groq-key"

# Windows Git Bash
export GROQ_API_KEY="your-groq-key"
```

**Step 3: Use with Our Agent**

I've created a Groq-compatible version: `simple_agent_groq.py`

```bash
cd 10-my-custom-agents
python simple_agent_groq.py
```

**Free Tier Limits:**
- 20 requests/minute
- 1,000,000 tokens/day
- Perfect for learning and testing!

---

## Option 3: LM Studio (GUI for Local Models)

If you prefer a graphical interface.

### Setup
1. Download: https://lmstudio.ai/
2. Download a model (Llama 3, Mistral, etc.)
3. Start the local server
4. Use the provided local API endpoint

---

## 🎯 Recommended Path

### For Beginners (Start Here):
1. **Get Gemini API Key** (Option 2 above) - Easiest, no installation
2. **Run our Gemini agent** - Instant start, generous limits
3. **Or install Ollama** (Option 1) - For local privacy
4. **Everything is free!**

### If You Want Better Quality:
1. **Get Groq API key** (Option 2)
2. **Uses powerful cloud models** (Llama 70B)
3. **Still completely free**
4. **Much faster than local on most computers**

---

## 📋 Quick Start: Ollama Agent

### 1. Install Ollama
```bash
winget install Ollama.Ollama
```

### 2. Download Model
```bash
ollama pull llama3.2
```

### 3. Run the Agent
```bash
cd ai-agent-practice/10-my-custom-agents
python simple_agent_ollama.py
```

### 4. Try These Tasks
```
> Calculate 25 * 47
> Write a Python function to reverse a string
> Read the file README.md and summarize it
> Create a todo list file with 5 items
```

---

## 🚀 Quick Start: Groq Agent (Free Cloud API)

### 1. Get API Key
- https://console.groq.com
- Sign up → Create API key → Copy it

### 2. Set Key
```bash
$env:GROQ_API_KEY="gsk_your_key_here"
```

### 3. Run the Agent
```bash
cd ai-agent-practice/10-my-custom-agents
python simple_agent_groq.py
```

---

## 💡 Model Recommendations

### For Local (Ollama):
| Model | Size | Speed | Quality | Use Case |
|-------|------|-------|---------|----------|
| llama3.2 | 3B | ⚡⚡⚡ | ⭐⭐⭐ | Best for beginners, very fast |
| llama3.1:8b | 8B | ⚡⚡ | ⭐⭐⭐⭐ | Better reasoning, still fast |
| mistral | 7B | ⚡⚡ | ⭐⭐⭐⭐ | Great for coding tasks |
| codellama | 7B | ⚡⚡ | ⭐⭐⭐⭐⭐ | Specialized for code |

### For Groq (Cloud - Free):
| Model | Use Case |
|-------|----------|
| llama-3.1-70b-versatile | Best overall, very capable |
| llama-3.1-8b-instant | Fast responses, good quality |
| mixtral-8x7b-32768 | Great for longer context |

---

## 🎓 Which Should You Choose?

**Choose Ollama if:**
- ✅ You want 100% privacy (everything stays on your computer)
- ✅ You have a decent computer (8GB+ RAM)
- ✅ You don't want any API keys or accounts
- ✅ You want to work offline

**Choose Gemini if:**
- ✅ You want the most generous free tier (60 req/min)
- ✅ You want high-quality responses without local setup
- ✅ You already have a Google account
- ✅ You want multimodal capabilities (images, etc.)

**Choose Groq if:**
- ✅ You want the fastest inference speed
- ✅ You want access to Llama 70B (most capable open model)
- ✅ You need lower latency than Gemini
- ✅ You don't mind creating another account

**Best Strategy:**
- ✅ Start with **Gemini** (easiest setup, most generous limits)
- ✅ Try **Groq** for comparison (different model strengths)
- ✅ Switch to **Ollama** for privacy/offline work
- ✅ All agents have the same tools, easy to swap!

---

## 🛠️ Troubleshooting

### "Ollama not found"
```bash
# Make sure ollama is installed and in PATH
ollama --version
# If not found, restart your terminal or reinstall
```

### "Model not found"
```bash
# Download the model first
ollama pull llama3.2
```

### "Groq API key not found"
```bash
# Check if it's set
echo $env:GROQ_API_KEY
# If empty, set it again
$env:GROQ_API_KEY="your-key"
```

### "Out of memory"
```bash
# Use a smaller model
ollama pull llama3.2  # 3B model, uses ~4GB RAM
# Instead of
ollama pull llama3.1:70b  # 70B model, uses ~40GB RAM
```

---

## 🎯 Next Steps

1. **Pick your option** (Ollama recommended for beginners)
2. **Set it up** (5-10 minutes)
3. **Run the agent** (see files in `10-my-custom-agents/`)
4. **Try Karpathy's agent** (adapt it to use Ollama/Groq)
5. **Build your own!**

---

**Ready to start?** I recommend:
1. Install Ollama: `winget install Ollama.Ollama`
2. Download model: `ollama pull llama3.2`
3. Run agent: `python simple_agent_ollama.py`

Want me to walk you through any of these steps?
