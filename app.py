import streamlit as st
import os

# Rule 10 & 11: Provider Independent and Frozen Logic
st.set_page_config(layout="wide", page_title="Engineering Workbench Baseline", initial_sidebar_state="collapsed")

# Rule 6: Minimalist plain gray background
st.markdown("""
    <style>
    .block-container { padding: 0 !important; background-color: #d3d3d3; height: 100vh; }
    header, footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

def main():
    # --- FROZEN AUTHENTICATION LOGIC ---
    if 'category' not in st.session_state: 
        st.session_state['category'] = None
    if 'logged_in' not in st.session_state: 
        st.session_state['logged_in'] = False

    if st.session_state['category'] is None:
        show_category_selection()
    elif not st.session_state['logged_in']:
        show_login_page()
    else:
        # This is where we will carefully rebuild the 1:1 blueprint
        show_workbench_gateway()

def show_category_selection():
    st.title("System Domain")
    cat = st.radio("Select Operational Domain:", ["Consumer Electronics", "Industrial Automation", "Military Systems"])
    if st.button("Initialize Gateway"):
        st.session_state['category'] = cat
        st.rerun()

def show_login_page():
    # File naming convention based on selected domain
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
            # Local storage implementation (Provider Independent)
            with open(filename, "a") as f: 
                f.write(f"{u},{p}\n")
            st.success("Credential Logged Locally.")

def check_credentials(u, p, filename):
    if not os.path.exists(filename): 
        return False
    with open(filename, "r") as f:
        credentials = [line.strip() for line in f.readlines()]
        return f"{u},{p}" in credentials

def show_workbench_gateway():
    st.success(f"System Authenticated: {st.session_state['category']}")
    st.info("Awaiting instruction for the rigid 1:1 grid reconstruction.")

if __name__ == "__main__":
    main()
