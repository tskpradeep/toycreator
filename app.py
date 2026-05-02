import streamlit as st
import os

# Rule 10 & 11: Frozen Logic and Provider Independence
st.set_page_config(layout="wide", page_title="Workbench v1.0", initial_sidebar_state="collapsed")

# Baseline CSS - Only ensures the background is the required plain gray
st.markdown("""
    <style>
    .block-container { padding: 0 !important; background-color: #d3d3d3; height: 100vh; }
    header, footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

def main():
    # --- FROZEN AUTHENTICATION LOGIC ---
    if 'category' not in st.session_state: st.session_state['category'] = None
    if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False

    if st.session_state['category'] is None:
        show_category_selection()
    elif not st.session_state['logged_in']:
        show_login_page()
    else:
        show_workbench_initialization()

def show_category_selection():
    st.title("System Domain")
    cat = st.radio("Select Domain:", ["Consumer Electronics", "Industrial Automation", "Military Systems"])
    if st.button("Initialize Gateway"):
        st.session_state['category'] = cat
        st.rerun()

def show_login_page():
    suffix = st.session_state['category'].replace(' ', '_')
    filename = f"auth_{suffix}.txt"
    st.subheader(f"Access Portal: {st.session_state['category']}")
    
    u = st.text_input("User ID")
    p = st.text_input("Passkey", type="password")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Authenticate"):
            if check_credentials(u, p, filename):
                st.session_state['logged_in'] = True
                st.rerun()
    with col2:
        if st.button("Register New ID"):
            with open(filename, "a") as f: 
                f.write(f"{u},{p}\n")
            st.success("Credential Logged.")

def check_credentials(u, p, filename):
    if not os.path.exists(filename): return False
    with open(filename, "r") as f:
        credentials = [line.strip() for line in f.readlines()]
        return f"{u},{p}" in credentials

# --- REFRESHED WORKBENCH INITIALIZATION ---
def show_workbench_initialization():
    st.write("System Ready. Waiting for Blueprint Grid Instructions...")

if __name__ == "__main__":
    main()
