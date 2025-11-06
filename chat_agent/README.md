# Chat Agent with Tool Calling

This demo shows how to build a conversational AI agent using **LangChain**, **LangGraph**, and **Azure OpenAI** with multiple tools.

## 🎯 What This Demo Shows

This example demonstrates:
- **LangGraph State Management**: Using TypedDict to define agent state
- **Tool Calling (Function Calling)**: LLM decides which tools to call based on user queries
- **Multiple Tools**: Agent has access to 3 different tools
- **ReAct Pattern**: Observe → Plan → Act → Repeat cycle

## 🛠️ Available Tools

The agent can use these tools:

### 1. Stock Price Checker 📈
Get real-time stock prices for companies (NSE/BSE):
- **Examples**: TCS, Infosys, Reliance, HDFC Bank, Wipro
- **Returns**: Current price, change, percentage, exchange

### 2. Currency Converter 💱
Convert between different currencies:
- **Supported**: USD, INR, EUR, GBP, JPY, AED, SGD, CAD, AUD
- **Returns**: Converted amount and exchange rate

### 3. Cricket Score Tracker 🏏
Get live, recent, or upcoming cricket match information:
- **Types**: Live scores, recent results, upcoming matches
- **Returns**: Match details, scores, player stats

## 🏗️ Architecture

```
User Query → Observe & Plan Node (LLM) → Decision
                                             ↓
                                    Tool Call? 
                                    /        \
                                  Yes         No
                                   ↓           ↓
                          Action Node      Response
                          (Execute Tool)      ↓
                                ↓            End
                          Back to LLM
                          (Process Result)
                                ↓
                           Final Response
```

### Graph Nodes

1. **observe_and_planning**: 
   - Analyzes current conversation state
   - Decides whether to call a tool or respond directly
   - Uses LLM with tool definitions

2. **action**: 
   - Executes the selected tool
   - Returns results to the graph state

### Graph Flow

- **Entry Point**: `observe_and_planning`
- **Conditional Edge**: Based on whether LLM made a tool call
  - If tool call → go to `action` node
  - If no tool call → END (return response)
- **Loop**: `action` → back to `observe_and_planning` (to process tool results)

## 📦 Code Structure

```python
# 1. Define Tools using @tool decorator
@tool
def get_stock_price(symbol: str) -> str:
    """Get stock price for stocks"""
    # Tool implementation
    
# 2. Define Agent State
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# 3. Create Graph
graph_builder = StateGraph(AgentState)
graph_builder.add_node("observe_and_planning", observe_and_plan)
graph_builder.add_node("action", action_node)
graph_builder.add_conditional_edges("observe_and_planning", tools_condition, {...})
graph = graph_builder.compile()

# 4. Run Agent
result = graph.stream({"messages": [user_message]})
```

## 🚀 Running the Demo

### Prerequisites
1. Python 3.8+
2. Azure OpenAI account with credentials in `.env` file

### Run
```bash
cd chat_agent
python chat_agent_demo.py
```

### Expected Output

The demo runs 4 scenarios:

**Demo 1**: Stock Price Query
```
User: "What is the current price of TCS stock?"
→ LLM calls get_stock_price("TCS")
→ Tool returns: {"company": "Tata Consultancy Services", "price": "₹3,680.00", ...}
→ LLM responds: "The current price of TCS is ₹3,680.00, down by 0.61%"
```

**Demo 2**: Currency Conversion
```
User: "Convert 100 USD to INR"
→ LLM calls convert_currency(100, "USD", "INR")
→ Tool returns: {"from": "100 USD", "to": "8300.00 INR", ...}
→ LLM responds: "100 USD is equal to ₹8,300.00"
```

**Demo 3**: Cricket Scores
```
User: "What are the live cricket scores?"
→ LLM calls get_cricket_score("live")
→ Tool returns: {"match": "India vs Australia", "score": ..., ...}
→ LLM responds: "India is currently playing Australia. India needs 8 runs..."
```

**Demo 4**: No Tool Needed
```
User: "Hi, my name is Priya. Nice to meet you!"
→ LLM responds directly without calling any tool
→ "Hello Priya! Nice to meet you too!"
```

## 🔑 Key Concepts

### 1. **Tool/Function Calling**
- LLM can "call" predefined functions when needed
- LLM provides function name + arguments as structured output
- Your code executes the actual function
- Result goes back to LLM to formulate final response

### 2. **LangGraph State Graph**
- Graph-based workflow for agents
- **Nodes**: Steps in the workflow (planning, action execution)
- **Edges**: Connections between nodes
- **State**: Shared data that flows through the graph

### 3. **ReAct Pattern (Reason + Act)**
- **Observe**: Analyze current state
- **Plan**: Decide what action to take
- **Act**: Execute the action
- **Repeat**: Continue until task complete

### 4. **Tool Binding**
```python
llm_with_tools = llm.bind_tools(tools)
```
This tells the LLM what functions are available and their signatures.

## 🎓 Learning Path

1. **Start Here**: Understand how tools are defined (`@tool` decorator)
2. **Graph Structure**: See how nodes connect with conditional edges
3. **State Management**: How messages flow through the graph
4. **Tool Execution**: How ToolNode automatically executes the called function
5. **Loop Pattern**: How results come back for LLM to process

## 📚 Extension Ideas

1. **Real APIs**: Replace mock data with actual APIs
   - Stock: Yahoo Finance API, Alpha Vantage
   - Currency: exchangerate-api.com, fixer.io
   - Cricket: Cricbuzz API, ESPN Cricinfo

2. **More Tools**: Add additional tools
   - Weather information
   - News articles
   - Database queries
   - File operations

3. **Memory**: Add conversation history
   - Remember user preferences
   - Context across multiple queries
   - Vector database for long-term memory

4. **Human-in-the-Loop**: Add confirmation step
   - Ask user before executing certain actions
   - Show tool parameters before execution

## 🤔 Discussion Questions

1. What happens if LLM calls wrong tool or wrong parameters?
2. How do we handle tool execution failures?
3. When should we use tools vs. LLM's built-in knowledge?
4. How to prevent infinite loops in graph execution?
5. How to add authentication to tool calls?

## 📖 References

- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Azure OpenAI Function Calling](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/function-calling)
