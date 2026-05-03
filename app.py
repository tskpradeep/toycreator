import streamlit as st
import os

# Rule 10: Provider Independence & Rule 1: Practicality
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
    st.title("Technology Domain Selection")
    # Rule 5: Suggesting the most robust verified categories for this architecture
    cat = st.radio("Select the infrastructure type to build:", 
                  ["Consumer Electronics", "Industrial Automation", "Military Systems"])
    if st.button("Initialize Gateway"):
        st.session_state['category'] = cat
        st.rerun()

def show_login_page():
    st.title(f"Access Portal: {st.session_state['category']}")
    if st.button("← Change Domain"):
        st.session_state['category'] = None
        st.rerun()
        
    tab1, tab2 = st.tabs(["Secure Login", "Register Account"])
    
    # Rule 10: Files are named by category for easy server migration
    suffix = st.session_state['category'].replace(' ', '_')
    filename = f"auth_{suffix}.txt"
    
    with tab1:
        u = st.text_input("Username", key="login_u")
        p = st.text_input("Password", type="password", key="login_p")
        if st.button("Login"):
            if check_credentials(u, p, filename):
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Authentication Failed")
    with tab2:
        nu = st.text_input("Create Username", key="reg_u")
        np = st.text_input("Create Password", type="password", key="reg_p")
        if st.button("Create"):
            save_credentials(nu, np, filename)
            st.success("Account Ready")

def save_credentials(u, p, filename):
    with open(filename, "a") as f: 
        f.write(f"{u},{p}\n")

def check_credentials(u, p, filename):
    if not os.path.exists(filename): return False
    with open(filename, "r") as f:
        for line in f:
            if f"{u},{p}" == line.strip(): return True
    return False

def show_workbench():
    # Mirrored T-Pane: Canvas (Left 3/4), Menu (Right 1/4)
    c1, c2 = st.columns([3, 1])
    with c1:
        st.header(f"System Canvas | {st.session_state['category']}")
        st.divider()
    with c2:
        st.header("Control")
        if st.button("Exit System", use_container_width=True):
            st.session_state.update({"logged_in": False})
            st.rerun()

if __name__ == "__main__":
    main()
