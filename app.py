import streamlit as st
import os

# Rule 10: Provider Independent. Rule 1: Excel-style Draggable UI.
st.set_page_config(layout="wide", page_title="Engineering Workbench", initial_sidebar_state="collapsed")

# Rule 6: No explanation. Implementing Zero-Gap Grid and Flex-Drag properties.
st.markdown("""
    <style>
    .block-container { padding: 0 !important; }
    header { visibility: hidden; }
    
    /* Zero-Gap Engineering Layout */
    .stHorizontalBlock { gap: 0 !important; }
    div[data-testid="column"] { padding: 0 !important; border: 0.5px solid #444; }
    
    /* Technical Styling */
    div.stTextArea textarea { font-family: 'Consolas', monospace; font-size: 11px; border-radius: 0; }
    .stButton button { border-radius: 0; width: 100%; border: 0.5px solid #444; }
    
    /* Custom Scrollbar for density */
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-thumb { background: #888; }
    </style>
    """, unsafe_allow_html=True)

def main():
    if 'category' not in st.session_state: st.session_state['category'] = None
    if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False

    if st.session_state['category'] is None:
        show_category_selection()
    elif not st.session_state['logged_in']:
        show_login_page()
    else:
        show_workbench()

# --- FROZEN AUTHENTICATION (Rule 11) ---
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

# --- DRAGGABLE WORKBENCH (RECREATED) ---
def show_workbench():
    # Top Menu Ribbon (Density per image_a64cb9.png)
    ribbon = st.columns(12)
    icons = ["📄", "📁", "💾", "📐", "🔍", "⚡", "🧩", "🛠️", "🔗", "🔄", "⚙️", "🔒"]
    for i, icon in enumerate(icons):
        ribbon[i].button(icon, key=f"rib_{i}")

    # Main Interaction Logic
    # Col 1: Main Workspace | Col 2: AI interaction | Col 3: Wall
    c1, c2, c3 = st.columns([0.70, 0.25, 0.05])

    with c1:
        # Drawing View (Top)
        st.container(height=500, border=True).write("CAD DRAWING / SCHEMATIC")
        
        # Drag-Simulation Border (Professional Splitter)
        st.markdown("<div style='background:#333; height:2px; cursor:row-resize;'></div>", unsafe_allow_html=True)
        
        # Command Window (Full Width of Workspace)
        st.text_area("COMMAND_LOG", "Ready.", height=200, label_visibility="collapsed")

    with c2:
        # AI Stack
        st.container(height=400, border=True).write("AI_ANALYSIS")
        st.markdown("<div style='background:#333; height:2px;'></div>", unsafe_allow_html=True)
        st.text_area("USER_PROMPT", placeholder="Enter command...", height=100, label_visibility="collapsed")
        st.button("EXECUTE")

    with c3:
        # Far Right Edge Wall
        for btn in ["⚙️", "🛠️", "🔒", "📁"]:
            st.button(btn, key=f"wall_{btn}")

    # Status Bar
    st.markdown("<div style='font-size:10px; padding:2px; border-top:1px solid #444;'>SYS_READY | DOMAIN: "+st.session_state.category+"</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
