import streamlit as st
import os

# Rule 10 & 11: Free, Portable, and Frozen Logic
st.set_page_config(layout="wide", page_title="ToyCreator Workbench")

def main():
    if 'category' not in st.session_state:
        st.session_state['category'] = None
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if st.session_state['category'] is None:
        show_category_selection()
    elif not st.session_state['logged_in']:
        show_login_page()
    else:
        show_workbench()

def show_category_selection():
    st.title("Select Technology Category")
    cat = st.radio("Choose the domain:", ["Consumer Electronics", "Industrial Automation", "Military Systems"])
    if st.button("Initialize Gateway"):
        st.session_state['category'] = cat
        st.rerun()

def show_login_page():
    st.title(f"Login: {st.session_state['category']}")
    if st.button("← Back"):
        st.session_state['category'] = None
        st.rerun()
        
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    suffix = st.session_state['category'].replace(' ', '_')
    filename = f"auth_{suffix}.txt"
    
    with tab1:
        u = st.text_input("Username", key="l_user")
        p = st.text_input("Password", type="password", key="l_pass")
        if st.button("Access Workbench"):
            if check_credentials(u, p, filename):
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Invalid Credentials")
    with tab2:
        nu = st.text_input("New Username", key="r_user")
        np = st.text_input("New Password", type="password", key="r_pass")
        if st.button("Create Account"):
            with open(filename, "a") as f:
                f.write(f"{nu},{np}\n")
            st.success(f"Account Created for {st.session_state['category']}")

def check_credentials(u, p, filename):
    if not os.path.exists(filename): return False
    with open(filename, "r") as f:
        # Rule 8: Stripping whitespace to ensure precise matching
        users = [line.strip() for line in f.readlines()]
        return f"{u},{p}" in users

def show_workbench():
    # Final Blueprint Layout from image_b135de.png
    col_work, col_ai, col_wall = st.columns([0.65, 0.30, 0.05])

    with col_work:
        st.subheader("Visual Display (CAD/Design)")
        # Dynamic Height Adjustment for Workspace
        h_adj = st.slider("Adjust Viewport Height", 100, 800, 400, label_visibility="collapsed")
        st.container(height=h_adj, border=True).write("CAD Render Area")
        
        st.subheader("Command Prompt")
        st.text_area("System Programming", height=200, placeholder="Coding for project...")

    with col_ai:
        st.subheader("AI Replying Window")
        st.container(height=400, border=True).write("AI Response Feed")
        
        st.subheader("User Prompting")
        st.text_area("Input Command", height=100, key="prompt")
        st.button("Execute", use_container_width=True)

    with col_wall:
        # Hover labels enabled via the 'help' parameter (Rule 7 verified)
        st.button("⚙️", help="Settings")
        st.button("📁", help="Files")
        st.button("💾", help="Save")
        st.button("🛠️", help="Tools")

    # Fixed Bottom Status Bar
    st.divider()
    c1, c2 = st.columns([3, 1])
    with c1:
        st.caption(f"Domain: {st.session_state.category} | System Online")
    with c2:
        if st.button("LOGOUT", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

if __name__ == "__main__":
    main()
