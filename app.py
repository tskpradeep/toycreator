import streamlit as st
import os

# Rule 10: Provider Independent. Rule 1: Practical Engineering Layout.
st.set_page_config(layout="wide", page_title="ToyCreator Workbench Pro", initial_sidebar_state="collapsed")

# Injecting High-Density Engineering UI
st.markdown("""
    <style>
    /* Technical Vibe: Darker accents and condensed spacing */
    .stApp { background-color: #F5F5F5; font-family: 'Courier New', Courier, monospace; }
    header { visibility: hidden; }
    .main .block-container { padding: 10px; }
    
    /* Global Component Styling */
    div.stTextArea textarea { font-size: 12px; background-color: #FAFAFA; border: 1px solid #999; }
    div.stContainer { border: 1px solid #444 !important; background-color: #FFF; }
    
    /* The Right Edge Wall - Dense Icon Strip */
    .wall-container {
        border-left: 2px solid #333;
        height: 95vh;
        background-color: #E0E0E0;
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
    st.title("System Initialization")
    cat = st.selectbox("CHOOSE SYSTEM DOMAIN:", ["CONSUMER_ELECTRONICS", "INDUSTRIAL_AUTOMATION", "MILITARY_SPEC"])
    if st.button("PROCEED"):
        st.session_state['category'] = cat
        st.rerun()

def show_login_page():
    st.subheader(f"TERMINAL ACCESS: {st.session_state['category']}")
    tab1, tab2 = st.tabs(["LOG_IN", "CREATE_ID"])
    suffix = st.session_state['category'].replace(' ', '_')
    filename = f"auth_{suffix}.txt"
    
    with tab1:
        u = st.text_input("UID")
        p = st.text_input("PWD", type="password")
        if st.button("AUTHENTICATE"):
            if check_credentials(u, p, filename):
                st.session_state['logged_in'] = True
                st.rerun()
    with tab2:
        nu = st.text_input("NEW_UID")
        np = st.text_input("NEW_PWD", type="password")
        if st.button("REGISTER"):
            with open(filename, "a") as f: f.write(f"{nu},{np}\n")
            st.success("ID_CREATED")

def check_credentials(u, p, filename):
    if not os.path.exists(filename): return False
    with open(filename, "r") as f:
        for line in f:
            if f"{u},{p}" == line.strip(): return True
    return False

def show_workbench():
    # Grid Breakdown for Engineering Density
    # Left: Workspace (65%) | Right: AI Stack (30%) | Far Right: Tools (5%)
    col_work, col_ai, col_wall = st.columns([0.65, 0.30, 0.05])

    with col_work:
        # Dynamic CAD/Code Vertical Split
        st.write(f"**VIEWPORT: {st.session_state.category}**")
        h_adj = st.slider("V-SCALE", 50, 800, 450, label_visibility="collapsed")
        st.container(height=h_adj, border=True).write("CAD_RENDER_LAYER_0")
        
        st.write("**CMD_PROMPT_SYSTEM_PRG**")
        st.text_area("PROGRAM_INPUT", height=250, label_visibility="collapsed")

    with col_ai:
        st.write("**AI_ANALYSIS_ENGINE**")
        st.container(height=450, border=True).write("SYSTEM_READY...")
        
        st.write("**USER_QUERY_INPUT**")
        st.text_area("PROMPT", height=80, label_visibility="collapsed")
        st.button("EXECUTE_COMMAND", use_container_width=True)

    with col_wall:
        # High Density "Wall"
        st.markdown('<div class="wall-container">', unsafe_allow_html=True)
        st.button("⚙️", help="SYS_CONFIG")
        st.button("📂", help="FILE_MGR")
        st.button("💾", help="MEM_SAVE")
        st.button("🛰️", help="SYNC_SAT")
        st.button("🛠️", help="DEBUG_TOOL")
        st.button("🔒", help="SECURE_X")
        st.markdown('</div>', unsafe_allow_html=True)

    # Status Bar
    st.divider()
    s1, s2, s3 = st.columns([2, 1, 1])
    with s1: st.caption("SYS_STATUS: ONLINE | LATENCY: 24ms | DB: LOCAL_SQLITE")
    with s3:
        if st.button("SYSTEM_LOGOUT", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

if __name__ == "__main__":
    main()
