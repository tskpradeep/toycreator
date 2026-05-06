import streamlit as st
import google.generativeai as genai

# 1. Page Config
st.set_page_config(page_title="AI Workbench 2026", layout="wide")

# 2. Total Dark Mode Design (All text visible)
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    /* Force all text to be White */
    .stApp, .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp label, .stMarkdown {
        color: #ffffff !important;
    }
    /* Input Box Styling */
    .stTextArea textarea { 
        background-color: #262730 !important; 
        color: #ffffff !important;
        border: 1px solid #444444 !important; 
        border-radius: 4px; 
    }
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #161b22 !important;
        border-right: 1px solid #30363d;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SETTINGS SIDEBAR
with st.sidebar:
    st.header("⚙️ Gemini 3 Settings")
    api_key = st.text_input("Enter 2026 API Key", type="password")
    
    # Updated to the currently active May 2026 models
    model_choice = st.selectbox(
        "Current Active Models",
        ["gemini-3-flash-preview", "gemini-3.1-pro-preview", "gemini-2.5-flash"]
    )
    st.caption("Note: Gemini 1.5 is officially retired.")

# 4. MAIN INTERFACE
st.title("AI Workbench")

col1, col2 = st.columns(2)

with col1:
    st.subheader("PROMPTING WINDOW")
    user_prompt = st.text_area("Type your request here:", height=400)
    send_button = st.button("Generate Response")

with col2:
    st.subheader("ANSWER WINDOW")
    answer_area = st.container()
    
    if send_button:
        if not api_key:
            st.error("Missing API Key! Get a new one at AI Studio.")
        elif not user_prompt:
            st.warning("Please enter a prompt.")
        else:
            with st.spinner("Streaming from Gemini 3..."):
                try:
                    # Initialize with Gemini 3 logic
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel(model_choice)
                    
                    response = model.generate_content(user_prompt)
                    
                    with answer_area:
                        st.markdown("---")
                        st.markdown(response.text)
                except Exception as e:
                    # In 2026, many errors are due to using old keys or old model strings
                    st.error(f"Execution Error: {e}")
                    st.info("Check if your API Key is restricted to specific 2026 models.")
    else:
        with answer_area:
            st.write("Awaiting your input...")
