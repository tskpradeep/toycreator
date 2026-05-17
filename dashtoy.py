import streamlit as st
import json
import os

# --- 1. INITIALIZE MASTER PAGE RULES ---
st.set_page_config(
    page_title="CAD DESIGNER PRO",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. PERSISTENT CORE RUNTIME MEMORY STATE ---
if "current_view" not in st.session_state:
    st.session_state.current_view = "MAIN_CANVAS"
if "active_panel" not in st.session_state:
    st.session_state.active_panel = None

CONFIG_PATH = "config_layer/comutoy.json"
STATE_PATH = "config_layer/active_board_state.json"

def save_system_configuration(data, path=CONFIG_PATH):
    """Securely updates the centralized local configuration files."""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        st.error(f"Write Fault: {str(e)}")

# --- 3. THE MASTER GRID RESTORATION CSS (Unlocks Pixel-Perfect Alignment) ---
st.markdown("""
    <style>
    /* Absolute reset to match image_007d38.png black terminal spec */
    .stApp {
        background-color: #000000 !important;
        color: #00FF00 !important;
        font-family: 'Courier New', Courier, monospace !important;
    }
    
    /* Strict global block override to force pure desktop multi-column layouts */
    [data-testid="stHorizontalBlock"] {
        background-color: #000000 !important;
        gap: 10px !important;
    }

    /* Fixed Border Frame for Central Workbench Layout Area */
    .canvas-border {
        border: 2px solid #333333 !important;
        padding: 15px;
        height: 500px;
        background-color: #000000;
        color: #FFFFFF;
        overflow-y: auto;
    }
    
    /* Green status text highlighting rules */
    .status-text-green {
        color: #00FF00 !important;
        font-weight: bold;
        font-size: 13px;
        margin-top: 10px;
    }
    
    /* Low-Profile Status Bottom Activity Monitor Logs Console */
    .log-box {
        border: 1px solid #222222 !important;
        background-color: #000000 !important;
        padding: 8px;
        font-size: 12px;
        color: #00FF00 !important;
        height: 160px;
        overflow-y: auto;
        white-space: pre-wrap;
        font-family: 'Courier New', monospace;
    }
    
    /* Pristine Right Edge Selection Command Double-Button Grid */
    div.native-square-deck button {
        background-color: #1a1a1a !important;
        color: #FFFFFF !important;
        border: 1px solid #333333 !important;
        border-radius: 2px !important;
        height: 30px !important;
        width: 100% !important;
        padding: 0px !important;
        font-size: 11px !important;
        font-weight: bold !important;
    }
    div.native-square-deck button:hover {
        border: 1px solid #00FF00 !important;
        color: #00FF00 !important;
    }
    
    /* Active Highlighting Matrix without resizing elements */
    div.active-target-btn button {
        background-color: #00FF00 !important;
        color: #000000 !important;
        border: 1px solid #00FF00 !important;
    }
    
    /* Right Side Diagnostic Instruction Console Text Frame */
    .chat-display {
        background-color: #000000;
        border: 1px solid #333333;
        padding: 12px;
        height: 460px;
        overflow-y: auto;
        color: #00FF00;
        font-size: 12px;
        line-height: 1.4;
    }
    
    /* Inner Configuration Hub Sub-Panel Layout Grid Buttons */
    div.repo-hub-btn button {
        background-color: #000000 !important;
        color: #00FF00 !important;
        border: 2px solid #00FF00 !important;
        border-radius: 10px !important;
        font-size: 16px !important;
        font-weight: bold !important;
        padding: 10px 5px !important;
    }
    div.repo-hub-btn button:hover {
        background-color: #00FF00 !important;
        color: #000000 !important;
    }
    </style>
""", unsafe_allow_html=True)


# --- 4. PRESERVED THREE-ZONE VIEWPORT GRAPHICAL FRAME ---
# Layout proportions meticulously set to completely protect screen real estate
col_canvas, col_chat, col_matrix = st.columns([6.8, 2.4, 0.8])


# =========================================================================
# ZONE A: CENTRAL MAIN COMMAND BENCH PLATFORM
# =========================================================================
with col_canvas:
    if st.session_state.current_view == "MAIN_CANVAS":
        st.markdown('<div class="canvas-border">', unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; margin-top: 220px; color:#444444; font-weight:bold; letter-spacing: 1px;'>[ IDLE: AWAITING CIRCUIT REQUEST ]</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allowed_with_html=True)
        
    elif st.session_state.current_view == "REPO_SET":
        st.markdown('<div class="canvas-border">', unsafe_allow_html=True)
        st.markdown("<p style='color:#00FF00; font-size:16px; margin:0; font-weight:bold;'>⚙️ REPOSITORY & WORKFLOW CONTROL HUB</p>", unsafe_allow_html=True)
        st.markdown("<hr style='margin:10px 0; border-color:#222222;'>", unsafe_allow_html=True)
        
        # Inner Toggle Row Structure 
        sub_col1, sub_col2, sub_col3 = st.columns(3)
        with sub_col1:
            st.markdown('<div class="repo-hub-btn">', unsafe_allow_html=True)
            if st.button("STORAGE", key="sub_panel_storage"):
                st.session_state.active_panel = "storage" if st.session_state.active_panel != "storage" else None
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with sub_col2:
            st.markdown('<div class="repo-hub-btn">', unsafe_allow_html=True)
            if st.button("BACK UP", key="sub_panel_backup"):
                st.session_state.active_panel = "backup" if st.session_state.active_panel != "backup" else None
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with sub_col3:
            st.markdown('<div class="repo-hub-btn">', unsafe_allow_html=True)
            if st.button("MILESTONE", key="sub_panel_milestone"):
                st.session_state.active_panel = "milestone" if st.session_state.active_panel != "milestone" else None
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Sub-Panel Interactive Configuration Form Fields
        if st.session_state.active_panel == "storage":
            st.markdown("<p style='color:#00FF00; font-weight:bold;'>📁 Active Workspace Destination Settings</p>", unsafe_allow_html=True)
            p_prov = st.selectbox("Active Cloud Workspace Target Engine", ["Google Drive", "Dropbox", "Local PC Directory Only"])
            l_pth = st.text_input("Active PC Workspace Folder Route (D:/)", "D:/Project_Mothership/temp_workspace")
            c_pth = st.text_input("System Cache Temporary Operations Storage Directory", "D:/Project_Mothership/temp_workspace/cache")
            if st.button("[ UPDATE STORAGE ROUTING RECORDS ]"):
                save_system_configuration({"primary_provider": p_prov, "local_path": l_pth, "cache_path": c_pth})
                st.success("Primary path mapping lines committed cleanly to comutoy.json index.")
                
        elif st.session_state.active_panel == "backup":
            st.markdown("<p style='color:#00FF00; font-weight:bold;'>🛡️ Redundant Synchronization Strategies</p>", unsafe_allow_html=True)
            b_prov = st.selectbox("Secondary Redundant Storage Target Vault", ["Dropbox", "Google Drive", "AWS S3 Cloud Server Instance"])
            s_frq = st.slider("Automated Cloud Sync Mirror Frequency (Hours)", 1, 24, 6)
            if st.button("[ WRITE SECURITY PROTOCOLS ]"):
                save_system_configuration({"backup_provider": b_prov, "sync_frequency_hours": s_frq})
                st.success("Redundancy rules written to config space storage mapping.")
                
        elif st.session_state.active_panel == "milestone":
            st.markdown("<p style='color:#00FF00; font-weight:bold;'>🎯 Custom Project Verification Checkpoints Pipeline</p>", unsafe_allow_html=True)
            m1 = st.checkbox("Milestone 1: Web Component Sourcing Clearance (Luvia AI Engine API)", value=True)
            m2 = st.checkbox("Milestone 2: Schematic Capture Validation (Flux.ai Schema Parsing)", value=True)
            m3 = st.checkbox("Milestone 3: Deep Headless Wave Simulation (KiCad Core SPICE Engine)", value=True)
            m4 = st.checkbox("Milestone 4: Trace Georouting Integrity Verification (Quilter CAM Engine)", value=True)
            m5 = st.checkbox("Milestone 5: 3D Enclosure Collision Check (nTop/Fusion Physics Rules)", value=False)
            a_mode = st.radio("Automation Rule Settings", ["Fully Automated Pipeline Operation", "Human Decision Boundary Hold Rules"])
            if st.button("[ LOCK FIXED GUIDELINE MATRIX ]"):
                save_system_configuration({"m1": m1, "m2": m2, "m3": m3, "m4": m4, "m5": m5, "mode": a_mode}, path=STATE_PATH)
                st.success("Milestone execution blueprints bound to live board state ledger.")

        # Bottom Sub-Panel Footing Row containing the Closed Button and Blank Bays
        st.markdown("<br><hr style='margin:5px 0; border-color:#222222;'>", unsafe_allow_html=True)
        fn_col1, fn_col2, fn_col3 = st.columns([1.5, 1.0, 1.5])
        with fn_col1:
            st.empty() # Blank Expansion Spot 1
        with fn_col2:
            if st.button("CLOSE", key="sub_panel_master_close"):
                st.session_state.current_view = "MAIN_CANVAS"
                st.session_state.active_panel = None
                st.rerun()
        with fn_col3:
            st.empty() # Blank Expansion Slot 2
            
        st.markdown('</div>', unsafe_allow_html=True)

    # Output Console Region Setup (Untouched positioning)
    st.markdown('<p class="status-text-green">&gt;_ SYSTEM REAL-TIME INFRASTRUCTURE TERMINAL FEED</p>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="log-box">&gt;_ CORE HOST LINKED UP VIA SECURE PIPELINE LOOPS... SUCCESS
&gt;_ DETECTED RUNTIME STATUS: 5 SPECIALIZED DATA DOMAIN ENGINEERING AGENTS ACTIVE
&gt;_ SYNCHRONIZED BROADCAST MATRIX WHITEBOARD REDIRECT STATUS: RUNNING
&gt;_ SYSTEM STORAGE OWNER ROOT PORTABLE ACCESS ENGINES: COMPLIANT
&gt;_ INTERFACE VIEW RECOGNIZED SYSTEM CHANNEL: PORT_{st.session_state.current_view}</div>
    """, unsafe_allow_html=True)


# =========================================================================
# ZONE B: CENTRAL CAD SIDE CHAT CONSOLE DISPLAY
# =========================================================================
with col_chat:
    st.markdown(
        '<div class="chat-display">'
        '****MATLAB:**** Type `clear all` and press Enter. This clears all variables, functions, and MEX-files from the workspace.<br><br>'
        '****R:**** Type `rm(list = ls())` and press Enter. This removes all objects from the current workspace.<br><br>'
        '****Python (Jupyter/IPython Notebook):**** There isn\'t a direct equivalent to `clear all` for all variables at once without restarting the kernel. You can restart the kernel to clear all variables and execution history. For individual variables, you use `del variable_name`. * ****Spyder (Python IDE):**** There\'s usually a button or menu option to clear all variables in the "Variable Explorer" pane. 3. ****Clear cache/cookies/history in a web browser:**** This is usually done through the browser\'s settings or history menu (e.g., "Clear browsing data"). 4. ****Clear notifications/alerts on a device:**** This is usually an option within the notification shade or settings. Let me know what you\'re trying to do, and I can give you more specific instructions!'
        '</div>', 
        unsafe_allow_html=True
    )
    st.text_input("Console Input Line Entry Point", value="TYPE HERE...", label_visibility="collapsed", key="terminal_input_line")
    
    # Custom Row Menu Nav Selection Dropdowns
    drop_col1, drop_col2, drop_col3 = st.columns(3)
    with drop_col1:
        st.selectbox("F_Menu", ["File"], label_visibility="collapsed", key="sys_drop_file")
    with drop_col2:
        st.selectbox("T_Menu", ["Tools"], label_visibility="collapsed", key="sys_drop_tools")
    with drop_col3:
        st.selectbox("V_Menu", ["View"], label_visibility="collapsed", key="sys_drop_view")


# =========================================================================
# ZONE C: PRISTINE RIGHT-EDGE CONTROL DECK DOUBLE-BUTTON MATRIX GRID
# =========================================================================
with col_matrix:
    st.markdown('<div class="native-square-deck">', unsafe_allow_html=True)
    
    # Row 1: The original, separate twin action square button blocks
    row1_left, row1_right = st.columns(2)
    with row1_left:
        if st.session_state.current_view == "REPO_SET":
            st.markdown('<div class="active-target-btn">', unsafe_allow_html=True)
            
        if st.button("RP", key="native_grid_r1_c1", help="Launch Storage Deployment Panel"):
            st.session_state.current_view = "REPO_SET" if st.session_state.current_view != "REPO_SET" else "MAIN_CANVAS"
            st.rerun()
            
        if st.session_state.current_view == "REPO_SET":
            st.markdown('</div>', unsafe_allow_html=True)
            
    with row1_right:
        st.button("FS", key="native_grid_r1_c2", help="Folder Structure Design Interface")
        
    # Rows 2 through 15: Restored unmerged dual-grid square button layout arrays
    for row_idx in range(2, 16):
        left_grid_block, right_grid_block = st.columns(2)
        with left_grid_block:
            st.button("", key=f"native_square_L_{row_idx}")
        with right_grid_block:
            st.button("", key=f"native_square_R_{row_idx}")
            
    st.selectbox("Engine Selector", ["AI-SET"], label_visibility="collapsed", key="matrix_bottom_ai_set")
    st.markdown('</div>', unsafe_allow_html=True)
