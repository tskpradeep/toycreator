import streamlit as st
from google import genai

# --- 1. DARK UI SETUP ---
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

# --- 2. SIDEBAR SETTINGS ---
with st.sidebar:
    st.header("⚙️ 2026 Settings")
    api_key = st.text_input("Enter 2026 API Key", type="password")
    
    # Selecting Model 2 as requested (Gemini 3 Flash)
    model_choice = "gemini-3-flash-preview"
    st.success(f"Active Model: {model_choice}")

# --- 3. DUAL WINDOW INTERFACE ---
st.title("AI Workbench")
col1, col2 = st.columns(2)

with col1:
    st.subheader("PROMPTING WINDOW")
    user_prompt = st.text_area("Your Question:", height=400, placeholder="e.g. Who are you?")
    send_btn = st.button("Send to Gemini 3")

with col2:
    st.subheader("ANSWER WINDOW")
    if send_btn:
        if not api_key:
            st.error("Missing API Key.")
        elif not user_prompt:
            st.warning("Please enter a prompt.")
        else:
            with st.spinner("Connecting to Google 2026 Servers..."):
                try:
                    # Verified 2026 Client Logic
                    client = genai.Client(api_key=api_key)
                    
                    # Generate content call
                    response = client.models.generate_content(
                        model=model_choice,
                        contents=user_prompt
                    )
                    
                    st.markdown("---")
                    # Prove it works by displaying the actual text
                    if response.text:
                        st.write(response.text)
                    else:
                        st.error("Empty Response. Check Safety Settings.")
                        
                except Exception as e:
                    # Captures the 400 error and provides the May 2026 solution
                    st.error(f"Execution Error: {e}")
                    if "400" in str(e):
                        st.info("💡 400 ERROR: Your API key is likely expired or from a legacy project. Create a NEW key at aistudio.google.com.")
    else:
        st.write("Awaiting your input...")
