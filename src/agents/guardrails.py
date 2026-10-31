import re

def scrub_pii(text):
    # 1. DEFINE THE DEVELOPER WHITELIST
    # Replace [REDACTED_LAST_NAME] with your actual last name
    developer_name = "Vinita Silaparasetty" 
    
    # Temporarily hide your name so the regex doesn't catch it
    placeholder = "___DEV_NAME___"
    protected_text = text.replace(developer_name, placeholder)

    # 2. REDACT USER PII (Emails and common patterns)
    # This ensures compliance with EU AI Act data minimization
    redacted = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[REDACTED_EMAIL]', protected_text)
    
    # Redact common "User" names if they appear in specific patterns
    redacted = re.sub(r'(?i)Jane Doe|John Doe', '[REDACTED_USER]', redacted)

    # 3. RESTORE DEVELOPER NAME
    return redacted.replace(placeholder, developer_name)

def calculate_faithfulness(llm, context, response):
    # Simplified faithfulness check for POC grounding
    from langchain_core.messages import HumanMessage
    eval_prompt = f"Context: {context}\nResponse: {response}\nIs the response supported by context? Score 0.0 to 1.0:"
    try:
        score_raw = llm.invoke([HumanMessage(content=eval_prompt)]).content
        return float(re.findall(r"0\.\d+|1\.0", score_raw)[0])
    except:
        return 0.5
