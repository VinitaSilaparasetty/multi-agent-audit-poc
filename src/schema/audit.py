
from pydantic import BaseModel, Field

from datetime import datetime

from typing import List, Optional, Any



class AuditEntry(BaseModel):

    """

    Schema for EU AI Act Article 12 Compliance.

    Captures the 'Who, What, When, and Why' of AI decisions.

    """

    timestamp: datetime = Field(default_factory=datetime.utcnow)

    node_name: str  # Which agent/node made the decision

    event_type: str  # 'inference', 'data_match', 'human_intervention'

    input_data: Any  # The prompt or search query

    output_data: Any # The recommendation or action

    reference_db: Optional[str] = "product_catalog_v1" # Database version used

    human_verifier_id: Optional[str] = None # Linked to Art. 14 Human Oversight

    rationale: str # Why this path was taken (explanation for auditors)



class ComplianceState(BaseModel):

    """The shared state for our LangGraph agents."""

    query: str

    results: List[dict] = []

    selected_product: Optional[str] = None

    is_approved: bool = False

    # The Audit Trail: A list of entries that forms the 'Black Box' record

    audit_trail: List[AuditEntry] = []

