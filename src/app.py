from flask import Flask, request, jsonify
from src.main_graph import app as agent_graph
import uuid

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>Multi-Agent Audit POC</h1><p>API is running. Use <b>/process</b> or <b>/approve</b> endpoints to interact.</p>"

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    thread_id = data.get("thread_id", str(uuid.uuid4()))
    config = {"configurable": {"thread_id": thread_id}}
    
    # Run the graph
    result = agent_graph.invoke({"query": data["query"]}, config)
    
    # FIX: Convert Pydantic objects to dictionaries so Flask can serialize them
    if "audit_trail" in result:
        result["audit_trail"] = [entry.model_dump() if hasattr(entry, 'model_dump') else entry for entry in result["audit_trail"]]
    
    return jsonify({"status": "pending_approval", "thread_id": thread_id, "data": result})

@app.route('/approve', methods=['POST'])
def approve():
    data = request.json
    thread_id = data.get("thread_id")
    config = {"configurable": {"thread_id": thread_id}}
    
    agent_graph.update_state(config, {"is_approved": True})
    result = agent_graph.invoke(None, config)
    
    # FIX: Convert Pydantic objects to dictionaries here as well
    if "audit_trail" in result:
        result["audit_trail"] = [entry.model_dump() if hasattr(entry, 'model_dump') else entry for entry in result["audit_trail"]]
        
    return jsonify({"status": "completed", "data": result})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
