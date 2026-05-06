import streamlit as st

# 1. Setup the Page Layout
st.set_page_config(page_title="AI Interface", layout="wide")

# 2. Apply Dark Mode Design (No borders, no shadows, high contrast text)
st.markdown("""
    <style>
    /* Main background color */
    .stApp { 
        background-color: #1a1a1a; 
    }
    
    /* Text color for the whole app */
    .stApp, .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp label {
        color: #ffffff !important;
    }

    /* Prompt Input Area */
    .stTextArea textarea { 
        background-color: #2d2d2d !important; 
        color: #ffffff !important;
        border: 1px solid #444444 !important; 
        border-radius: 0px; 
        box-shadow: none !important;
    }

    /* Sidebar Background */
    section[data-testid="stSidebar"] {
        background-color: #121212 !important;
    }

    /* Button Styling */
    .stButton>button {
        background-color: #444444;
        color: white;
        border-radius: 0px;
        border: none;
    }
    
    .stButton>button:hover {
        background-color: #666666;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SETTINGS WINDOW (The Sidebar)
with st.sidebar:
    st.header("⚙️ Gemini Settings")
    
    api_key = st.text_input("Gemini API Key", type="password", placeholder="Paste your key here")
    
    model_version = st.selectbox(
        "Model Version",
        ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-1.0-pro"]
    )
    
    st.divider()
    st.caption("Settings update automatically.")

# 4. MAIN INTERFACE (The Two Windows)
st.title("AI Workbench")

# Creating the split view: Left for prompting, Right for seeing the answer
col1, col2 = st.columns(2)

with col1:
    st.subheader("PROMPTING WINDOW")
    user_prompt = st.text_area("Type your request:", height=400, key="prompt_input")
    send_button = st.button("Get Answer")

with col2:
    st.subheader("ANSWER WINDOW")
    # This creates a plain dark box for the result
    answer_box = st.container()
    
    with answer_box:
        if send_button:
            if not api_key:
                st.error("Error: Missing API Key in Settings!")
            elif not user_prompt:
                st.warning("Please type a prompt first.")
            else:
                st.info(f"Connecting to {model_version}...")
                st.markdown("---")
                st.write("Your AI answer will appear here in white text.")
        else:
            st.write("Waiting for your prompt...")
