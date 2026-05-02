import streamlit as st
import os

# Rule 10 & 4: Free, Provider-Independent. 
st.set_page_config(layout="wide", page_title="Engineering Workbench", initial_sidebar_state="collapsed")

# CSS to lock window height to 100% of the screen (No length scroll)
st.markdown("""
    <style>
    /* Force app to fill 100% height and hide main scrollbar */
    .main .block-container { 
        padding: 0 !important; 
        max-height: 100vh; 
        overflow: hidden; 
    }
    header { visibility: hidden; }
    
    /* Zero-Gap Engineering Layout */
    .stHorizontalBlock { gap: 0 !important; }
    
    /* Resizable-ready containers */
    .resizable-v { 
        display: flex; 
        flex-direction: column; 
        height: 90vh; 
    }
    
    /* Professional Border Styles */
    div[data-testid="column"] { border: 0.5px solid #444; }
    div.stTextArea textarea { font-family: 'Consolas', monospace; font-size: 11px; border-radius: 0; }
    </style>
    """, unsafe_allow_html=True)

def main():
    if 'category' not in st.session_state: st.session_state['category'] = None
    if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
    # Height state for the "Drag" simulation
    if 'h_workspace' not in st.session_state: st.session_state['h_workspace'] = 500

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

# --- DRAGGABLE WORKBENCH ---
def show_workbench():
    # Top Menu Ribbon
    ribbon = st.columns(12)
    icons = ["📄", "📁", "💾", "📐", "🔍", "⚡", "🧩", "🛠️", "🔗", "🔄", "⚙️", "🔒"]
    for i, icon in enumerate(icons):
        ribbon[i].button(icon, key=f"rib_{i}")

    # Column 1: Workspace | Column 2: AI | Column 3: Wall
    c1, c2, c3 = st.columns([0.70, 0.25, 0.05])

    with c1:
        # CAD Window
        st.container(height=st.session_state['h_workspace'], border=True).write("CAD DRAWING / SCHEMATIC")
        
        # The Draggable Wall (Functional Trigger)
        # Rule 1: Manufacturable trigger for resizing height
        if st.button("↕ DRAG BOUNDARY", help="Click to toggle between Code and CAD focus"):
            st.session_state['h_workspace'] = 200 if st.session_state['h_workspace'] == 500 else 500
            st.rerun()
        
        # Command Window
        st.text_area("COMMAND_LOG", "Ready.", height=250, label_visibility="collapsed")

    with c2:
        # AI Stack
        st.container(height=400, border=True).write("AI_ANALYSIS")
        st.text_area("USER_PROMPT", placeholder="Enter command...", height=150, label_visibility="collapsed")
        st.button("EXECUTE COMMAND")

    with c3:
        for btn in ["⚙️", "🛠️", "🔒", "📁"]:
            st.button(btn, key=f"wall_{btn}")

    # Status Bar fixed to bottom
    st.markdown(f"<div style='position:fixed; bottom:0; width:100%; background:#eee; font-size:10px; padding:5px; border-top:1px solid #444;'>SYS_READY | DOMAIN: {st.session_state.category}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
