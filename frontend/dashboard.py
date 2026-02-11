import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/analyze")

st.set_page_config(page_title="AI Guardian Dashboard", page_icon="🛡️")

st.title("🛡️ AI Guardian – Cyber Wellness Dashboard")
st.write("Scan text messages or emails for privacy & data-leak risks.")

text_input = st.text_area("Paste message or email:", height=200)
if st.button("Analyze"):
    if text_input.strip():
        with st.spinner("Analyzing via FastAPI + LLM..."):
            resp = requests.post(API_URL, json={"text": text_input})
            if resp.status_code == 200:
                analysis = resp.json()["analysis"]
                st.subheader("🧾 Results")
                st.json(analysis)
            else:
                st.error(f"Error: {resp.status_code} - {resp.text}")
