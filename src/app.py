from flask import Flask, request, jsonify
from src.main_graph import app as agent_graph
from src.utils.logger import save_audit_log

app = Flask(__name__)

@app.route("/process", methods=["POST"])
def process_request():
    """Starts the agentic flow and pauses at the human checkpoint."""
    data = request.json
    thread_id = data.get("thread_id", "default_thread")
    config = {"configurable": {"thread_id": thread_id}}
    
    # Initialize the state and run until the 'order' node (the interrupt)
    initial_state = {
        "query": data.get("query"),
        "audit_trail": []
    }
    
    agent_graph.invoke(initial_state, config)
    return jsonify({"status": "pending_approval", "message": "AI has ranked products. Awaiting human oversight."})

@app.route("/approve", methods=["POST"])
def approve_action():
    """Resumes the flow after human verification and saves the audit trail."""
    data = request.json
    thread_id = data.get("thread_id")
    config = {"configurable": {"thread_id": thread_id}}
    
    # Update state with human approval flag
    agent_graph.update_state(config, {"is_approved": True, "selected_product": data.get("product")})
    
    # Resume the graph to finish the 'order' node
    final_state = agent_graph.invoke(None, config)
    
    # MANDATORY COMPLIANCE STEP: Save the state to the Audit Log
    save_audit_log(final_state, thread_id)
    
    return jsonify({
        "status": "success", 
        "message": "Order processed and logged to Audit Trail.",
        "log_reference": f"audit_trail_{thread_id}.json"
    })

if __name__ == "__main__":
    app.run(port=5000, debug=True)
