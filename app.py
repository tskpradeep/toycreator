# app.py
import streamlit as st
import requests

st.set_page_config(page_title="Simple AI Chat", layout="wide")

# ---------- Sidebar Settings ----------
st.sidebar.title("Settings")

api_url = st.sidebar.text_input(
    "API URL",
    value="https://api.openai.com/v1/chat/completions"
)

api_key = st.sidebar.text_input(
    "API Key",
    type="password"
)

model = st.sidebar.text_input(
    "Model",
    value="gpt-4o-mini"
)

# ---------- Main UI ----------
st.title("Simple AI Chat")

prompt = st.text_area("Your Prompt", height=200)

if st.button("Send"):

    if not prompt:
        st.warning("Enter a prompt.")
    elif not api_key:
        st.warning("Enter API Key.")
    else:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        data = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        try:
            response = requests.post(
                api_url,
                headers=headers,
                json=data
            )

            result = response.json()

            reply = result["choices"][0]["message"]["content"]

            st.text_area("AI Reply", value=reply, height=300)

        except Exception as e:
            st.error(str(e))
