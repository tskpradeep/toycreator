import streamlit as st
import json
import os

st.set_page_config(page_title="AI-SET CONFIG", layout="centered")

# CSS to maintain the look
st.markdown("""
<style>
    .stApp { background-color: #000; color: #00ff00; font-family: monospace; }
    .main-box { border: 2px solid #00ff00; padding: 20px; box-shadow: 0 0 20px #004400; }
    h2 { color: #00ff00; border-bottom: 1px solid #00ff00; }
    label { color: #00ff00 !important; }
    input { background-color: #000 !important; color: #00ff00 !important; border: 1px solid #00ff00 !important; }
</style>
""", unsafe_allow_html=True)

CONFIG_FILE = "comutoy.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"version": "gemini-1.5-flash", "api_key": "", "api_url": "https://generativelanguage.googleapis.com/v1beta/models/"}

config = load_config()

st.title("[ SYSTEM AI-SET ]")

with st.container():
    st.markdown('<div class="main-box">', unsafe_allow_html=True)
    
    tool = st.selectbox("TOOL SELECTION", ["GOOGLE GEMINI", "LUVIA AI", "FLUX.AI"])
    
    version = st.selectbox("AVAILABLE VERSIONS", 
                          ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-1.0-pro"],
                          index=["gemini-1.5-flash", "gemini-1.5-pro", "gemini-1.0-pro"].index(config['version']))
    
    api_key = st.text_input("API KEY / LOCAL PATH", value=config['api_key'], type="password")
    
    api_url = st.text_input("API URL", value=config['api_url'])
    
    if st.button("SAVE TO COMUTOY.JSON"):
        new_config = {
            "tool": tool,
            "version": version,
            "api_key": api_key,
            "api_url": api_url
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(new_config, f, indent=4)
        st.success("CONFIGURATION SAVED SUCCESSFULLY")
        
    st.markdown('</div>', unsafe_allow_html=True)

st.info("The main window (dashtoy.py) will use these settings on the next prompt.")
