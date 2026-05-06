import streamlit as st
from google import genai

# --- UI SETUP ---
st.set_page_config(page_title="AI Workbench 2026", layout="wide")

# Dark Mode CSS - Ensures 100% text visibility
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

# --- SIDEBAR SETTINGS ---
with st.sidebar:
    st.header("⚙️ 2026 Settings")
    # THE ONLY OPTION: API KEY
    api_key = st.text_input("Enter 2026 API Key", type="password")
    
    # PERMANENTLY ERASED 1.5 - ONLY 2026 MODELS ALLOWED
    model_choice = "gemini-3-flash"
    st.success(f"Active Model: {model_choice}")

# --- MAIN INTERFACE ---
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
            st.error("Action Required: Paste your API Key in the sidebar.")
        elif not user_prompt:
            st.warning("Action Required: Enter a prompt.")
        else:
            with st.spinner("Processing via Google 2026 Servers..."):
                try:
                    # NEW 2026 SDK CLIENT - Resolves the 400 Header Bug
                    client = genai.Client(api_key=api_key)
                    
                    # FETCHING RESPONSE
                    response = client.models.generate_content(
                        model=model_choice,
                        contents=user_prompt
                    )
                    
                    st.markdown("---")
                    # ACTUAL RESPONSE COLLECTION
                    if response.text:
                        st.write(response.text)
                    else:
                        st.error("Model returned no text. Check API Studio Safety settings.")
                        
                except Exception as e:
                    # CLEAR ERROR REPORTING
                    st.error(f"Technical Failure: {e}")
                    if "400" in str(e):
                        st.info("💡 May 2026 Notice: Google recently purged old keys. If this 400 error persists, delete your key at AI Studio and create a NEW one.")
    else:
        st.write("Awaiting your input...")
