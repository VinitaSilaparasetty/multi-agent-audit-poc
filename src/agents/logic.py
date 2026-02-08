from datetime import datetime, timezone
from src.state.schema import AuditEntry

def shopping_agent(state):
    """Simulates a shopping search and adds an audit entry."""
    entry = AuditEntry(
        node_name="shopping_agent",
        ev_rationale="Top results based on keyword relevance."
    )
    # Ensure any manual datetime calls use timezone.utc
    new_trail = state.get("audit_trail", []) + [entry]
    return {"results": [{"id": 1, "name": "Standard Laptop", "price": 999}], "audit_trail": new_trail}

def order_agent(state):
    """Checks for human approval before 'processing' an order."""
    if not state.get("is_approved"):
        raise ValueError("Regulatory violation: Human approval missing (Art. 14)")
    
    entry = AuditEntry(
        node_name="order_agent",
        ev_rationale="Transaction finalized after human verification."
    )
    new_trail = state.get("audit_trail", []) + [entry]
    return {"audit_trail": new_trail}
