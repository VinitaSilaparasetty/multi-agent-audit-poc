from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from src.agents.logic import shopping_agent, order_agent
from src.agents.ml_logic import ml_ranker_node

workflow = StateGraph(dict)

workflow.add_node("shop", shopping_agent)
workflow.add_node("ranker", ml_ranker_node)
workflow.add_node("order", order_agent)

# The logic flow: Search -> ML Rank -> Human Gate -> Order
workflow.set_entry_point("shop")
workflow.add_edge("shop", "ranker")
workflow.add_edge("ranker", "order")
workflow.add_edge("order", END)

memory = MemorySaver()
app = workflow.compile(checkpointer=memory, interrupt_before=["order"])
