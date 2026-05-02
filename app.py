import streamlit as st
import os

# Rule 10: Provider Independent. Rule 1: High-Density CAD Style.
st.set_page_config(layout="wide", page_title="Workbench Pro", initial_sidebar_state="collapsed")

# Custom CSS for "Professional Engineering" Appearance
st.markdown("""
    <style>
    /* Remove huge gaps and padding */
    .block-container { padding: 0rem 1rem 1rem !important; }
    .stApp { background-color: #fdfdfd; }
    
    /* Top Menu Bar Density */
    .top-menu { display: flex; gap: 5px; background: #333; padding: 2px 10px; color: white; font-size: 12px; }
    
    /* Compact Borders & Fonts */
    div.stTextArea textarea { font-family: 'Consolas', monospace; font-size: 12px; border: 1px solid #999; }
    div.stContainer { border: 1px solid #ccc !important; border-radius: 0px !important; }
    
    /* Hide Streamlit default elements for more space */
    header { visibility: hidden; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
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

# --- AUTH LOGIC (FROZEN PER RULE 11) ---
def show_category_selection():
    st.title("System Domain")
    cat = st.selectbox("Select Project Category", ["Consumer Electronics", "Industrial Automation", "Military Systems"])
    if st.button("Initialize"):
        st.session_state['category'] = cat
        st.rerun()

def show_login_page():
    st.caption(f"Domain: {st.session_state['category']}")
    tab1, tab2 = st.tabs(["Login", "Register"])
    suffix = st.session_state['category'].replace(' ', '_')
    filename = f"auth_{suffix}.txt"
    with tab1:
        u = st.text_input("User ID")
        p = st.text_input("Passkey", type="password")
        if st.button("Authenticate"):
            if check_credentials(u, p, filename):
                st.session_state['logged_in'] = True
                st.rerun()
    with tab2:
        nu = st.text_input("New User ID")
        np = st.text_input("New Passkey", type="password")
        if st.button("Create Account"):
            with open(filename, "a") as f: f.write(f"{nu},{np}\n")
            st.success("Account Ready")

def check_credentials(u, p, filename):
    if not os.path.exists(filename): return False
    with open(filename, "r") as f:
        users = [line.strip() for line in f.readlines()]
        return f"{u},{p}" in users

# --- WORKBENCH (REBUILT FOR IMAGE 2 ACCURACY) ---
def show_workbench():
    # 1. TOP TOOL RIBBON (Dense Icon Bar)
    cols = st.columns(20) # 20 small columns for icons
    icons = ["📄", "📂", "💾", "🖨️", "🔍", "📐", "⚡", "🧩", "🛠️", "🔗"]
    for i, icon in enumerate(icons):
        cols[i].button(icon, key=f"btn_{i}")

    # 2. MAIN BODY (Split into CAD and AI Stack)
    # Using columns for the Vertical Split logic
    main_left, main_right = st.columns([0.7, 0.3])

    with main_left:
        # CAD Display (Image 2 Top)
        st.caption("DESIGNS / SCHEMATICS")
        h_split = st.number_input("Window Scale", 100, 800, 450, step=50, label_visibility="collapsed")
        st.container(height=h_adj if 'h_adj' in locals() else h_split, border=True).write("CAD Drawing Engine")

    with main_right:
        # AI Interaction Stack (Image 2 Right)
        st.caption("AI ANALYSIS FEED")
        st.container(height=300, border=True).write("Waiting for system input...")
        st.caption("USER PROMPTING")
        st.text_input("Enter Command", key="prompt_compact", label_visibility="collapsed")
        st.button("EXECUTE", use_container_width=True)

    # 3. FULL WIDTH COMMAND WINDOW (Image 2 Bottom)
    st.markdown("---")
    st.caption("COMMAND WINDOW / SESSION LOG")
    st.text_area("Log", "Ready.\nSession started...", height=150, label_visibility="collapsed")

    # 4. STATUS BAR
    s1, s2 = st.columns([4, 1])
    with s1: st.caption(f"CONNECTED | DOMAIN: {st.session_state.category} | ENCODING: UTF-8")
    with s2: 
        if st.button("EXIT", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

if __name__ == "__main__":
    main()
