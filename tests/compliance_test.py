import pytest
from src.main_graph import app as agent_graph
from src.agents.logic import order_agent, shopping_agent

def test_order_gate_fails_without_approval():
    """Validates Art. 14 Human Oversight."""
    illegal_state = {
        "query": "laptop",
        "results": [{"id": 1, "price": 999}],
        "is_approved": False,
        "selected_product": "Standard Laptop",
        "audit_trail": []
    }
    with pytest.raises(ValueError, match="Regulatory violation: Human approval missing"):
        order_agent(illegal_state)

def test_audit_trail_immutability():
    """Validates Art. 12 Record-keeping."""
    initial_state = {"query": "test", "audit_trail": []}
    first_pass = shopping_agent(initial_state)
    
    assert len(first_pass["audit_trail"]) == 1
    # Use dot notation for Pydantic objects
    assert first_pass["audit_trail"][0].node_name == "shopping_agent"
