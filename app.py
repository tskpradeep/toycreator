import streamlit as st
import requests
import json

# --- 1. UI CONFIGURATION ---
st.set_page_config(page_title="AI Workbench 2026", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white !important; }
    .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp label { color: white !important; }
    .stTextArea textarea { 
        background-color: #1c2128 !important; 
        color: white !important;
        border: 1px solid #30363d !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Dashboard Settings")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    # Using Model 2 (Gemini 3 Flash) as requested
    model_id = "gemini-3-flash-preview"
    st.success(f"Target: {model_id}")

# --- 3. DUAL WINDOW DASHBOARD ---
st.title("AI Workbench")
col1, col2 = st.columns(2)

with col1:
    st.subheader("PROMPTING WINDOW")
    user_prompt = st.text_area("Enter your request:", height=400)
    send_btn = st.button("Get Response")

with col2:
    st.subheader("ANSWER WINDOW")
    if send_btn:
        if not api_key:
            st.error("API Key is missing.")
        elif not user_prompt:
            st.warning("Please enter a prompt.")
        else:
            with st.spinner("Connecting to Google Servers..."):
                try:
                    # DIRECT REST API CALL (Bypasses library bugs)
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_id}:generateContent?key={api_key}"
                    
                    headers = {'Content-Type': 'application/json'}
                    data = {
                        "contents": [{"parts": [{"text": user_prompt}]}]
                    }
                    
                    response = requests.post(url, headers=headers, json=data)
                    result = response.json()
                    
                    # ERROR HANDLING FOR THE 400 ERROR
                    if response.status_code != 200:
                        st.error(f"Error {response.status_code}: {result['error']['message']}")
                        if "API key not valid" in str(result):
                            st.info("💡 SOLUTION: Go to aistudio.google.com, delete your old key, and create a NEW one. Keys from before April 2026 are often rejected.")
                    else:
                        # SUCCESSFUL RESPONSE DISPLAY
                        answer = result['candidates'][0]['content']['parts'][0]['text']
                        st.markdown("---")
                        st.write(answer)
                        
                except Exception as e:
                    st.error(f"Technical Failure: {e}")
    else:
        st.write("Awaiting your input...")
