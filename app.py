import streamlit as st
import os

# Hard-coded Rule: Wide layout and precise Light-Gray background
st.set_page_config(layout="wide", page_title="ToyCreator Workbench")

# UI Fix: Injecting clean CSS for the background and removing default borders
st.markdown("""
    <style>
    .stApp {
        background-color: #D3D3D3;
    }
    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0);
    }
    </style>
    """, unsafe_allow_html=True)

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
    # One practical choice: Radio buttons for clean selection
    cat = st.radio("Choose the domain for this project:", 
                  ["Consumer Electronics", "Industrial Automation", "Military Grade Systems"])
    if st.button("Proceed to Login"):
        st.session_state['category'] = cat
        st.rerun()

def show_login_page():
    st.title(f"Login: {st.session_state['category']}")
    if st.button("← Back to Categories"):
        st.session_state['category'] = None
        st.rerun()
        
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    # Category-specific credential files ensure migration flexibility (Point 3)
    filename = f"users_{st.session_state['category'].replace(' ', '_')}.txt"
    
    with tab1:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Login"):
            if check_credentials(u, p, filename):
                st.session_state['logged_in'] = True
                st.rerun()
    with tab2:
        nu = st.text_input("New Username")
        np = st.text_input("New Password", type="password")
        if st.button("Create Account"):
            save_credentials(nu, np, filename)
            st.success("Account created!")

def save_credentials(u, p, filename):
    with open(filename, "a") as f: f.write(f"{u},{p}\n")

def check_credentials(u, p, filename):
    if not os.path.exists(filename): return False
    with open(filename, "r") as f:
        for line in f:
            if f"{u},{p}" == line.strip(): return True
    return False

def show_workbench():
    # Mirrored T-Pane (Canvas Left 3/4, Menu Right 1/4)
    c1, c2 = st.columns([3, 1])
    with c1:
        st.subheader(f"System Canvas: {st.session_state['category']}")
        st.write("---")
    with c2:
        st.subheader("Control Menu")
        st.button("Logout", on_click=lambda: st.session_state.update({"logged_in": False}))

if __name__ == "__main__":
    main()
