import streamlit as st
import google.generativeai as genai

# 1. Page Config
st.set_page_config(page_title="AI Workbench", layout="wide")

# 2. Dark Mode Styling
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

# 3. Sidebar Settings
with st.sidebar:
    st.header("⚙️ Gemini Settings")
    api_key = st.text_input("Gemini API Key", type="password")
    model_choice = st.selectbox(
        "Select Model",
        ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"]
    )
    st.info("The 'Flash' model is best for the free version.")

# 4. Main Interface
st.title("AI Workbench")

col1, col2 = st.columns(2)

with col1:
    st.subheader("PROMPTING WINDOW")
    user_prompt = st.text_area("Type your request:", height=400, placeholder="e.g. Who are you?")
    send_button = st.button("Get Answer")

with col2:
    st.subheader("ANSWER WINDOW")
    answer_container = st.container()
    
    if send_button:
        if not api_key:
            st.error("Please enter your API Key in the sidebar.")
        elif not user_prompt:
            st.warning("Please enter a prompt first.")
        else:
            with st.spinner("Connecting to Google..."):
                try:
                    # CONFIGURING THE AI ENGINE
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel(model_choice)
                    
                    # SENDING THE PROMPT
                    response = model.generate_content(user_prompt)
                    
                    # DISPLAYING THE ANSWER
                    with answer_container:
                        st.markdown("---")
                        st.markdown(response.text)
                except Exception as e:
                    st.error(f"Technical Error: {e}")
                    st.write("Tip: Make sure your API key is correct for the selected model.")
    else:
        with answer_container:
            st.write("Waiting for prompt...")
