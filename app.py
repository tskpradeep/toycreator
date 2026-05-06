import streamlit as st
import google.generativeai as genai

# --- UI CONFIGURATION ---
st.set_page_config(page_title="AI Workbench", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #1a1a1a; color: white !important; }
    .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp label { color: white !important; }
    .stTextArea textarea { background-color: #2d2d2d !important; color: white !important; border: 1px solid #444444 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR SETTINGS ---
with st.sidebar:
    st.header("⚙️ Gemini Settings")
    api_key = st.text_input("Enter API Key", type="password")
    # Using 'gemini-1.5-flash' as it remains the most stable free-tier endpoint in May 2026
    model_version = st.selectbox("Model", ["gemini-1.5-flash", "gemini-2.0-flash"])

# --- MAIN WINDOWS ---
st.title("AI Workbench")
col1, col2 = st.columns(2)

with col1:
    st.subheader("PROMPTING WINDOW")
    user_prompt = st.text_area("Your Question:", height=400)
    send_button = st.button("Get Response")

with col2:
    st.subheader("ANSWER WINDOW")
    if send_button:
        if not api_key:
            st.error("Missing API Key.")
        else:
            with st.spinner("Fetching response..."):
                try:
                    # THE ACTUAL CONNECTION LOGIC
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel(model_version)
                    
                    # This line sends your prompt and gets the text back
                    response = model.generate_content(user_prompt)
                    
                    st.markdown("---")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")
    else:
        st.write("Waiting for prompt...")
