# AI Agent Practice Workspace

## 🎯 Learning Path (Recommended Order)

Based on real-world production agent patterns used in 2025.

---

### Phase 1: Understand What An Agent Actually Is (No Frameworks)

#### 📁 `01-karpathy-agent/` - START HERE
**Andrej Karpathy's 130-line agent**
- No dependencies, no frameworks
- Can browse web, write code, run code, debug itself
- Read entire source in 5 minutes
- **Goal**: Understand the core loop: LLM → Tool Selection → Execution → Feedback

**What to do:**
1. Clone the repo
2. Read the 130 lines of code
3. Add ONE tool (e.g., file reader)
4. Run it and watch the magic

---

#### 📁 `02-react-pattern/`
**Original ReAct Implementation (120 lines)**
- The pattern powering 99% of agents today
- Reasoning + Acting loop
- No frameworks

**What to do:**
1. Implement the ReAct loop from scratch
2. Understand "Thought → Action → Observation" pattern
3. Connect to any LLM API

---

### Phase 2: Feel Real Agent Power (5 Minutes Each)

#### 📁 `03-mentat/`
**Best open-source code agent**
- Points at any folder, refactors code, adds features
- Better than Copilot Chat for non-trivial tasks
- Works with local (Ollama) or OpenAI

**What to do:**
1. Point it at an old project
2. Ask it to add a feature you never built
3. Watch it edit your actual files

---

#### 📁 `04-claude-computer/`
**Anthropic's full computer control**
- Moves mouse, clicks, types, browses
- The thing that broke the internet 2 months ago
- You can run it locally

**What to do:**
1. Set it up with screen capture
2. Give it a task (e.g., "Book a flight")
3. Watch it control your computer

---

#### 📁 `05-open-interpreter/`
**Classic terminal control agent**
- Full terminal access
- Can do any task on your computer
- Raw agent capability demo

**What to do:**
1. Install it
2. Ask it to automate a repetitive task
3. See it write and execute scripts

---

#### 📁 `06-storm/`
**Stanford's research paper writer**
- Writes 10-page cited research papers
- Real web research
- Complete papers from scratch

**What to do:**
1. Pick a topic you want to learn
2. Let it research and write
3. Review the cited sources

---

### Phase 3: Build Your Own (Production Frameworks)

#### 📁 `07-langgraph-examples/`
**The standard for production agents**
- 60+ complete, runnable examples
- Code agents, research agents, multi-agent teams
- 90% of production agents built on this

**What to do:**
1. Clone the examples repo
2. Pick a simple research agent
3. Modify it for your use case (e.g., email summarizer)
4. Deploy it

---

#### 📁 `08-crewai-examples/`
**Best for multi-agent teams**
- 100+ examples of agent teams
- Market research → Business plan → Landing page
- Copy-pasteable production code

**What to do:**
1. Build a 3-agent team
2. Assign roles (researcher, writer, reviewer)
3. Watch them collaborate

---

### Phase 4: Advanced State-of-the-Art

#### 📁 `09-opendevin/`
**Full AI software engineer**
- Builds complete applications
- 100% local
- Equal to Cognition Devin

**What to do:**
1. Give it a complex coding task
2. Watch it architect, code, test
3. Review the generated codebase

---

#### 📁 `10-my-custom-agents/`
**Your own agent experiments**
- Build agents for YOUR repetitive tasks
- Keep them under 300 lines
- Focus on solving real problems

---

## 🚀 Quick Start Commands

### Start with Karpathy's Agent (Recommended First)
```bash
cd 01-karpathy-agent
git clone https://github.com/karpathy/agentic.git
cd agentic
# Read agent.py (130 lines)
# Add your own tool
# Run: python agent.py
```

### Run Mentat on Your Code
```bash
cd 03-mentat
pip install mentat
mentat /path/to/your/project
# Ask: "Add error handling to all API endpoints"
```

### Try Open Interpreter
```bash
cd 05-open-interpreter
pip install open-interpreter
interpreter
# Now chat with your terminal
```

### Build with LangGraph
```bash
cd 07-langgraph-examples
git clone https://github.com/langchain-ai/langgraph.git
cd langgraph/examples
# Pick any example and run it
```

---

## 💡 Key Insights

After running these, you'll understand:

1. **An agent is just a loop**: LLM → Tool Selection → Execution → Feedback
2. **90% of useful agents are <300 lines**: No need for complex frameworks
3. **The magic is in the tools**: Give good tools, get good results
4. **ReAct pattern powers everything**: Thought → Action → Observation
5. **Multi-agent teams are powerful**: Divide and conquer complex tasks

---

## 📚 Resources

**Core Concept:**
- Agent = Loop that asks LLM "what tool next?", runs it, feeds back result

**Essential Patterns:**
- ReAct: Reasoning + Acting
- Plan-and-Execute: Plan first, then execute
- Multi-Agent: Teams collaborating

**Production Frameworks:**
- LangGraph: Most popular (90% of prod agents)
- CrewAI: Best for multi-agent teams
- AutoGen: Microsoft's framework

---

**Created:** 2026-02-08  
**Goal:** Master AI agents through hands-on practice

**Remember**: Start with Karpathy's 130 lines. Understand it completely. Then everything else makes sense.
