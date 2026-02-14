import ollama
import time
import json
import re

risk_keywords = ["password", "credit card", "ssn", "bank", "otp", "pin", "login", "credentials"]

# Cache the model to avoid reloading
_model_loaded = False

def ensure_model_loaded():
    global _model_loaded
    if not _model_loaded:
        # Warm up the model with a simple request
        try:
            print("🔄 Loading AI model (first time may take 30-60 seconds)...")
            ollama.chat(
                model='llama3.2:3b',
                messages=[{'role': 'user', 'content': 'Hello'}],
                options={'num_ctx': 2048}
            )
            _model_loaded = True
            print("✅ Model loaded and ready!")
        except Exception as e:
            print(f"⚠️ Model not ready: {e}")

def analyze_text(text: str) -> dict:
    # Ensure model is loaded (first call only)
    ensure_model_loaded()
    
    # Start timing
    start_time = time.time()
    
    flags = [kw for kw in risk_keywords if kw.lower() in text.lower()]
    
    # Calculate risk level based on flags
    risk_level = len(flags) * 20
    risk_level = min(risk_level, 100)
    
    # Create a better prompt
    prompt = f"""You are a cybersecurity expert. Analyze this message and respond in this exact JSON format:
{{
    "classification": "Safe/Suspicious/Dangerous",
    "confidence": "High/Medium/Low",
    "reason": "Brief explanation",
    "safe_rewrite": "A safer version of the message",
    "tips": ["Tip 1", "Tip 2", "Tip 3"]
}}

Message: {text}"""

    try:
        response = ollama.chat(
            model='llama3.2:3b',
            messages=[{'role': 'user', 'content': prompt}],
            options={'num_ctx': 2048}
        )
        advice = response['message']['content'].strip()
        
        # Try to parse JSON from response
        json_match = re.search(r'\{.*\}', advice, re.DOTALL)
        if json_match:
            try:
                parsed = json.loads(json_match.group())
                advice = parsed
            except:
                advice = {"text": advice, "flags": flags}
        else:
            advice = {"text": advice, "flags": flags}
            
    except Exception as e:
        advice = {
            "text": f"Local model warming up...",
            "flags": flags,
            "error": str(e)
        }
    
    # Calculate processing time
    process_time = time.time() - start_time
    
    return {
        "flags": flags,
        "risk_level": risk_level,
        "advice": advice,
        "processing_time": round(process_time, 2)
    }
