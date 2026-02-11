import re

def find_pii(text: str):
    patterns = {
        "emails": re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text),
        "phones": re.findall(r"\+?\d[\d\- ]{7,}\d", text),
    }
    return {k: v for k, v in patterns.items() if v}
