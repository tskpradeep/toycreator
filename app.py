import streamlit as st
import os

# Rule 10 & 11: Free, Portable, and Frozen Logic
st.set_page_config(layout="wide", page_title="Workbench", initial_sidebar_state="collapsed")

# 1:1 Blueprint CSS Implementation
st.markdown("""
    <style>
    .main .block-container { padding: 0 !important; height: 100vh; overflow: hidden; background-color: #fdfdfd; }
    header { visibility: hidden; }
    
    /* Grid Definition for 1:1 Layout */
    .blueprint-grid {
        display: grid;
        grid-template-columns: 1fr 300px 150px; /* Workspace | AI Panel | Square Matrix */
        grid-template-rows: 1fr 150px 80px;     /* Top Content | Command Prompt | Footer */
        height: 100vh;
        border: 2px solid black;
    }

    /* Borders based on Image colors */
    .vertical-red-border { border-right: 3px solid red !important; }
    .horizontal-green-border { border-bottom: 3px solid green !important; }
    
    /* Square Matrix Buttons */
    .matrix-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        grid-gap: 2px;
        padding: 5px;
    }
    .sq-btn { width: 40px; height: 40px; background: black; border: 1px solid white; }
    </style>
    """, unsafe_allow_html=True)

def main():
    if 'category' not in st.session_state: st.session_state['category'] = None
    if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
    if 'v_split' not in st.session_state: st.session_state['v_split'] = 0.7  # Red line position
    if 'h_split' not in st.session_state: st.session_state['h_split'] = 0.6  # Green line position

    if st.session_state['category'] is None:
        show_category_selection()
    elif not st.session_state['logged_in']:
        show_login_page()
    else:
        show_workbench()

# --- FROZEN AUTHENTICATION LOGIC ---
def show_category_selection():
    st.title("System Domain")
    cat = st.radio("Domain:", ["Consumer Electronics", "Industrial Automation", "Military Systems"])
    if st.button("Initialize Gateway"):
        st.session_state['category'] = cat
        st.rerun()

def show_login_page():
    suffix = st.session_state['category'].replace(' ', '_')
    filename = f"auth_{suffix}.txt"
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    with tab1:
        u = st.text_input("User ID")
        p = st.text_input("Passkey", type="password")
        if st.button("Authenticate"):
            if check_credentials(u, p, filename):
                st.session_state['logged_in'] = True
                st.rerun()
    with tab2:
        nu = st.text_input("New ID")
        np = st.text_input("New Passkey", type="password")
        if st.button("Create Account"):
            with open(filename, "a") as f: f.write(f"{nu},{np}\n")

def check_credentials(u, p, filename):
    if not os.path.exists(filename): return False
    with open(filename, "r") as f:
        return f"{u},{p}" in [line.strip() for line in f.readlines()]

# --- 1:1 WORKBENCH ---
def show_workbench():
    # Outer Layout using standard Columns to maintain functionality
    c_main, c_ai, c_matrix = st.columns([st.session_state['v_split'], 0.25, 0.05])

    with c_main:
        # Top: CAD/Visuals
        st.container(height=450, border=True).write("VISUAL DISPLAYS / CAD DESIGNS")
        
        # GREEN BORDER (Horizontal Partition)
        st.markdown("<div style='border-bottom: 3px solid green; margin: 5px 0;'></div>", unsafe_allow_html=True)
        
        # Bottom: Command Prompt
        st.text_area("COMMAND PROMPT", "For system programming...", height=150)

    with c_ai:
        # RED BORDER starts here (Vertical)
        st.markdown("<div style='border-left: 3px solid red; height: 100vh; position: absolute; left: 0;'></div>", unsafe_allow_html=True)
        
        # AI Replying
        st.container(height=350, border=True).write("AI TEXT REPLYING WINDOW")
        
        # GREEN BORDER (Horizontal)
        st.markdown("<div style='border-bottom: 3px solid green; margin: 5px 0;'></div>", unsafe_allow_html=True)
        
        # User Prompting
        st.text_area("USER PROMPT", height=200, placeholder="USER PROMPTING")

    with c_matrix:
        # Rare buttons stack (Vertical right wall)
        for i in range(10):
            st.button("⬛", key=f"rare_{i}")

    # FOOTER SECTION
    st.markdown("---")
    f1, f2, f3 = st.columns([0.2, 0.5, 0.3])
    with f1:
        st.info("Small Indicators")
    with f2:
        st.success("Control Buttons Decisions Space")
    with f3:
        # Square Matrix (Right Bottom Corner)
        m_cols = st.columns(3)
        for i in range(9):
            m_cols[i % 3].button("⬛", key=f"mat_{i}")

if __name__ == "__main__":
    main()
