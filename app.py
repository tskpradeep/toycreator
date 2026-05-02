import streamlit as st
import os

# Hardcoded Rule: Ensure layout is wide for landscape monitors
st.set_page_config(layout="wide")

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
                st.error("Invalid username or password")

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
    if not os.path.exists("users.txt"):
        return False
    with open("users.txt", "r") as f:
        for line in f:
            u, p = line.strip().split(",")
            if u == username and p == password:
                return True
    return False

def show_workbench():
    st.write("Login Successful. Workbench Architecture Loading...")
    if st.button("Logout"):
        st.session_state['logged_in'] = False
        st.rerun()

if __name__ == "__main__":
    main()
