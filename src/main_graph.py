import os
from typing import TypedDict, List, Annotated
import operator
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

class AgentState(TypedDict):
    query: str
    results: List[dict]
    compliance_logs: Annotated[List[str], operator.add]
    agent_outcome: str

from agents.logic import shopping_agent, order_agent, poc_notice_agent

load_dotenv()
llm = ChatOpenAI(model="llama-3.1-8b-instant", openai_api_key=os.getenv("GROQ_API_KEY"), openai_api_base="https://api.groq.com/openai/v1")

def router(state):
    q = state["query"].lower()
    # Active Demo Intents
    if any(word in q for word in ["buy", "purchase", "pay", "order"]):
        return "order"
    # Placeholder for non-demo intents
    if any(word in q for word in ["refund", "status", "help", "broken", "return"]):
        return "notice"
    return "shopping"

workflow = StateGraph(AgentState)
workflow.add_node("shopping", shopping_agent)
workflow.add_node("order", order_agent)
workflow.add_node("notice", poc_notice_agent)

workflow.set_conditional_entry_point(router, {"shopping": "shopping", "order": "order", "notice": "notice"})
workflow.add_edge("shopping", END)
workflow.add_edge("order", END)
workflow.add_edge("notice", END)

app = workflow.compile()
