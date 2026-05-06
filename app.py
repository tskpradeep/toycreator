import streamlit as st
import requests

st.set_page_config(page_title="Gemini AI Chat", layout="wide")

# ---------- Sidebar ----------
st.sidebar.title("Settings")

api_url = st.sidebar.text_input(
    "API URL",
    value="https://generativelanguage.googleapis.com/v1beta/models/"
)

api_key = st.sidebar.text_input("Gemini API Key", type="password")

model = st.sidebar.selectbox(
    "Model",
    [
        "gemini-2.5-flash",
        "gemini-2.5-pro",
        "gemini-2.5-flash-lite"
    ]
)

# ---------- Main ----------
st.title("Gemini AI Chat")

prompt = st.text_area("Your Prompt", height=220)

if st.button("Send"):

    if not api_key:
        st.warning("Enter API key")
        st.stop()

    if not prompt:
        st.warning("Enter prompt")
        st.stop()

    url = f"{api_url}{model}:generateContent?key={api_key}"

    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    try:
        response = requests.post(url, json=data)
        result = response.json()

        if "candidates" in result:
            reply = result["candidates"][0]["content"]["parts"][0]["text"]
            st.text_area("AI Reply", value=reply, height=320)
        else:
            st.error(result)

    except Exception as e:
        st.error(str(e))
