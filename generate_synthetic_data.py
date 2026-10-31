import json
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

def generate_catalog():
    # Use Groq via the OpenAI compatibility layer
    llm = ChatOpenAI(
        model="llama-3.1-8b-instant",
        openai_api_key=os.getenv("GROQ_API_KEY"),
        openai_api_base="https://api.groq.com/openai/v1"
    )
    
    print("🤖 Generating synthetic products via Groq...")
    
    prompt = """
    Generate a JSON list of 10 consumer electronics for a store catalog. 
    Each must have exactly these keys: 'SKU ID', 'Product Name', 'price', 'category', and 'description'.
    Return ONLY the raw JSON list. No markdown blocks.
    """
    
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        content = response.content.strip()
        
        # Simple cleanup if the LLM includes markdown
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        with open('synthetic_catalog.json', 'w') as f:
            f.write(content)
        print("✅ Created synthetic_catalog.json")
    except Exception as e:
        print(f"❌ Generation failed: {e}")

if __name__ == "__main__":
    generate_catalog()
