import streamlit as st
import json
import os

# --- 1. CORE APPLICATION CONFIGURATION ---
st.set_page_config(
    page_title="CAD DESIGNER PRO",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. THE MASTER SYSTEM REGISTRY & STATE ENGINE ---
if "current_view" not in st.session_state:
    st.session_state.current_view = "MAIN_CANVAS"
if "active_panel" not in st.session_state:
    st.session_state.active_panel = None

CONFIG_PATH = "config_layer/comutoy.json"
STATE_PATH = "config_layer/active_board_state.json"

def save_system_configuration(data, path=CONFIG_PATH):
    """Writes path mappings and configuration arrays directly to storage layer."""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        st.error(f"Configuration Write Failure: {str(e)}")

# --- 3. HIGH-DENSITY TERMINAL STYLING SHEETS ---
st.markdown("""
    <style>
    /* Global Background Settings matching image_007d38.png */
    .stApp {
        background-color: #000000;
        color: #00FF00;
        font-family: 'Courier New', Courier, monospace !important;
    }
    
    /* Main Central Workspace Canvas Style Rules */
    .canvas-border {
        border: 2px solid #333333;
        padding: 20px;
        height: 520px;
        background-color: #000000;
        color: #FFFFFF;
        position: relative;
    }
    
    /* Native Green System Prompt Text styling */
    .terminal-prompt-text {
        color: #00FF00 !important;
        font-weight: bold;
    }
    
    /* Bottom Status Activity Log Monitor Feed */
    .log-box {
        border: 1px solid #111111;
        background-color: #000000;
        padding: 10px;
        font-size: 12px;
        color: #00FF00;
        height: 180px;
        overflow-y: auto;
        white-space: pre-wrap;
    }
    
    /* Unmodified Native Grid Square Action Buttons (Far Right Deck) */
    div.native-square-deck button {
        background-color: #1a1a1a !important;
        color: #FFFFFF !important;
        border: 1px solid #333333 !important;
        border-radius: 4px !important;
        height: 32px !important;
        width: 100% !important;
        padding: 0px !important;
        font-size: 11px !important;
        font-weight: bold !important;
        transition: all 0.2s ease;
    }
    div.native-square-deck button:hover {
        border: 1px solid #00FF00 !important;
        color: #00FF00 !important;
        box-shadow: 0px 0px 5px #00FF00 !important;
    }
    
    /* Dynamic Target Styling for Activated Modules */
    div.active-target-btn button {
        background-color: #00FF00 !important;
        color: #000000 !important;
        border: 1px solid #00FF00 !important;
    }
    
    /* Side Chat Prompt Console Box Overlay rules */
    .chat-display {
        background-color: #000000;
        border-left: 1px solid #222222;
        padding: 10px;
        height: 400px;
        overflow-y: auto;
        color: #00FF00;
        font-size: 12px;
    }
    </style>
""", unsafe_allow_html=True)


# --- 4. STRUCTURAL WORKSPACE VIEWPORT LAYOUT ---
# 3-Column Split: 65% Main Canvas Area, 25% Chat Console, 10% Native Selection Button Matrix
col_canvas, col_chat, col_matrix = st.columns([6.5, 2.5, 1.0])


# === SECTION A: MAIN CENTRAL WORKSPACE CANVAS AREA ===
with col_canvas:
    if st.session_state.current_view == "MAIN_CANVAS":
        st.markdown('<div class="canvas-border">', unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; margin-top: 220px; color:#555555; font-weight:bold;'>[ IDLE: AWAITING CIRCUIT REQUEST ]</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    elif st.session_state.current_view == "REPO_SET":
        st.markdown('<div class="canvas-border" style="overflow-y: auto;">', unsafe_allow_html=True)
        st.markdown("<h4 style='color:#00FF00;'>⚙️ REPOSITORY & WORKFLOW CONTROL HUB</h4>", unsafe_allow_html=True)
        st.markdown("<hr style='border-color:#333333;'>", unsafe_allow_html=True)
        
        # --- REPO_SET.PY INLINE EXECUTED SUB-PANEL CONTROLS ---
        sub_col1, sub_col2, sub_col3 = st.columns(3)
        
        with sub_col1:
            if st.button("STORAGE", key="repo_panel_storage"):
                st.session_state.active_panel = "storage" if st.session_state.active_panel != "storage" else None
                st.rerun()
        with sub_col2:
            if st.button("BACK UP", key="repo_panel_backup"):
                st.session_state.active_panel = "backup" if st.session_state.active_panel != "backup" else None
                st.rerun()
        with sub_col3:
            if st.button("MILESTONE", key="repo_panel_milestone"):
                st.session_state.active_panel = "milestone" if st.session_state.active_panel != "milestone" else None
                st.rerun()
                
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Sub-Panel Target Operations Area
        if st.session_state.active_panel == "storage":
            st.markdown("<p style='color:#00FF00; font-weight:bold;'>📁 Primary Workspace Storage Setup</p>", unsafe_allow_html=True)
            p_provider = st.selectbox("Active Cloud Workspace Target Engine", ["Google Drive", "Dropbox", "Local PC Directory Only"])
            l_path = st.text_input("Active PC Workspace Folder Route (D:/)", "D:/Project_Mothership/temp_workspace")
            c_path = st.text_input("System Cache Temporary Operations Storage Directory", "D:/Project_Mothership/temp_workspace/cache")
            if st.button("[ SAVE STORAGE TARGETS ]"):
                save_system_configuration({"primary_provider": p_provider, "local_path": l_path, "cache_path": c_path})
                st.success("Primary path mapping records written cleanly to config_layer.")
                
        elif st.session_state.active_panel == "backup":
            st.markdown("<p style='color:#00FF00; font-weight:bold;'>🛡️ Redundant Mirroring Configurations</p>", unsafe_allow_html=True)
            b_provider = st.selectbox("Secondary Cold Storage Target Vault", ["Dropbox", "Google Drive", "AWS S3 Cloud Server Instance"])
            s_freq = st.slider("Automated Cloud Sync Mirror Frequency (Hours)", 1, 24, 6)
            if st.button("[ SAVE BACKUP MATRIX POLICIES ]"):
                save_system_configuration({"backup_provider": b_provider, "sync_frequency_hours": s_freq})
                st.success("Redundancy configurations updated successfully.")
                
        elif st.session_state.active_panel == "milestone":
            st.markdown("<p style='color:#00FF00; font-weight:bold;'>🎯 Milestone Target Checkpoints & Rules Pipeline</p>", unsafe_allow_html=True)
            m1 = st.checkbox("Milestone 1: Web Component Sourcing Clearance (Luvia AI Engine API)", value=True)
            m2 = st.checkbox("Milestone 2: Schematic Capture Validation (Flux.ai Schema Parsing)", value=True)
            m3 = st.checkbox("Milestone 3: Deep Headless Wave Simulation (KiCad Core SPICE Engine)", value=True)
            m4 = st.checkbox("Milestone 4: Trace Georouting Integrity Verification (Quilter CAM Engine)", value=True)
            m5 = st.checkbox("Milestone 5: 3D Enclosure Collision Check (nTop/Fusion Physics Rules)", value=False)
            auto_mode = st.radio("Automation Rule Selection", ["Fully Automated Execution Flow", "Human Checkpoint Intercept Rules"])
            if st.button("[ LOCK MILESTONE COMPLIANCE TEMPLATE ]"):
                save_system_configuration({
                    "m1": m1, "m2": m2, "m3": m3, "m4": m4, "m5": m5, "mode": auto_mode
                }, path=STATE_PATH)
                st.success("Fixed guidelines anchored to centralized whiteboard memory file.")

        # Bottom Row: Centered Close Action Block with Two Expansion Bays
        st.markdown("<br><hr style='border-color:#222222;'>", unsafe_allow_html=True)
        b_row1, b_row2, b_row3 = st.columns([1.5, 1.0, 1.5])
        with b_row1:
            st.empty()  
        with b_row2:
            if st.button("CLOSE", key="repo_panel_close"):
                st.session_state.current_view = "MAIN_CANVAS"
                st.session_state.active_panel = None
                st.rerun()
        with b_row3:
            st.empty()  
            
        st.markdown('</div>', unsafe_allow_html=True)

    # Core Terminal Real-Time Status Feed Bar
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="terminal-prompt-text">&gt;_ SYSTEM LIVE TRANSMISSION MONITOR LOGS</p>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="log-box">&gt;_ SYSTEM CORE INITIATED NATIVELY... SUCCESS
&gt;_ CONFIG_SAVE: MATRIX FLAGGED IN SYSTEM_LEARNING_LOOP.JSON
&gt;_ DETECTED ACTIVE CHANNELS: 5 DOMAIN ENGINEERING AGENTS STANDBY
&gt;_ CONFERENCE BROADCAST PROTOCOL LINK: ONLINE
&gt;_ SYSTEM STATUS: OPERATIONAL MIGRATION READY
&gt;_ INTERFACE VIEW RECOGNIZED PORT: {st.session_state.current_view}</div>
    """, unsafe_allow_html=True)


# === SECTION B: RIGHT-HAND SIDE CHAT PROMPT PANEL ===
with col_chat:
    st.markdown('<div class="chat-display">', unsafe_allow_html=True)
    st.markdown("**\*\*MATLAB:\*\*** Type `clear all` and press Enter. This clears all variables, functions, and MEX-files from the workspace.<br><br>**\*\*R:\*\*** Type `rm(list = ls())` and press Enter. This removes all objects from the current workspace.<br><br>**\*\*Python (Jupyter/IPython Notebook):\*\*** There isn't a direct equivalent to `clear all` for all variables at once without restarting the kernel. You can restart the kernel to clear all variables and execution history. For individual variables, you use `del variable_name`. * **\*\*Spyder (Python IDE):\*\*** There's usually a button or menu option to clear all variables in the 'Variable Explorer' pane. 3. **\*\*Clear cache/cookies/history in a web browser:\*\*** This is usually done through the browser's settings or history menu (e.g., 'Clear browsing data'). 4. **\*\*Clear notifications/alerts on a device:\*\*** This is usually an option within the notification shade or settings. Let me know what you're trying to do, and I can give you more specific instructions!", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.text_input("", value="TYPE HERE...", label_visibility="collapsed")
    
    # Bottom App Control Triggers
    b_col1, b_col2, b_col3 = st.columns(3)
    with b_col1:
        st.selectbox("", ["File"], label_visibility="collapsed", key="file_nav_drop")
    with b_col2:
        st.selectbox("", ["Tools"], label_visibility="collapsed", key="tools_nav_drop")
    with b_col3:
        st.selectbox("", ["View"], label_visibility="collapsed", key="view_nav_drop")


# === SECTION C: UNMODIFIED NATIVE DOUBLE-BUTTON STACK GRID ===
with col_matrix:
    st.markdown('<div class="native-square-deck">', unsafe_allow_html=True)
    
    # Row 1: The original unmerged dual button layout
    grid_col_1, grid_col_2 = st.columns(2)
    with grid_col_1:
        if st.session_state.current_view == "REPO_SET":
            st.markdown('<div class="active-target-btn">', unsafe_allow_html=True)
            
        if st.button("RP", key="native_slot_row1_left", help="Open Repository and Storage Hub"):
            st.session_state.current_view = "REPO_SET" if st.session_state.current_view != "REPO_SET" else "MAIN_CANVAS"
            st.rerun()
            
        if st.session_state.current_view == "REPO_SET":
            st.markdown('</div>', unsafe_allow_html=True)
            
    with grid_col_2:
        st.button("FS", key="native_slot_row1_right", help="Folder Structure Configuration Panel")
        
    # Rows 2 to 15: Pristine dual placeholder square layout mapping image_007d38.png
    for row_idx in range(2, 16):
        g_left, g_right = st.columns(2)
        with g_left:
            st.button("", key=f"native_btn_L_{row_idx}")
        with g_right:
            st.button("", key=f"native_btn_R_{row_idx}")
            
    st.selectbox("", ["AI-SET"], label_visibility="collapsed", key="ai_set_footer_drop")
    st.markdown('</div>', unsafe_allow_html=True)
