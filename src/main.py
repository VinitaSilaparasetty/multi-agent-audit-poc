
from langgraph.graph import StateGraph, END

from langgraph.checkpoint.memory import MemorySaver

from src.agents.logic import shopping_agent, order_agent



workflow = StateGraph(dict) # In production, use your Pydantic schema



workflow.add_node("shop", shopping_agent)

workflow.add_node("order", order_agent)



workflow.set_entry_point("shop")

workflow.add_edge("shop", "order")

workflow.add_edge("order", END)



# Persistence is the key to Auditability

memory = MemorySaver()



# Compile with an INTERRUPT before the order for EU Art. 14 compliance

app = workflow.compile(checkpointer=memory, interrupt_before=["order"])

