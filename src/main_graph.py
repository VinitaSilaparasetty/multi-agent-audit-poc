import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from src.state.schema import AgentState
from src.agents.logic import shopping_agent, order_agent

load_dotenv()

# Configuration for Llama 3.2 via Groq
llm = ChatOpenAI(
    model="llama-3.2-3b-preview", 
    openai_api_base="https://api.groq.com/openai/v1",
    openai_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

# Initialize Memory (The Checkpointer)
memory = MemorySaver()

# Initialize the Graph
workflow = StateGraph(AgentState)

# Define Nodes
workflow.add_node("shopping_agent", shopping_agent)
workflow.add_node("order_gate", order_agent)

# Build Edges
workflow.set_entry_point("shopping_agent")
workflow.add_edge("shopping_agent", "order_gate")
workflow.add_edge("order_gate", END)

# Compile with BOTH the interrupt AND the checkpointer
app = workflow.compile(
    checkpointer=memory,
    interrupt_before=["order_gate"]
)
