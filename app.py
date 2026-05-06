import streamlit as st

# 1. Setup the Page Layout
st.set_page_config(page_title="AI Workbench", layout="wide")

# 2. Dark Mode CSS
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
    
    # UPDATED MODELS FOR MAY 2026
    model_version = st.selectbox(
        "Model Version",
        ["gemini-2.0-flash", "gemini-3-flash-preview", "gemini-3-pro-preview"]
    )
    st.caption("Note: 1.5 models are deprecated.")

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
                # This spinner tells you the app is ALIVE while waiting
                with st.spinner(f"AI is thinking (using {model_version})..."):
                    try:
                        # Logic placeholder - This is where the actual API call goes
                        st.markdown("---")
                        st.success("Connection Successful!")
                        st.write("If this stays 'thinking' for 2 minutes, check your API Key quota.")
                    except Exception as e:
                        st.error(f"Error: {e}")
        else:
            st.write("Waiting for prompt...")
