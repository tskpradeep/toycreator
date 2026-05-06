import streamlit as st
from google import genai

# 1. Page Config
st.set_page_config(page_title="2026 AI Workbench", layout="wide")

# 2. Dark Mode CSS
st.markdown("""<style>
    .stApp { background-color: #0e1117; color: white !important; }
    .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp label { color: white !important; }
    .stTextArea textarea { background-color: #1c2128 !important; color: white !important; border: 1px solid #30363d; }
</style>""", unsafe_allow_html=True)

# 3. Sidebar Settings
with st.sidebar:
    st.header("⚙️ 2026 Gemini Settings")
    # Tip: In 2026, most keys start with 'AIza...'
    api_key = st.text_input("New Gemini API Key", type="password")
    
    # These are the current stable models for May 2026
    model_choice = st.selectbox(
        "Current Stable Models",
        ["gemini-3-flash-preview", "gemini-3.1-flash-lite", "gemini-3.1-pro"]
    )
    st.caption("Check aistudio.google.com for your new key.")

# 4. Main Interface
st.title("AI Workbench")
col1, col2 = st.columns(2)

with col1:
    st.subheader("PROMPTING WINDOW")
    user_prompt = st.text_area("Your Question:", height=400, placeholder="e.g. Who are you?")
    send_btn = st.button("Generate Response")

with col2:
    st.subheader("ANSWER WINDOW")
    if send_btn:
        if not api_key:
            st.error("Missing API Key! Please paste a new one in the sidebar.")
        else:
            with st.spinner("Talking to Google 2026 Servers..."):
                try:
                    # NEW 2026 CLIENT LOGIC
                    client = genai.Client(api_key=api_key)
                    
                    response = client.models.generate_content(
                        model=model_choice,
                        contents=user_prompt
                    )
                    
                    st.markdown("---")
                    # If response is empty or blocked, this will catch it
                    if response.text:
                        st.write(response.text)
                    else:
                        st.warning("The model returned an empty response. Check safety settings.")
                        
                except Exception as e:
                    # This captures the 400 error and explains it
                    st.error(f"Execution Error: {e}")
                    if "400" in str(e):
                        st.info("💡 Your key is invalid for this model. Please generate a NEW key at AI Studio.")
    else:
        st.write("Awaiting your input...")
