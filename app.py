import streamlit as st
import requests

# Set the functional design you specified: light-gray, no shadows
st.set_page_config(page_title="ToyCreator Gateway", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #d3d3d3; color: black; }
    div.stButton > button { border: 1px solid black; border-radius: 0px; }
    </style>
    """, unsafe_allow_html=True)

st.title("ToyCreator Phase 1")

# Use a clean input field for your key
api_key = st.text_input("Enter Key:", type="password")

if st.button("Initialize Workbench"):
    if not api_key:
        st.warning("Key Required")
    else:
        # This direct URL method is the only one currently bypassing the 400 error
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash:generateContent?key={api_key}"
        
        headers = {'Content-Type': 'application/json'}
        payload = {"contents": [{"parts": [{"text": "System Check"}]}]}

        try:
            response = requests.post(url, headers=headers, json=payload)
            result = response.json()

            if response.status_code == 200:
                st.success("AUTHENTICATED")
                st.session_state['api_ready'] = True
                # Proceed to your hard-freezed Phase 1 GUI logic here
            else:
                # Show the exact reason from Google without AI interpretation
                error_info = result.get('error', {}).get('message', 'Validation Failed')
                st.error(f"Error: {error_info}")
                st.info("Check if 'Generative Language API' is enabled in your Google Cloud console.")
        except Exception as e:
            st.error(f"Technical Block: {e}")
