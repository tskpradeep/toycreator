import streamlit as st

# 1. Setup the Page Layout
st.set_page_config(page_title="AI Interface", layout="wide")

# 2. Apply the Design (Plain light-gray background, no shadows)
st.markdown("""
    <style>
    /* Background color for the whole app */
    .stApp { 
        background-color: #e0e0e0; 
    }
    /* Simple text boxes with no borders/shadows */
    .stTextArea textarea { 
        background-color: #ffffff; 
        border: 1px solid #cccccc; 
        border-radius: 0px; 
        box-shadow: none !important;
    }
    /* Styling for the output box */
    .stVerticalBlock {
        gap: 0rem;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SETTINGS WINDOW (The Sidebar)
with st.sidebar:
    st.header("⚙️ Gemini Settings")
    st.write("Configure your AI here:")
    
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
    user_prompt = st.text_area("Type your request:", height=400)
    send_button = st.button("Get Answer")

with col2:
    st.subheader("ANSWER WINDOW")
    # This creates a plain box for the result
    answer_box = st.container()
    
    with answer_box:
        if send_button:
            if not api_key:
                st.error("Error: Missing API Key in Settings!")
            elif not user_prompt:
                st.warning("Please type a prompt first.")
            else:
                # This is a placeholder showing the system is working
                st.info(f"Connecting to {model_version}...")
                st.markdown("---")
                st.write("Your AI answer will appear here.")
                st.write("(To finish this, you would connect the Google Gemini library next).")
        else:
            st.write("Waitng for your prompt...")
