# AI Agent Demo - LangGraph with Azure OpenAI

This repository contains demos for building AI agents using **LangChain**, **LangGraph**, and **Azure OpenAI API**.

## 📋 Prerequisites

- Python 3.8+
- Azure OpenAI account with:
  - An endpoint URL
  - An API key
  - A deployed chat model (e.g., GPT-4, GPT-4o-mini, GPT-3.5-turbo)

## 🚀 Environment Setup

### 1. Clone the Repository

```bash
git clone https://github.com/patelashutosh/agent_demo.git
cd agent_demo
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Azure OpenAI Credentials

Copy the example environment file:
```bash
cp env.example .env
```

Edit `.env` and fill in your Azure OpenAI credentials:
```env
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
OPENAI_API_VERSION=2024-02-01
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=your-deployment-name
```

**Note:** The `.env` file is automatically excluded from git via `.gitignore` to protect your credentials.

## 📦 Project Structure

```
agent_demo/
├── chat_agent/              # Chat agent with tool calling
│   ├── chat_agent_demo.py
│   └── README.md
├── simple_browser_agent/    # Browser agent framework
│   ├── agent.py
│   ├── browser.py
│   ├── tools.py
│   ├── prompts.py
│   ├── models.py
│   └── README.md
├── greenhouse_agent/        # Browser agent demo - ATS automation
│   ├── greenhouse_demo.py
│   └── README.md
├── doc/                     # Presentation materials
│   ├── AI_Agent_Session_Presentation.md
│   └── SESSION_PREPARATION_GUIDE.md
├── requirements.txt         # Python dependencies
├── env.example             # Template for environment variables
├── .env                    # Your credentials (not in git)
└── venv/                   # Virtual environment
```

## 🎯 Available Demos

### 1. Chat Agent with Tool Calling
A conversational agent that demonstrates the ReAct pattern with multiple tools.

**Tools Available**:
- 📈 **Stock Price Checker**: Get real-time prices for NSE/BSE stocks (TCS, Infosys, Reliance, etc.)
- 💱 **Currency Converter**: Convert between INR and other currencies (USD, EUR, GBP, etc.)
- 🏏 **Cricket Score Tracker**: Get live cricket scores, recent results, and upcoming matches

📖 See [chat_agent/README.md](chat_agent/README.md) for details.

**Run**: `python chat_agent/chat_agent_demo.py`

**Perfect for**: Learning about function calling, tool usage, LangGraph basics

---

### 2. Browser Agent Framework
**Reusable** core browser automation framework using Chrome DevTools Protocol (CDP).

**Features**:
- Vision-based page understanding (screenshots + element extraction)
- Element highlighting for transparency
- 8 browser actions: navigate, click, input_text, extract, send_keys, scroll, screenshot, done
- LangGraph state management

📖 See [simple_browser_agent/README.md](simple_browser_agent/README.md) for framework details.

**Note**: This is a reusable framework/library used by all browser agent demos (like Greenhouse). Think of it as a Python package that multiple applications can import and use.

---

### 3. Browser Agent - Greenhouse ATS Demo
An autonomous browser agent that logs into Greenhouse ATS and navigates to job applications automatically.

**Capabilities**:
- 🔐 Automated login with credentials
- 🔍 Search and navigate job listings
- 📋 Navigate to applications review page
- 👁️ Vision-based page understanding
- 🤖 Autonomous decision making (ReAct pattern)
- 🎯 Goal-oriented task completion

📖 See [greenhouse_agent/README.md](greenhouse_agent/README.md) for details.

**Run**: `python greenhouse_agent/greenhouse_demo.py`

**Perfect for**: Demonstrating autonomous agents, browser automation, AI-powered RPA

**Note**: This demo uses the `simple_browser_agent/` framework. The framework is reusable - you can create additional demos (LinkedIn automation, GitHub Actions, etc.) using the same underlying browser engine.

---

## 🎓 Knowledge Sharing Session

This repository includes complete presentation materials for conducting AI Agent knowledge sharing sessions:

📄 **Presentation**: [doc/AI_Agent_Session_Presentation.md](doc/AI_Agent_Session_Presentation.md)
📖 **Session Guide**: [doc/SESSION_PREPARATION_GUIDE.md](doc/SESSION_PREPARATION_GUIDE.md)

**Topics Covered**:
- What are AI Agents? (Evolution from chatbots)
- Function Calling / Tool Usage
- LangGraph Architecture
- ReAct Pattern (Reason + Act)
- Model Context Protocol (MCP)
- Agent Memory
- Autonomous Browser Agents
- Live Demos

**Duration**: 60-90 minutes with live demos

---

## 🛠️ Dependencies

### Core Agent Framework
- `langchain` - Core LangChain library
- `langchain-core` - Core abstractions
- `langchain-openai` - Azure OpenAI integration
- `langgraph` - Graph-based agent framework
- `python-dotenv` - Environment variable management
- `typing-extensions` - Enhanced type hints

### Browser Agent Additional Dependencies
- `websockets` - WebSocket client for CDP communication
- `httpx` - Async HTTP client
- `pydantic` - Data validation

All dependencies are listed in `requirements.txt`.

## 🐛 Troubleshooting

### Import Errors
- Ensure you've activated the virtual environment: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

### Azure API Errors
- Verify your `.env` file has correct credentials
- Check that your Azure deployment is active
- Ensure your API version matches your deployment
- **Temperature errors**: Some models (like gpt-4o-mini) only support default temperature values

### Browser Agent Issues
- **Chrome not found**: Install Chrome or Chromium browser
- **Connection errors**: Check if port 9222 is available
- **Element not clickable**: Elements may be hidden or require scrolling
- **Login fails**: Verify credentials are correct and site is accessible

## 🔑 Key Concepts

### Function Calling (Tool Usage)
LLMs can call predefined functions to interact with external systems. The LLM decides which function to call based on user input, and your code executes the actual function.

### LangGraph
A framework for building stateful, multi-actor applications with LLMs. Uses a graph structure where nodes represent operations and edges define the flow.

### ReAct Pattern
**Reason** → **Act** → **Observe** → Repeat. An agent pattern where the LLM:
1. Reasons about what to do
2. Takes an action (calls a tool)
3. Observes the result
4. Repeats until task complete

### Autonomous Agents
Agents that can perceive their environment, make decisions, and take actions to accomplish goals without constant human guidance.

## 📚 Additional Resources

- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Azure OpenAI Documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)

## 🤝 Contributing

This is an educational demo project. Feel free to:
- Fork and experiment
- Submit issues for bugs
- Share your own agent implementations
- Improve documentation

## 📄 License

This is a demo project for educational purposes.

## 🙏 Credits

Built with:
- [LangChain](https://www.langchain.com/) - LLM application framework
- [LangGraph](https://github.com/langchain-ai/langgraph) - Graph-based workflows
- [Azure OpenAI](https://azure.microsoft.com/en-us/products/ai-services/openai-service) - LLM API
- Inspired by [browser-use](https://github.com/browser-use/browser-use) for browser automation patterns

---

**Happy Building! 🚀**
