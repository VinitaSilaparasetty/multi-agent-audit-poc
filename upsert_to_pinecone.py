import json
import os
from dotenv import load_dotenv
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer

load_dotenv()
embed_model = SentenceTransformer("BAAI/bge-m3", trust_remote_code=True)
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))

# Load the 3-item catalog
with open('synthetic_catalog.json', 'r') as f:
    products = json.load(f)

# DELETE old data to prevent "Ghost Results"
print("Clearing old vectors...")
index.delete(delete_all=True)

# Upload new data
vectors = []
for p in products:
    text_to_embed = f"{p['Product Name']} {p['category']} {p['description']}"
    v = embed_model.encode(text_to_embed).tolist()
    vectors.append({
        "id": p['SKU ID'],
        "values": v,
        "metadata": {
            "name": p['Product Name'],
            "category": p['category'],
            "description": p['description'],
            "price": p['price']
        }
    })

index.upsert(vectors=vectors)
print("Successfully synced 3-item catalog to Pinecone!")
