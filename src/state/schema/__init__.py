from typing import TypedDict, List
from pydantic import BaseModel, Field
from datetime import datetime, timezone

class AuditEntry(BaseModel):
    # Updated to use timezone-aware UTC to clear Python 3.12 warnings
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    node_name: str
    ev_rationale: str

class AgentState(TypedDict):
    query: str
    results: List[dict]
    is_approved: bool
    selected_product: str
    audit_trail: List[AuditEntry]
