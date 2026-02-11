import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

risk_keywords = ["password", "credit card", "ssn", "bank", "otp"]

def analyze_text(text: str) -> dict:
    flags = [kw for kw in risk_keywords if kw.lower() in text.lower()]

    prompt = f"""You are a cybersecurity assistant.
    Classify this text as Safe, Suspicious, or Dangerous.
    Give a reason and a safer rewrite suggestion if needed.
    Text: {text}"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        advice = response.choices[0].message.content.strip()
    except Exception as e:
        advice = f"Error calling OpenAI: {str(e)}"

    return {"flags": flags, "advice": advice}
