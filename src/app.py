import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from flask import Flask, request, jsonify, render_template
import main_graph

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message", "")
    config = {"configurable": {"thread_id": "final-debug-session"}}
    
    try:
        # Invoke graph
        final_state = main_graph.app.invoke({"query": user_message}, config=config)
        
        # Pull data with fallback defaults
        outcome = final_state.get("agent_outcome", "The agent processed your request but returned no text.")
        logs = final_state.get("compliance_logs", ["Audit complete (No logs generated)"])
        
        # Terminal Debugging
        print(f"\n--- AUDIT DATA SENT TO UI ---")
        print(f"Outcome: {outcome}")
        print(f"Logs: {logs}")
        
        return jsonify({
            "agent_outcome": outcome,
            "compliance_logs": logs
        })
    except Exception as e:
        print(f"❌ Backend Error: {e}")
        return jsonify({"agent_outcome": f"Error: {str(e)}", "compliance_logs": ["Audit failed"]}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True, use_reloader=False)
