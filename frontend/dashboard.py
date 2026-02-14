import streamlit as st
import requests
import os
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import time

# Page config must be first
st.set_page_config(
    page_title="AI Guardian", 
    page_icon="🛡️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    /* Main title styling */
    .main-title {
        font-size: 3rem !important;
        color: #00ff88 !important;
        text-shadow: 0 0 10px rgba(0,255,136,0.5);
        margin-bottom: 0.5rem;
    }
    
    /* Subtitle styling */
    .subtitle {
        font-size: 1.2rem;
        color: #cccccc;
        margin-bottom: 2rem;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Result container */
    .result-container {
        background: rgba(30, 60, 114, 0.3);
        border-radius: 15px;
        padding: 2rem;
        margin-top: 2rem;
        border-left: 5px solid #00ff88;
        backdrop-filter: blur(10px);
    }
    
    /* Warning text */
    .warning-text {
        color: #ffaa00;
        font-weight: bold;
    }
    
    /* Safe text */
    .safe-text {
        color: #00ff88;
        font-weight: bold;
    }
    
    /* Danger text */
    .danger-text {
        color: #ff4444;
        font-weight: bold;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #00ff88 0%, #00cc88 100%);
        color: #1a1a2e;
        font-weight: bold;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-size: 1.2rem;
        transition: all 0.3s ease;
        box-shadow: 0 5px 20px rgba(0,255,136,0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,255,136,0.4);
    }
    
    /* Text area styling */
    .stTextArea textarea {
        background: rgba(30, 60, 114, 0.2);
        color: white;
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 15px;
        font-size: 1.1rem;
        backdrop-filter: blur(5px);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #0f2027 0%, #203a43 100%);
    }
    
    /* Stats box */
    .stats-box {
        background: rgba(255,255,255,0.05);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(255,255,255,0.1);
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/analyze")

# Initialize session state for history
if 'history' not in st.session_state:
    st.session_state.history = []
if 'total_scans' not in st.session_state:
    st.session_state.total_scans = 0
if 'total_risks' not in st.session_state:
    st.session_state.total_risks = 0

# Sidebar - Modern Design
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #00ff88;'>🛡️ AI Guardian</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Stats in sidebar
    st.markdown("### 📊 Your Protection Stats")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class='stats-box'>
            <h3 style='color: #00ff88; text-align: center;'>{st.session_state.total_scans}</h3>
            <p style='text-align: center;'>Total Scans</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='stats-box'>
            <h3 style='color: #ff4444; text-align: center;'>{st.session_state.total_risks}</h3>
            <p style='text-align: center;'>Risks Found</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Features list
    st.markdown("### ✨ Features")
    features = [
        "🔍 Real-time message scanning",
        "🤖 Local AI (privacy first!)",
        "📊 Risk score visualization",
        "🔄 Safe message rewriting",
        "📈 Usage statistics",
        "🎯 Phishing detection",
        "🔒 Data leak prevention"
    ]
    for feature in features:
        st.markdown(f"- {feature}")
    
    st.markdown("---")
    
    # About section
    with st.expander("ℹ️ About AI Guardian"):
        st.markdown("""
        **Version:** 2.0  
        **Model:** Llama 3.2 (Local)  
        **Privacy:** 100% offline  
        **Made for:** DevDash 2026
        """)

# Main content
st.markdown("<h1 class='main-title'>🛡️ AI Guardian</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Your personal cybersecurity assistant – powered by local AI</p>", unsafe_allow_html=True)

# Create tabs for different features
tab1, tab2, tab3 = st.tabs(["🔍 Message Scanner", "📈 Analytics", "⚙️ Settings"])

with tab1:
    # Main scanning interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        text_input = st.text_area(
            "Paste your message or email to analyze:",
            height=200,
            placeholder="Enter suspicious messages, emails, or text here..."
        )
        
        # Example templates
        examples = st.selectbox(
            "Try an example:",
            ["", "📧 Phishing Email", "🏦 Bank Transfer", "💬 Normal Chat", "🔑 Password Reset"]
        )
        
        if examples == "📧 Phishing Email":
            text_input = """Dear Customer,
Your account has been compromised. Click here to reset your password immediately:
http://fake-bank.com/reset
Failure to do so will result in account closure."""
            
        elif examples == "🏦 Bank Transfer":
            text_input = "Please send $5000 to account 123456789 at Bank of America. Routing number: 021000021"
            
        elif examples == "💬 Normal Chat":
            text_input = "Hey, are we still meeting for lunch at 2pm tomorrow?"
            
        elif examples == "🔑 Password Reset":
            text_input = "Your verification code is 123456. Never share this code with anyone."
    
    with col2:
        st.markdown("### 🎯 Quick Tips")
        st.info("""
        • **Dangerous:** Bank details, passwords, OTPs
        • **Suspicious:** Urgent requests, weird links
        • **Safe:** Casual conversations, general info
        """)
        
        # Risk level guide
        st.markdown("### 📊 Risk Scale")
        st.markdown("""
        <div style='background: linear-gradient(90deg, #00ff88 0%, #ffaa00 50%, #ff4444 100%); height: 20px; border-radius: 10px;'></div>
        <div style='display: flex; justify-content: space-between;'>
            <span>Safe</span>
            <span>Suspicious</span>
            <span>Dangerous</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Analyze button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        analyze_button = st.button("🔍 Analyze Message", use_container_width=True)
    
    if analyze_button and text_input:
        with st.spinner("🤖 AI is analyzing your message..."):
            try:
                # Call API
                start_time = time.time()
                resp = requests.post(API_URL, json={"text": text_input}, timeout=120)
                response_time = time.time() - start_time
                
                if resp.status_code == 200:
                    data = resp.json()
                    analysis = data["analysis"]
                    
                    # Update stats
                    st.session_state.total_scans += 1
                    if analysis.get('risk_level', 0) > 50:
                        st.session_state.total_risks += 1
                    
                    # Store in history
                    st.session_state.history.append({
                        'text': text_input[:50] + "...",
                        'risk': analysis.get('risk_level', 0),
                        'time': datetime.now().strftime("%H:%M:%S"),
                        'flags': analysis.get('flags', [])
                    })
                    
                    # Display results in a beautiful container
                    st.markdown("<div class='result-container'>", unsafe_allow_html=True)
                    
                    # Risk level with color
                    risk_level = analysis.get('risk_level', 0)
                    if risk_level < 30:
                        risk_color = "#00ff88"
                        risk_text = "SAFE"
                        emoji = "✅"
                    elif risk_level < 70:
                        risk_color = "#ffaa00"
                        risk_text = "SUSPICIOUS"
                        emoji = "⚠️"
                    else:
                        risk_color = "#ff4444"
                        risk_text = "DANGEROUS"
                        emoji = "🚨"
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown(f"<h2 style='color: {risk_color};'>{emoji} {risk_text}</h2>", unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"<h3>Risk Score: {risk_level}/100</h3>", unsafe_allow_html=True)
                    with col3:
                        st.markdown(f"<h3>⚡ {response_time:.2f}s</h3>", unsafe_allow_html=True)
                    
                    # Risk gauge - FIXED COLORS
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=risk_level,
                        domain={'x': [0, 1], 'y': [0, 1]},
                        title={'text': "Risk Level"},
                        gauge={
                            'axis': {'range': [0, 100]},
                            'bar': {'color': risk_color},
                            'steps': [
                                {'range': [0, 30], 'color': "rgba(0, 255, 136, 0.2)"},      # Light green
                                {'range': [30, 70], 'color': "rgba(255, 170, 0, 0.2)"},     # Light orange
                                {'range': [70, 100], 'color': "rgba(255, 68, 68, 0.2)"}     # Light red
                            ],
                            'threshold': {
                                'line': {'color': "white", 'width': 4},
                                'thickness': 0.75,
                                'value': risk_level
                            }
                        }
                    ))
                    fig.update_layout(height=250, paper_bgcolor='rgba(0,0,0,0)')
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Detected flags
                    if analysis.get('flags'):
                        st.markdown("### 🔍 Detected Sensitive Information:")
                        flags_html = ""
                        for flag in analysis['flags']:
                            flags_html += f"<span style='background: {risk_color}33; padding: 5px 10px; border-radius: 20px; margin: 5px; display: inline-block;'>🔴 {flag.upper()}</span>"
                        st.markdown(flags_html, unsafe_allow_html=True)
                    
                    # AI Advice
                    advice = analysis.get('advice', {})
                    if isinstance(advice, dict):
                        if 'classification' in advice:
                            st.markdown(f"### 🤖 AI Analysis")
                            st.markdown(f"**Classification:** {advice.get('classification', 'N/A')}")
                            st.markdown(f"**Confidence:** {advice.get('confidence', 'N/A')}")
                            st.markdown(f"**Reason:** {advice.get('reason', 'N/A')}")
                            
                            if 'safe_rewrite' in advice:
                                st.markdown("### ✨ Safer Version:")
                                st.info(advice['safe_rewrite'])
                            
                            if 'tips' in advice:
                                st.markdown("### 💡 Security Tips:")
                                for tip in advice['tips']:
                                    st.markdown(f"- {tip}")
                        else:
                            st.markdown("### 🤖 AI Advice:")
                            st.write(advice.get('text', advice))
                    else:
                        st.markdown("### 🤖 AI Advice:")
                        st.write(advice)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                else:
                    st.error(f"API Error: {resp.status_code}")
                    
            except Exception as e:
                st.error(f"Connection Error: {str(e)}")
                st.info("Make sure the backend is running: `python3 -m uvicorn backend.main:app --reload --port 8000`")

with tab2:
    st.markdown("### 📈 Analytics Dashboard")
    
    if st.session_state.history:
        # Create dataframe from history
        df = pd.DataFrame(st.session_state.history)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Risk trend
            fig = px.line(df, x='time', y='risk', title="Risk Trend Over Time")
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Flag frequency
            all_flags = []
            for item in st.session_state.history:
                all_flags.extend(item['flags'])
            
            if all_flags:
                flag_counts = pd.Series(all_flags).value_counts()
                fig = px.pie(values=flag_counts.values, names=flag_counts.index, title="Detected Risks")
                st.plotly_chart(fig, use_container_width=True)
        
        # Recent scans
        st.markdown("### 🕒 Recent Scans")
        for item in reversed(st.session_state.history[-5:]):
            color = "#00ff88" if item['risk'] < 30 else "#ffaa00" if item['risk'] < 70 else "#ff4444"
            st.markdown(f"""
            <div style='background: rgba(255,255,255,0.05); padding: 10px; border-radius: 10px; margin: 5px 0; border-left: 5px solid {color};'>
                <b>{item['time']}</b> - {item['text']} <span style='color: {color};'>Risk: {item['risk']}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No scans yet. Try analyzing a message in the Scanner tab!")

with tab3:
    st.markdown("### ⚙️ Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎨 Appearance")
        theme = st.selectbox("Theme", ["Dark (Default)", "Light", "Cyberpunk"])
        
        st.markdown("#### 🔧 Performance")
        model_speed = st.select_slider("Model Speed", options=["Fast", "Balanced", "Accurate"])
        
    with col2:
        st.markdown("#### 🔒 Privacy")
        st.checkbox("Store scan history", value=True)
        st.checkbox("Send anonymous usage stats", value=False)
        
        st.markdown("#### 📝 Default Settings")
        auto_scan = st.checkbox("Auto-scan on paste", value=False)
    
    if st.button("Save Settings"):
        st.success("✅ Settings saved!")
    
    st.markdown("---")
    st.markdown("### 📋 About This Project")
    st.markdown("""
    **AI Guardian** is a privacy-first cybersecurity assistant built for DevDash 2026.
    
    - **100% Local AI** – No data leaves your machine
    - **Real-time Analysis** – Instant risk detection
    - **Smart Rewrites** – AI-powered safe alternatives
    - **Beautiful Dashboard** – Professional, modern UI
    
    Built with ❤️ using Python, FastAPI, Streamlit, and Ollama
    """)

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #666;'>🛡️ AI Guardian v2.0 | Made for DevDash 2026 | Privacy First • Local AI • No Cloud</p>",
    unsafe_allow_html=True
)
