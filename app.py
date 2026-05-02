import streamlit as st
import os

# Hard-coded Rule: Wide layout and plain gray background
st.set_page_config(layout="wide")
st.markdown("""
    <style>
    .stApp {
        background-color: #D3D3D3;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:
        show_login_page()
    else:
        show_workbench()

def show_login_page():
    st.title("ToyCreator Workbench Login")
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    with tab1:
        login_user = st.text_input("Username", key="l_user")
        login_pass = st.text_input("Password", type="password", key="l_pass")
        if st.button("Login"):
            if check_credentials(login_user, login_pass):
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Invalid username/password")
    with tab2:
        new_user = st.text_input("Choose Username", key="s_user")
        new_pass = st.text_input("Choose Password", type="password", key="s_pass")
        if st.button("Create Account"):
            save_credentials(new_user, new_pass)
            st.success("Account created! Please login.")

def save_credentials(username, password):
    with open("users.txt", "a") as f:
        f.write(f"{username},{password}\n")

def check_credentials(username, password):
    if not os.path.exists("users.txt"): return False
    with open("users.txt", "r") as f:
        for line in f:
            u, p = line.strip().split(",")
            if u == username and p == password: return True
    return False

def show_workbench():
    # MIRRORED T-PANE ARCHITECTURE
    # Top Section: Canvas (Left 3/4) and Menu (Right 1/4)
    col_left, col_right = st.columns([3, 1])

    with col_left:
        st.subheader("System Canvas")
        st.info("Architecture Visuals and Form-Factor Validation Area")
        # Placeholder for AI output visuals

    with col_right:
        st.subheader("Control Menu")
        st.radio("Device Grade", ["Toy", "Industry", "Military"])
        st.selectbox("Connectivity", ["USB", "PoE", "Coaxial"])

    # Bottom Section: Terminal and Action Bar
    st.divider()
    terminal_col = st.container()
    with terminal_col:
        st.text_area("Command Terminal / Live Logs", value="System Ready...", height=100)
    
    action_col1, action_col2 = st.columns([8, 2])
    with action_col2:
        if st.button("Logout", use_container_width=True):
            st.session_state['logged_in'] = False
            st.rerun()

if __name__ == "__main__":
    main()
