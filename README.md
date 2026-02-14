# AI Guardian 🛡️ – Cyber Wellness & Data Protection Assistant

**Problem**  
Online conversations leak sensitive data every day – from OTPs and bank details to toxic language. Individuals and small businesses need a simple, private tool to scan messages before sending.

**Solution**  
AI Guardian is a privacy‑first dashboard that combines **fast regex detection** with a **local LLM (Ollama)** to classify text, detect risks, and suggest safer rewrites. No cloud API = no cost, no data leaks.

**Tech Stack**  
Python | FastAPI | Streamlit | Ollama (llama3.2) | Plotly | Regex

## Quick Start

1. Clone this repo and open in Codespace.
2. Install dependencies: `pip install -r requirements.txt`
3. Start Ollama server: `ollama serve` (keep terminal open)
4. Pull model: `ollama pull llama3.2:3b` (first time only)
5. Run backend: `uvicorn backend.main:app --reload --port 8000`
6. Run dashboard: `streamlit run frontend/dashboard.py --server.port 8501 --server.enableCORS false`
7. Open the forwarded port 8501 and paste a message!

Built for DevDash 2026 by [Your Name] – solo developer passionate about AI for social good.
