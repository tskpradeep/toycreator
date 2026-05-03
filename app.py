import streamlit as st
import streamlit.components.v1 as components
import os

# Phase 1: Hard-Frozen Baseline
st.set_page_config(layout="wide", page_title="System Gateway", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .block-container { padding: 0 !important; background-color: #000000; height: 100vh; width: 100vw; }
    header, footer { visibility: hidden !important; }
    
    /* Login Centering Styles */
    .auth-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        flex-direction: column;
    }
    .stTextInput, .stButton, .stRadio { width: 350px !important; }
    h1, h2, h3, label, p, .stMarkdown { 
        color: #ffffff !important; 
        text-align: center !important; 
        font-family: 'Courier New', Courier, monospace !important;
    }
    .stTextInput input {
        background-color: #111 !important;
        color: #00ff00 !important;
        border: 1px solid #333 !important;
        text-align: center !important;
    }
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
        show_phase2_dashboard()

def show_category_selection():
    st.markdown('<div class="auth-wrapper">', unsafe_allow_html=True)
    st.markdown("## TECHNOLOGY DOMAIN")
    cat = st.radio("Select infrastructure type:", ["Consumer Electronics", "Industrial Automation", "Military Systems"], label_visibility="collapsed")
    if st.button("INITIALIZE GATEWAY"):
        st.session_state['category'] = cat
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def show_login_page():
    st.markdown('<div class="auth-wrapper">', unsafe_allow_html=True)
    st.markdown(f"## ACCESS PORTAL")
    if st.button("← CHANGE DOMAIN"):
        st.session_state['category'] = None
        st.rerun()
    suffix = st.session_state['category'].replace(' ', '_')
    filename = f"auth_{suffix}.txt"
    u = st.text_input("Username", key="login_u", placeholder="USER ID")
    p = st.text_input("Password", type="password", key="login_p", placeholder="PASSKEY")
    if st.button("LOGIN"):
        if check_credentials(u, p, filename):
            st.session_state['logged_in'] = True
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def check_credentials(u, p, filename):
    if not os.path.exists(filename): return False
    with open(filename, "r") as f:
        return any(f"{u},{p}" == line.strip() for line in f)

# Phase 2: Dashboard Implementation
def show_phase2_dashboard():
    # Technical Workbench with Slidable Red/Green Dividers
    html_layout = """
    <style>
        body { background-color: black; margin: 0; overflow: hidden; font-family: 'Courier New', monospace; }
        .wrapper { display: grid; grid-template-columns: 1fr 5px 250px 60px; grid-template-rows: 1fr 5px 150px 80px; height: 100vh; width: 100vw; border: 2px solid white; box-sizing: border-box; }
        
        /* Panes */
        .pane { border: 1px solid #333; position: relative; overflow: hidden; display: flex; align-items: center; justify-content: center; padding: 10px; }
        
        /* Slidable Lines */
        .v-slider { grid-column: 2; grid-row: 1 / 4; background-color: red; cursor: col-resize; z-index: 10; }
        .h-slider { grid-column: 1 / 4; grid-row: 2; background-color: green; cursor: row-resize; z-index: 10; }
        
        /* Specific Sections */
        .matrix-right { grid-column: 4; grid-row: 1 / 4; display: grid; grid-template-columns: 1fr; border-left: 2px solid white; }
        .matrix-bottom { grid-column: 3 / 5; grid-row: 4; display: grid; grid-template-columns: repeat(5, 1fr); border-top: 2px solid white; }
        .cell { border: 1px solid white; background: black; }
        
        .indicator-pane { grid-column: 1; grid-row: 4; border-top: 2px solid white; width: 150px; border-right: 2px solid white; }
        .control-pane { grid-column: 1; grid-row: 4; border-top: 2px solid white; margin-left: 150px; }
    </style>

    <div class="wrapper" id="mainGrid">
        <div class="pane" style="grid-column: 1; grid-row: 1;"></div>
        <div class="v-slider" id="vRed"></div>
        <div class="pane" style="grid-column: 3; grid-row: 1;"></div>
        
        <div class="h-slider" id="hGreen"></div>
        
        <div class="pane" style="grid-column: 1; grid-row: 3;"></div>
        <div class="pane" style="grid-column: 3; grid-row: 3;"></div>
        
        <div class="matrix-right">""" + "".join(['<div class="cell"></div>' for _ in range(15)]) + """</div>
        <div class="indicator-pane"></div>
        <div class="control-pane"></div>
        <div class="matrix-bottom">""" + "".join(['<div class="cell"></div>' for _ in range(10)]) + """</div>
    </div>

    <script>
        const grid = document.getElementById('mainGrid');
        const vRed = document.getElementById('vRed');
        const hGreen = document.getElementById('hGreen');

        vRed.onmousedown = function(e) {
            document.onmousemove = function(e) {
                let p = (e.pageX / window.innerWidth) * 100;
                if(p > 10 && p < 90) grid.style.gridTemplateColumns = p + "% 5px 1fr 60px";
            };
            document.onmouseup = () => document.onmousemove = null;
        };

        hGreen.onmousedown = function(e) {
            document.onmousemove = function(e) {
                let p = (e.pageY / window.innerHeight) * 100;
                if(p > 10 && p < 90) grid.style.gridTemplateRows = p + "% 5px 1fr 80px";
            };
            document.onmouseup = () => document.onmousemove = null;
        };
    </script>
    """
    components.html(html_layout, height=1000)

if __name__ == "__main__":
    main()
