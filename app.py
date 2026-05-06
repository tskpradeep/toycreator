import streamlit as st
from google import genai  # Requires 'google-genai' in requirements.txt

# --- UI SETUP ---
st.set_page_config(page_title="AI Workbench 2026", layout="wide")

# Dark Theme for 2026 Visibility
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

# --- SIDEBAR: ONLY API OPTION ---
with st.sidebar:
    st.header("⚙️ 2026 Settings")
    api_key = st.text_input("Enter 2026 API Key", type="password")
    
    # Model 2 Locked (Gemini 3 Flash)
    model_choice = "gemini-3-flash-preview"
    st.success(f"Active Model: {model_choice}")

# --- INTERFACE ---
st.title("AI Workbench")
col1, col2 = st.columns(2)

with col1:
    st.subheader("PROMPTING WINDOW")
    user_prompt = st.text_area("Your Question:", height=400, placeholder="Type here...")
    send_btn = st.button("Send to Gemini 3")

with col2:
    st.subheader("ANSWER WINDOW")
    if send_btn:
        if not api_key:
            st.error("API Key Required.")
        elif not user_prompt:
            st.warning("Enter a prompt.")
        else:
            with st.spinner("Connecting..."):
                try:
                    # NEW 2026 CLIENT ARCHITECTURE
                    client = genai.Client(api_key=api_key)
                    
                    response = client.models.generate_content(
                        model=model_choice,
                        contents=user_prompt
                    )
                    
                    st.markdown("---")
                    if response.text:
                        st.write(response.text)
                    else:
                        st.error("No text returned. Check API permissions.")
                        
                except Exception as e:
                    st.error(f"Error: {e}")
    else:
        st.write("Awaiting your input...")
