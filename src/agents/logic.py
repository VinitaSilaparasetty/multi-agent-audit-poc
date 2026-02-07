
from src.schema.audit import AuditEntry



def shopping_agent(state):

    """Node: Recommends products and logs the event for traceability."""

    results = [{"id": 1, "name": "Standard Laptop", "price": 999}]

    

    # Create the Audit Entry (Mandatory for Compliance)

    new_entry = AuditEntry(

        node_name="shopping_agent",

        event_type="inference",

        input_data=state["query"],

        output_data=results,

        rationale="Top results based on keyword relevance."

    )

    

    return {

        "results": results,

        "audit_trail": state["audit_trail"] + [new_entry]

    }



def order_agent(state):

    """Node: Processes the order ONLY if human approved."""

    if not state.get("is_approved"):

        raise ValueError("Regulatory violation: Human approval missing for order.")

        

    new_entry = AuditEntry(

        node_name="order_agent",

        event_type="human_intervention",

        input_data=state["selected_product"],

        output_data="Order Processed",

        human_verifier_id="operator_01", # ID of the person who hit 'Approve'

        rationale="Human operator verified price and availability."

    )

    

    return {

        "audit_trail": state["audit_trail"] + [new_entry]

    }

