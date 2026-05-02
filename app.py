import streamlit as st
import os

# Rule 10 & 11: Free, Portable, and Frozen Logic
st.set_page_config(layout="wide", page_title="Workbench", initial_sidebar_state="collapsed")

# CSS for Zero-Scroll and Engineering Density
st.markdown("""
    <style>
    /* Lock Viewport to prevent scrolling */
    .main .block-container { 
        padding: 0 !important; 
        height: 100vh; 
        overflow: hidden; 
        background-color: #fdfdfd;
    }
    header { visibility: hidden; }
    
    /* Zero-Gap Engineering Grid */
    .stHorizontalBlock { gap: 0 !important; }
    div[data-testid="column"] { padding: 0 !important; border: 0.5px solid #444; }
    
    /* Technical Text Areas */
    div.stTextArea textarea { font-family: 'Consolas', monospace; font-size: 11px; border-radius: 0; }
    
    /* Resizer Line Styling */
    .resizer-line {
        background-color: #333;
        height: 4px;
        cursor: ns-resize;
        display: flex;
        justify-content: center;
        align-items: center;
        color: white;
        font-size: 8px;
        line-height: 4px;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    if 'category' not in st.session_state: st.session_state['category'] = None
    if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
    if 'h_split' not in st.session_state: st.session_state['h_split'] = 450

    if st.session_state['category'] is None:
        show_category_selection()
    elif not st.session_state['logged_in']:
        show_login_page()
    else:
        show_workbench()

# --- FROZEN AUTHENTICATION ---
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

# --- WORKBENCH (IMAGE_A64CB9.PNG ALIGNMENT) ---
def show_workbench():
    # 1. Top Icon Ribbon (Engineering Density)
    ribbon = st.columns(15)
    icons = ["📄", "📁", "💾", "📐", "🔍", "⚡", "🧩", "🛠️", "🔗", "🔄", "⚙️", "🔒"]
    for i, icon in enumerate(icons):
        ribbon[i].button(icon, key=f"rib_{i}")

    # 2. Main Workbench Area
    col_main, col_ai, col_wall = st.columns([0.70, 0.25, 0.05])

    with col_main:
        # CAD Section
        st.container(height=st.session_state['h_split'], border=True).write("CAD DRAWING AREA")
        
        # Excel-Style Divider Logic
        st.markdown('<div class="resizer-line">••••••••••••••••</div>', unsafe_allow_html=True)
        # Small buttons to simulate the "Drag" without breaking the 100vh lock
        c_up, c_down, _ = st.columns([0.05, 0.05, 0.9])
        if c_up.button("▴", key="up"): st.session_state['h_split'] = max(100, st.session_state['h_split']-50); st.rerun()
        if c_down.button("▾", key="down"): st.session_state['h_split'] = min(700, st.session_state['h_split']+50); st.rerun()
        
        # Bottom Command Window
        st.text_area("COMMAND_WINDOW", "System Initialized...", height=200, label_visibility="collapsed")

    with col_ai:
        # AI Interaction
        st.container(height=400, border=True).write("AI_ANALYSIS")
        st.text_area("USER_PROMPT", placeholder="Enter instructions...", height=150, label_visibility="collapsed")
        st.button("EXECUTE")

    with col_wall:
        # Right Wall Buttons
        for btn in ["⚙️", "📁", "💾", "🛠️"]:
            st.button(btn, key=f"wall_{btn}")

if __name__ == "__main__":
    main()
