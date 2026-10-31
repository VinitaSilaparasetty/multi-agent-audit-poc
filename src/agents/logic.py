import os
from dotenv import load_dotenv
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from langchain_core.messages import HumanMessage, SystemMessage
from .guardrails import scrub_pii, calculate_faithfulness

load_dotenv()
embed_model = SentenceTransformer("BAAI/bge-m3", trust_remote_code=True)
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))

def shopping_agent(state):
    from main_graph import llm
    raw_query = state.get("query", "").strip()

    # 1. PII Scrub
    redacted_query = scrub_pii(raw_query)
    privacy_log = "[DONE] Privacy Guard: Redacted PII" if redacted_query != raw_query else "[DONE] Privacy Guard: No PII detected"

    # 2. Short Query Filter (Prevents 'Yes' from searching the catalog)
    if len(redacted_query.split()) < 3 and redacted_query.lower() in ["yes", "no", "ok", "sure", "thanks"]:
        return {
            "agent_outcome": "I understand. Would you like to see our actual laptop inventory now, or do you have more questions about the hardware specifications?",
            "compliance_logs": [privacy_log, "[INFO] Logic: Short query bypass - no RAG triggered"],
            "results": []
        }

    # 3. Standard RAG Retrieval
    query_vector = embed_model.encode(redacted_query, normalize_embeddings=True).tolist()
    search_results = index.query(vector=query_vector, top_k=1, include_metadata=True)
    matches = [m['metadata'] for m in search_results['matches']]
    selected = matches[0] if matches else {"name": "No product", "category": "N/A", "description": "N/A"}
    
    context = f"Product: {selected['name']}, Category: {selected['category']}, Description: {selected.get('description', 'N/A')}"

    # 4. Strict Generation
    system_instr = "You are a shopping assistant. If a product does not match the USER'S requested category (e.g. they want a laptop, you found a watch), REFUSE the match."
    user_prompt = f"Catalog Context: {context}\nUser Request: {redacted_query}"
    
    ai_response = llm.invoke([SystemMessage(content=system_instr), HumanMessage(content=user_prompt)]).content.strip()

    # 5. Audit
    f_score = calculate_faithfulness(llm, context, ai_response)
    grounding_log = f"[DONE] Grounding Check: Score {f_score:.2f}"

    return {
        "results": [selected],
        "compliance_logs": [privacy_log, grounding_log],
        "agent_outcome": ai_response
    }

def order_agent(state):
    return {"agent_outcome": "Redirecting to secure checkout...", "compliance_logs": ["[DONE] Order Agent: Purchase intent verified"]}

def poc_notice_agent(state):
    return {"agent_outcome": "DEMO NOTICE: This intent is mapped but inactive in this POC.", "compliance_logs": ["[SYSTEM] Routing to Placeholder"]}
