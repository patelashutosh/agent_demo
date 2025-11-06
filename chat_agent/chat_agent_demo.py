import os
import json
from dotenv import load_dotenv
from typing import Annotated
from typing_extensions import TypedDict

from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    ToolMessage,
    AIMessage,
)
from langchain_core.tools import tool
from langchain_openai import AzureChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

# --- 1. Load Environment Variables ---
# Make sure to create a .env file with your Azure credentials
load_dotenv()

# Check for essential environment variables
if "AZURE_OPENAI_ENDPOINT" not in os.environ:
    raise EnvironmentError(
        "AZURE_OPENAI_ENDPOINT not found in .env file."
        "Please add: AZURE_OPENAI_ENDPOINT='https://your-endpoint.openai.azure.com/'"
    )
if "AZURE_OPENAI_API_KEY" not in os.environ:
    raise EnvironmentError(
        "AZURE_OPENAI_API_KEY not found in .env file. Please add: AZURE_OPENAI_API_KEY='your-api-key'"
    )
if "OPENAI_API_VERSION" not in os.environ:
    raise EnvironmentError(
        "OPENAI_API_VERSION not found in .env file."
        "Please add: OPENAI_API_VERSION='2024-02-01' (or your API version)"
    )
if "AZURE_OPENAI_CHAT_DEPLOYMENT_NAME" not in os.environ:
    raise EnvironmentError(
        "AZURE_OPENAI_CHAT_DEPLOYMENT_NAME not found in .env file."
        "Please add: AZURE_OPENAI_CHAT_DEPLOYMENT_NAME='your-deployment-name'"
    )


# --- 2. Define Mock Tools ---

@tool
def get_stock_price(symbol: str) -> str:
    """
    Get the current stock price for stocks (NSE/BSE).
    
    Args:
        symbol: The stock symbol (e.g., RELIANCE, TCS, INFY, HDFCBANK).
    """
    print(f"--- Calling get_stock_price tool for {symbol} ---")
    # In a real app, you'd call a stock API here (e.g., Yahoo Finance, Alpha Vantage).
    # For this demo, we'll return mock responses.
    
    stock_data = {
        "reliance": {
            "company": "Reliance Industries Ltd",
            "price": "₹2,450.50",
            "change": "+15.25 (+0.63%)",
            "exchange": "NSE"
        },
        "tcs": {
            "company": "Tata Consultancy Services",
            "price": "₹3,680.00",
            "change": "-22.50 (-0.61%)",
            "exchange": "NSE"
        },
        "infy": {
            "company": "Infosys Ltd",
            "price": "₹1,420.75",
            "change": "+8.90 (+0.63%)",
            "exchange": "NSE"
        },
        "hdfcbank": {
            "company": "HDFC Bank Ltd",
            "price": "₹1,650.20",
            "change": "+12.30 (+0.75%)",
            "exchange": "NSE"
        },
        "wipro": {
            "company": "Wipro Ltd",
            "price": "₹450.35",
            "change": "-3.15 (-0.69%)",
            "exchange": "NSE"
        }
    }
    
    symbol_lower = symbol.lower().replace(".ns", "")
    
    if symbol_lower in stock_data:
        data = stock_data[symbol_lower]
        return json.dumps(data)
    else:
        return json.dumps({
            "company": symbol,
            "price": "₹1,250.00",
            "change": "+5.00 (+0.40%)",
            "exchange": "NSE"
        })


@tool
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """
    Convert currency from one denomination to another.
    
    Args:
        amount: The amount to convert.
        from_currency: Source currency code (e.g., USD, INR, EUR, GBP).
        to_currency: Target currency code (e.g., USD, INR, EUR, GBP).
    """
    print(f"--- Calling convert_currency tool: {amount} {from_currency} to {to_currency} ---")
    # In a real app, you'd call a currency API here (e.g., exchangerate-api.com, fixer.io).
    # For this demo, we'll use approximate exchange rates.
    
    # Exchange rates (as of example date, relative to INR)
    rates_to_inr = {
        "inr": 1.0,
        "usd": 83.0,
        "eur": 90.0,
        "gbp": 105.0,
        "jpy": 0.55,
        "aed": 22.6,
        "sgd": 62.0,
        "cad": 61.0,
        "aud": 55.0
    }
    
    from_curr = from_currency.lower()
    to_curr = to_currency.lower()
    
    if from_curr not in rates_to_inr or to_curr not in rates_to_inr:
        return json.dumps({
            "error": f"Unsupported currency: {from_currency} or {to_currency}",
            "supported": "USD, INR, EUR, GBP, JPY, AED, SGD, CAD, AUD"
        })
    
    # Convert to INR first, then to target currency
    amount_in_inr = amount * rates_to_inr[from_curr]
    converted_amount = amount_in_inr / rates_to_inr[to_curr]
    
    return json.dumps({
        "from": f"{amount} {from_currency.upper()}",
        "to": f"{converted_amount:.2f} {to_currency.upper()}",
        "rate": f"1 {from_currency.upper()} = {rates_to_inr[from_curr] / rates_to_inr[to_curr]:.4f} {to_currency.upper()}"
    })


@tool
def get_cricket_score(match_type: str = "live") -> str:
    """
    Get live or recent cricket match scores.
    
    Args:
        match_type: Type of match info to retrieve - "live", "recent", or "upcoming".
    """
    print(f"--- Calling get_cricket_score tool for {match_type} matches ---")
    # In a real app, you'd call a cricket API here (e.g., Cricbuzz API, ESPN Cricinfo).
    # For this demo, we'll return mock match data.
    
    if match_type == "live":
        return json.dumps({
            "status": "live",
            "match": "India vs Australia - 3rd ODI",
            "venue": "Narendra Modi Stadium, Ahmedabad",
            "score": "India: 289/7 (48.2 overs) | Target: 287",
            "current": "India need 8 runs to win from 10 balls",
            "batsmen": "Hardik Pandya 45* (32), Ravindra Jadeja 28* (19)"
        })
    elif match_type == "recent":
        return json.dumps({
            "status": "completed",
            "match": "India vs South Africa - 2nd T20I",
            "result": "India won by 16 runs",
            "scores": "India: 180/7 (20 overs) | South Africa: 164/8 (20 overs)",
            "player_of_match": "Suryakumar Yadav (68 off 40)"
        })
    else:  # upcoming
        return json.dumps({
            "status": "upcoming",
            "match": "India vs England - 1st Test",
            "venue": "Rajiv Gandhi International Stadium, Hyderabad",
            "date": "January 25, 2025",
            "time": "09:30 AM IST"
        })


# --- 3. Define the Agent State ---
# This TypedDict defines the structure of our agent's state.
# The `add_messages` function ensures new messages are appended to the list
# instead of replacing it.
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


# --- 4. Initialize LLM and Tools ---

# Initialize the AzureChatOpenAI model
# It will automatically read the AZURE_OPENAI_API_KEY from the environment
# Configured with retry logic for rate limit handling
llm = AzureChatOpenAI(
    api_version=os.environ["OPENAI_API_VERSION"],
    azure_deployment=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    max_retries=5,  # Retry up to 5 times on failures (handles rate limits)
    timeout=60.0,   # 60 second timeout per request
    # The OpenAI client automatically handles exponential backoff for 429 errors
)

# Create a list of tools our agent can use
tools = [get_stock_price, convert_currency, get_cricket_score]

# Bind the tools to the LLM. This tells the LLM it can call these tools.
llm_with_tools = llm.bind_tools(tools)

# The ToolNode is a prebuilt LangGraph node that executes tools.
# We wrap it as action_node to represent action execution.
action_node = ToolNode(tools)


# --- 5. Define Graph Nodes ---

# This node handles observation and planning. It calls the LLM to analyze
# the current state (messages) and plan the next action.
def observe_and_plan(state: AgentState) -> dict:
    """
    Observe the current conversation state and plan the next action.
    
    The model analyzes the messages and decides to either:
    - Respond directly with an answer, or
    - Issue a tool call to gather more information
    """
    print("--- Observing & Planning (Calling LLM) ---")
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    # The response (an AIMessage) is added to the state
    return {"messages": [response]}


# --- 6. Construct the Graph ---
print("Constructing LangGraph agent...")
graph_builder = StateGraph(AgentState)

# Add the two nodes to the graph
graph_builder.add_node("observe_and_planning", observe_and_plan)
graph_builder.add_node("action", action_node)  # Execute actions (tool calls)

# The entry point is the "observe_and_planning" node
graph_builder.set_entry_point("observe_and_planning")

# This conditional edge routes the flow *after* the "observe_and_planning" node runs.
# It checks the last message (the AIMessage from `observe_and_plan`):
# - If it contains tool calls, it routes to the "action" node.
# - Otherwise, it routes to END, finishing the graph execution.
graph_builder.add_conditional_edges(
    "observe_and_planning",
    tools_condition,  # This is a prebuilt function
    {
        "tools": "action",  # Route to "action" node if tool calls are present
        END: END,  # Otherwise, end the flow
    },
)

# This edge routes the flow *after* the "action" node runs.
# The output of the actions (ToolMessages) is sent back to the "observe_and_planning" node
# so the LLM can process the tool results and generate a final answer.
graph_builder.add_edge("action", "observe_and_planning")

# Compile the state graph into a runnable graph
graph = graph_builder.compile()
print("✅ Graph compiled successfully!")


# --- 7. Run the Demo ---

print("\n" + "=" * 70)
print("🚀 DEMO 1: Query that requires tool call - Stock Price")
print("=" * 70)

# We use .stream() to see all the steps in the graph
# The input is a dictionary matching the AgentState
inputs_stock = {
    "messages": [HumanMessage(content="What is the current price of TCS stock?")]
}

for event in graph.stream(inputs_stock, stream_mode="values"):
    # `stream_mode="values"` yields the full state at each step
    latest_message = event["messages"][-1]
    print(f"\nNode: '{event.get('__key__', 'entry')}'")
    print("---")
    latest_message.pretty_print()
    if isinstance(latest_message, AIMessage) and latest_message.tool_calls:
        print(f"Tool Call: {latest_message.tool_calls[0]['name']}")
    elif isinstance(latest_message, ToolMessage):
        print(f"Tool Result: {latest_message.content}")

print("\n" + "=" * 70)
print("🚀 DEMO 2: Query that requires tool call - Currency Conversion")
print("=" * 70)

inputs_currency = {
    "messages": [HumanMessage(content="Convert 100 USD to INR")]
}

for event in graph.stream(inputs_currency, stream_mode="values"):
    latest_message = event["messages"][-1]
    print(f"\nNode: '{event.get('__key__', 'entry')}'")
    print("---")
    latest_message.pretty_print()
    if isinstance(latest_message, AIMessage) and latest_message.tool_calls:
        print(f"Tool Call: {latest_message.tool_calls[0]['name']}")
    elif isinstance(latest_message, ToolMessage):
        print(f"Tool Result: {latest_message.content}")

print("\n" + "=" * 70)
print("🚀 DEMO 3: Query that requires tool call - Cricket Scores")
print("=" * 70)

inputs_cricket = {
    "messages": [HumanMessage(content="What are the live cricket scores?")]
}

for event in graph.stream(inputs_cricket, stream_mode="values"):
    latest_message = event["messages"][-1]
    print(f"\nNode: '{event.get('__key__', 'entry')}'")
    print("---")
    latest_message.pretty_print()
    if isinstance(latest_message, AIMessage) and latest_message.tool_calls:
        print(f"Tool Call: {latest_message.tool_calls[0]['name']}")
    elif isinstance(latest_message, ToolMessage):
        print(f"Tool Result: {latest_message.content}")

print("\n" + "=" * 70)
print("🚀 DEMO 4: Query that does NOT require a tool call")
print("=" * 70)

inputs_no_tool = {"messages": [HumanMessage(content="Hi, my name is Ashutosh. Nice to meet you!")]}

for event in graph.stream(inputs_no_tool, stream_mode="values"):
    latest_message = event["messages"][-1]
    print(f"\nNode: '{event.get('__key__', 'entry')}'")
    print("---")
    latest_message.pretty_print()


