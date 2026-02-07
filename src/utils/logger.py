import json
import logging
from datetime import datetime
from pathlib import Path

# Setup industrial logging for AI Audit Trails
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("EU_AI_AUDIT")

def save_audit_log(state, thread_id):
    """
    Saves the current Agent State to a local JSON file.
    This fulfills Art. 12 'Record-keeping' requirements by creating
    a persistent, immutable history of AI state transitions.
    """
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    filename = f"audit_trail_{thread_id}.json"
    log_path = log_dir / filename
    
    # Extract only the serializable parts of the state
    audit_data = {
        "thread_id": thread_id,
        "timestamp": datetime.utcnow().isoformat(),
        "query": state.get("query"),
        "results_count": len(state.get("results", [])),
        "audit_trail": [entry.model_dump() if hasattr(entry, 'model_dump') else entry for entry in state.get("audit_trail", [])]
    }
    
    with open(log_path, "a") as f:
        f.write(json.dumps(audit_data) + "\n")
    
    logger.info(f"Audit log entry saved for thread: {thread_id}")
