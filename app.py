import streamlit as st
import os

# Rule 10 & 11: Provider Independent and Frozen Logic
st.set_page_config(layout="wide", page_title="Engineering Workbench", initial_sidebar_state="collapsed")

# Rule 6: Minimalist Pure Black Background with Centered Narrow UI
st.markdown("""
    <style>
    /* Full reset of the Streamlit canvas to black */
    .block-container { 
        padding: 0 !important; 
        background-color: #000000; 
        height: 100vh; 
        display: flex;
        justify-content: center;
        align-items: center;
    }
    header, footer { visibility: hidden; }
    
    /* Center the main content block and restrict width */
    .centered-container {
        width: 400px;
        text-align: center;
        color: white;
        font-family: "Courier New", Courier, monospace;
    }

    /* Restrict width of input bars and center them */
    .stTextInput > div > div > input {
        background-color: #1a1a1a !important;
        color: white !important;
        border: 1px solid #444 !important;
        text-align: center;
    }
    
    /* Ensure all text/labels are visible against black background */
    .stMarkdown, .stRadio, .stTextInput, .stButton, label { 
        color: white !important; 
        text-align: center !important;
    }
    
    /* Center radio buttons and their labels */
    [data-testid="stVerticalBlock"] > div {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    # Wrap everything in a centered div
    st.markdown('<div class="centered-container">', unsafe_allow_html=True)
    
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
        show_workbench_ready()
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_category_selection():
    st.title("System Domain")
    cat = st.radio("Select Operational Domain:", ["Consumer Electronics", "Industrial Automation", "Military Systems"])
    if st.button("Initialize Gateway"):
        st.session_state['category'] = cat
        st.rerun()

def show_login_page():
    suffix = st.session_state['category'].replace(' ', '_')
    filename = f"auth_{suffix}.txt"
    
    st.subheader(f"Access Portal")
    st.caption(f"Domain: {st.session_state['category']}")
    
    # Small input bars centered
    u = st.text_input("User ID", placeholder="Enter ID")
    p = st.text_input("Passkey", type="password", placeholder="Enter Passkey")
    
    if st.button("Authenticate"):
        if check_credentials(u, p, filename):
            st.session_state['logged_in'] = True
            st.rerun()
            
    if st.button("Register New ID"):
        with open(filename, "a") as f: 
            f.write(f"{u},{p}\n")
        st.success("Log Created.")

def check_credentials(u, p, filename):
    if not os.path.exists(filename): 
        return False
    with open(filename, "r") as f:
        credentials = [line.strip() for line in f.readlines()]
        return f"{u},{p}" in credentials

def show_workbench_ready():
    st.success(f"Authenticated: {st.session_state['category']}")
    st.info("System Ready for Grid Implementation.")

if __name__ == "__main__":
    main()
