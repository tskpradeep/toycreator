import streamlit as st
import streamlit.components.v1 as components
import os

# PHASE 1 & 2: HARD-FROZEN INTEGRATED BASELINE
st.set_page_config(layout="wide", page_title="System Gateway", initial_sidebar_state="collapsed")

# CSS: FORCED CENTERING AND FIXED DIMENSIONS
st.markdown("""
    <style>
    /* Full Black Reset */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #000000 !important;
        margin: 0;
        padding: 0;
    }
    
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }

    header, footer { visibility: hidden !important; }

    /* AUTHENTICATION HUB: Fixed Width & Dead Center */
    .auth-container {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 320px;
        text-align: center;
        z-index: 9999;
    }

    /* Small Precise Input Bars */
    .stTextInput input {
        background-color: #000 !important;
        color: #00ff00 !important;
        border: 1px solid #444 !important;
        border-radius: 0px !important;
        text-align: center !important;
        height: 30px !important;
    }

    /* Engineering Typography */
    h2, h4, label, p, .stMarkdown { 
        color: #ffffff !important; 
        text-align: center !important; 
        font-family: 'Courier New', Courier, monospace !important;
        text-transform: uppercase;
    }

    /* Professional Buttons */
    .stButton>button {
        width: 100% !important;
        border-radius: 0px !important;
        background-color: #222 !important;
        color: white !important;
        border: 1px solid #444 !important;
        font-size: 12px !important;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    if 'category' not in st.session_state: st.session_state['category'] = None
    if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False

    if st.session_state['category'] is None:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        show_category_selection()
        st.markdown('</div>', unsafe_allow_html=True)
    elif not st.session_state['logged_in']:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        show_login_page()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Phase 2: 1:1 Dashboard Implementation based on image_1abf38.png
        show_phase2_dashboard()

def show_category_selection():
    st.markdown("## SYSTEM DOMAIN")
    cat = st.radio("DOMAIN", ["Consumer Electronics", "Industrial Automation", "Military Systems"], label_visibility="collapsed")
    if st.button("INITIALIZE"):
        st.session_state['category'] = cat
        st.rerun()

def show_login_page():
    st.markdown("## ACCESS PORTAL")
    st.markdown(f"<p style='color: #666;'>{st.session_state['category']}</p>", unsafe_allow_html=True)
    
    suffix = st.session_state['category'].replace(' ', '_')
    filename = f"auth_{suffix}.txt"
    
    u = st.text_input("USER", key="login_u", placeholder="ID", label_visibility="collapsed")
    p = st.text_input("PASS", type="password", key="login_p", placeholder="PASS", label_visibility="collapsed")
    
    if st.button("AUTHENTICATE"):
        if check_credentials(u, p, filename):
            st.session_state['logged_in'] = True
            st.rerun()
    
    if st.button("BACK"):
        st.session_state['category'] = None
        st.rerun()

def check_credentials(u, p, filename):
    if not os.path.exists(filename): return False
    with open(filename, "r") as f:
        return any(f"{u},{p}" == line.strip() for line in f)

def show_phase2_dashboard():
    # dashboard structure 1:1 as in image_1abf38.png
    # Red line (Vertical) and Green lines (Horizontal) are draggable
    dashboard_html = """
    <style>
        body { background-color: black; color: white; margin: 0; overflow: hidden; font-family: 'Courier New', monospace; }
        .wrapper { display: grid; grid-template-columns: 1fr 4px 300px 60px; grid-template-rows: 1fr 4px 180px 100px; height: 100vh; width: 100vw; border: 2px solid white; box-sizing: border-box; }
        
        .pane { border: 0.5px solid #222; display: flex; align-items: center; justify-content: center; position: relative; }
        
        /* Drag Dividers */
        .v-divider-red { grid-column: 2; grid-row: 1 / 4; background-color: red; cursor: col-resize; z-index: 100; }
        .h-divider-green { grid-column: 1 / 4; grid-row: 2; background-color: #00ff00; cursor: row-resize; z-index: 100; }
        
        /* Matrices */
        .matrix-side { grid-column: 4; grid-row: 1 / 4; display: grid; grid-template-rows: repeat(12, 1fr); border-left: 2px solid white; }
        .matrix-bottom { grid-column: 3 / 5; grid-row: 4; display: grid; grid-template-columns: repeat(5, 1fr); grid-template-rows: 1fr 1fr; border-top: 2px solid white; border-left: 2px solid white; }
        .cell { border: 1px solid white; }

        /* Bottom Control Bar */
        .indicator-box { grid-column: 1; grid-row: 4; border-top: 2px solid white; border-right: 2px solid white; width: 200px; }
        .control-buttons { grid-column: 1; grid-row: 4; border-top: 2px solid white; margin-left: 200px; }
    </style>

    <div class="wrapper" id="grid">
        <div class="pane" style="grid-column: 1; grid-row: 1;"></div>
        <div class="v-divider-red" id="vRed"></div>
        <div class="pane" style="grid-column: 3; grid-row: 1;"></div>
        
        <div class="h-divider-green" id="hGreen"></div>
        
        <div class="pane" style="grid-column: 1; grid-row: 3;"></div>
        <div class="pane" style="grid-column: 3; grid-row: 3;"></div>
        
        <div class="matrix-side">""" + "".join(['<div class="cell"></div>' for _ in range(12)]) + """</div>
        <div class="indicator-box"></div>
        <div class="control-buttons"></div>
        <div class="matrix-bottom">""" + "".join(['<div class="cell"></div>' for _ in range(10)]) + """</div>
    </div>

    <script>
        const grid = document.getElementById('grid');
        const vRed = document.getElementById('vRed');
        const hGreen = document.getElementById('hGreen');

        vRed.onmousedown = function() {
            document.onmousemove = function(e) {
                let x = (e.pageX / window.innerWidth) * 100;
                if(x > 20 && x < 85) grid.style.gridTemplateColumns = x + "% 4px 1fr 60px";
            };
            document.onmouseup = () => document.onmousemove = null;
        };

        hGreen.onmousedown = function() {
            document.onmousemove = function(e) {
                let y = (e.pageY / window.innerHeight) * 100;
                if(y > 20 && y < 80) grid.style.gridTemplateRows = y + "% 4px 1fr 100px";
            };
            document.onmouseup = () => document.onmousemove = null;
        };
    </script>
    """
    components.html(dashboard_html, height=2000)

if __name__ == "__main__":
    main()
