import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="2026 AI Workbench", layout="wide")

# --- Dark Mode CSS ---
st.markdown("""<style>
    .stApp { background-color: #0e1117; color: white !important; }
    .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp label { color: white !important; }
    .stTextArea textarea { background-color: #262730 !important; color: white !important; border: 1px solid #444444; }
</style>""", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ 2026 Settings")
    api_key = st.text_input("New Gemini 3 Key", type="password")
    # Using the exact 2026 model string
    model_choice = "gemini-3-flash-preview" 

# --- Main Logic ---
st.title("AI Workbench")
col1, col2 = st.columns(2)

with col1:
    st.subheader("PROMPTING")
    user_prompt = st.text_area("Your Question:", height=300)
    send_btn = st.button("Send Request")

with col2:
    st.subheader("RESPONSE")
    if send_btn:
        if not api_key:
            st.error("Error: Please paste a NEW API Key in the sidebar.")
        else:
            try:
                genai.configure(api_key=api_key)
                # SETTING SAFETY TO 'BLOCK_NONE' TO PREVENT NONSENSE FLAGS
                model = genai.GenerativeModel(
                    model_name=model_choice,
                    safety_settings={
                        "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
                        "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
                        "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
                        "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
                    }
                )
                response = model.generate_content(user_prompt)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Execution Error: {e}")
                st.info("If it says 'Invalid Key', please generate a new one at AI Studio.")
