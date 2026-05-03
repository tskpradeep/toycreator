import streamlit as st
import os

# PHASE 1: HARD-FROZEN LOGIC & GUI BASELINE
# Rule 10: Provider Independence | Rule 11: 1:1 Engineering Rigidity
st.set_page_config(layout="wide", page_title="System Gateway", initial_sidebar_state="collapsed")

# PROFESSIONAL GUI FREEZE: Pure Black, Centered, No Spreading
st.markdown("""
    <style>
    /* Full Reset */
    .block-container { padding: 0 !important; background-color: #000000; height: 100vh; width: 100vw; display: flex; justify-content: center; align-items: center; }
    header, footer { visibility: hidden !important; }
    
    /* Centered Professional Hub (Locked at 350px) */
    .stApp { background-color: #000000; }
    [data-testid="stVerticalBlock"] { align-items: center !important; }
    
    /* Constraints for Login Bars */
    .stTextInput, .stButton, .stRadio {
        width: 350px !important;
    }

    /* Professional Engineering Text */
    h1, h2, h3, label, p, .stMarkdown { 
        color: #ffffff !important; 
        text-align: center !important; 
        font-family: 'Courier New', Courier, monospace !important;
    }

    /* Small Precise Input Bars */
    .stTextInput input {
        background-color: #111 !important;
        color: #00ff00 !important;
        border: 1px solid #333 !important;
        text-align: center !important;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    # --- AUTHENTICATION STATE TRACKING ---
    if 'category' not in st.session_state:
        st.session_state['category'] = None
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    # --- GATEWAY LOGIC FLOW ---
    if st.session_state['category'] is None:
        show_category_selection()
    elif not st.session_state['logged_in']:
        show_login_page()
    else:
        show_workbench_ready()

def show_category_selection():
    st.markdown("## TECHNOLOGY DOMAIN")
    cat = st.radio("Select infrastructure type:", 
                  ["Consumer Electronics", "Industrial Automation", "Military Systems"],
                  label_visibility="collapsed")
    
    if st.button("INITIALIZE GATEWAY"):
        st.session_state['category'] = cat
        st.rerun()

def show_login_page():
    st.markdown(f"## ACCESS PORTAL")
    st.markdown(f"#### {st.session_state['category']}")
    
    # Navigation Back
    if st.button("← CHANGE DOMAIN"):
        st.session_state['category'] = None
        st.rerun()
        
    # User Input
    suffix = st.session_state['category'].replace(' ', '_')
    filename = f"auth_{suffix}.txt"
    
    u = st.text_input("Username", key="login_u", placeholder="USER ID")
    p = st.text_input("Password", type="password", key="login_p", placeholder="PASSKEY")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("LOGIN"):
            if check_credentials(u, p, filename):
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("FAILED")
    with col2:
        if st.button("CREATE"):
            save_credentials(u, p, filename)
            st.success("SAVED")

def save_credentials(u, p, filename):
    with open(filename, "a") as f: 
        f.write(f"{u},{p}\n")

def check_credentials(u, p, filename):
    if not os.path.exists(filename): return False
    with open(filename, "r") as f:
        for line in f:
            if f"{u},{p}" == line.strip(): return True
    return False

def show_workbench_ready():
    # Placeholder for Phase 2 Grid
    st.markdown("<h2 style='color: #00ff00;'>SYSTEM ONLINE</h2>", unsafe_allow_html=True)
    st.markdown(f"**DOMAIN:** {st.session_state['category']}")
    if st.button("EXIT SYSTEM"):
        st.session_state.update({"logged_in": False})
        st.rerun()

if __name__ == "__main__":
    main()
