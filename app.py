import streamlit as st
import google.generativeai as genai

# 1. Setup the Page Layout
st.set_page_config(page_title="AI Workbench", layout="wide")

# 2. Dark Mode CSS (Fixed to ensure text is always white)
st.markdown("""
    <style>
    .stApp { background-color: #1a1a1a; }
    .stApp, .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp label { color: #ffffff !important; }
    .stTextArea textarea { 
        background-color: #2d2d2d !important; 
        color: #ffffff !important;
        border: 1px solid #444444 !important; 
        border-radius: 0px; 
    }
    section[data-testid="stSidebar"] { background-color: #121212 !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. SETTINGS SIDEBAR
with st.sidebar:
    st.header("⚙️ Gemini Settings")
    api_key = st.text_input("Gemini API Key", type="password")
    
    # 2026 ACTIVE MODELS
    model_version = st.selectbox(
        "Model Version",
        ["gemini-3-flash-preview", "gemini-3.1-flash-lite-preview", "gemini-2.5-flash"]
    )
    st.caption("Note: 1.5 models were retired earlier this year.")

# 4. MAIN INTERFACE
st.title("AI Workbench")

col1, col2 = st.columns(2)

with col1:
    st.subheader("PROMPTING WINDOW")
    user_prompt = st.text_area("Type your request:", height=400)
    send_button = st.button("Get Answer")

with col2:
    st.subheader("ANSWER WINDOW")
    answer_box = st.container()
    
    with answer_box:
        if send_button:
            if not api_key:
                st.error("Please enter your API Key in the sidebar.")
            elif not user_prompt:
                st.warning("Please enter a prompt.")
            else:
                with st.spinner(f"AI is thinking..."):
                    try:
                        # --- THE MISSING CONNECTION LOGIC ---
                        genai.configure(api_key=api_key)
                        model = genai.GenerativeModel(model_version)
                        
                        # Fetch the response
                        response = model.generate_content(user_prompt)
                        
                        # Show the response
                        st.markdown("---")
                        st.markdown(response.text)
                        
                    except Exception as e:
                        st.error(f"Error: {e}")
                        st.info("Check if your API key is active for 2026 models in AI Studio.")
        else:
            st.write("Waiting for prompt...")
