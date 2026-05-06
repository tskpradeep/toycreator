import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="AI Interface", layout="wide")

# --- CUSTOM CSS FOR MINIMALIST LOOK ---
st.markdown("""
    <style>
    .stApp { background-color: #e0e0e0; }
    .stTextArea textarea { background-color: #ffffff; border: none; }
    .stChatMessage { background-color: #f5f5f5; border-radius: 0px; }
    </style>
    """, unsafe_allow_index=True)

# --- SIDEBAR (SETTINGS) ---
with st.sidebar:
    st.header("⚙️ Gemini Settings")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    model_version = st.selectbox(
        "Model Version",
        ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-1.0-pro"]
    )
    st.info("Settings are saved for this session.")

# --- MAIN INTERFACE (2 WINDOWS) ---
st.title("AI Workbench")

# Create two columns to act as your "windows"
col1, col2 = st.columns(2)

with col1:
    st.subheader("PROMPTING WINDOW")
    user_prompt = st.text_area("Enter your prompt here:", height=300, placeholder="Type something...")
    send_button = st.button("Send to AI")

with col2:
    st.subheader("ANSWER WINDOW")
    # Container for the AI response to make it look like a distinct window
    response_container = st.container(border=True)
    
    if send_button:
        if not api_key:
            st.error("Please enter an API Key in the settings sidebar.")
        elif not user_prompt:
            st.warning("Please enter a prompt first.")
        else:
            with response_container:
                st.write(f"**System:** Sending request to {model_version}...")
                # This is where your AI logic will display the final answer
                st.markdown("---")
                st.write("AI response will appear here once connected to the API.")
    else:
        with response_container:
            st.write("Waiting for prompt...")
