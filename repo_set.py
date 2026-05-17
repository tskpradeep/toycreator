import streamlit as st
import json
import os

# --- PAGE LAYOUT CONFIGURATION ---
st.set_page_config(
    page_title="System Configuration Hub",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- HIGH-DENSITY CYBERPUNK STYLING ---
st.markdown("""
    <style>
    /* Main application background override */
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
    }
    
    /* Cyberpunk Bright Neon Green Button Array */
    div.stButton > button {
        background-color: #000000 !important;
        color: #00FF00 !important;
        border: 2px solid #00FF00 !important;
        border-radius: 12px !important;
        font-size: 20px !important;
        font-weight: bold !important;
        font-family: 'Courier New', Courier, monospace !important;
        padding: 15px 10px !important;
        width: 100% !important;
        transition: all 0.3s ease-in-out;
    }
    
    /* Button Hover Interaction */
    div.stButton > button:hover {
        background-color: #00FF00 !important;
        color: #000000 !important;
        box-shadow: 0px 0px 15px #00FF00 !important;
    }
    
    /* Dedicated Styling for the Central Close Action Block */
    .close-container button {
        font-size: 14px !important;
        padding: 8px 5px !important;
        border-radius: 8px !important;
    }
    
    /* Configuration Section Callouts */
    .config-card {
        border: 1px solid #333333;
        padding: 20px;
        border-radius: 10px;
        background-color: #111111;
        margin-top: 15px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allowed_with_html=html)

# --- STATE MANAGEMENT LOGIC ---
CONFIG_PATH = "../config_layer/comutoy.json"
STATE_PATH = "../config_layer/active_board_state.json"

# Initialize Session State Variables cleanly
if "active_panel" not in st.session_state:
    st.session_state.active_panel = None

def save_system_configuration(data, path=CONFIG_PATH):
    """Writes dynamic path maps and settings straight to config layer."""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        st.error(f"Configuration Write Failure: {str(e)}")

# --- CORE USER INTERFACE CANVAS ---
st.title("⚙️ REPOSITORY & WORKFLOW CONTROL HUB")
st.markdown("---")

# 1. TOP ROW: THE PRIMARY PANEL TOGGLES (3-Column Layout from Sketch)
top_col1, top_col2, top_col3 = st.columns(3)

with top_col1:
    if st.button("STORAGE"):
        st.session_state.active_panel = "storage" if st.session_state.active_panel != "storage" else None

with top_col2:
    if st.button("BACK UP"):
        st.session_state.active_panel = "backup" if st.session_state.active_panel != "backup" else None

with top_col3:
    if st.button("MILESTONE"):
        st.session_state.active_panel = "milestone" if st.session_state.active_panel != "milestone" else None


# 2. DYNAMIC ACTIVE WORKSPACE REGION (Decoupled & Isolated)
if st.session_state.active_panel == "storage":
    st.markdown('<div class="config-card">', unsafe_allowed_with_html=True)
    st.subheader("📁 Primary Workspace Storage Configuration")
    
    primary_provider = st.selectbox("Primary Cloud Provider Asset Mirror", ["Google Drive", "Dropbox", "Local Target Only"])
    local_path = st.text_input("Active PC Local Path Directory Mapping (D:/)", "D:/Project_Mothership/temp_workspace")
    cache_path = st.text_input("System Cache Ephemeral Operations Directory", "D:/Project_Mothership/temp_workspace/cache")
    
    if st.button("[ SAVE STORAGE MAPPINGS ]"):
        payload = {"primary_provider": primary_provider, "local_path": local_path, "cache_path": cache_path}
        save_system_configuration(payload)
        st.success("Storage Layer Mapping Updated In Local Config.")
    st.markdown('</div>', unsafe_allowed_with_html=True)

elif st.session_state.active_panel == "backup":
    st.markdown('<div class="config-card">', unsafe_allowed_with_html=True)
    st.subheader("🛡️ Redundancy & Cold Backup Protocols")
    
    backup_provider = st.selectbox("Secondary Redundant Mirror Target", ["Dropbox", "Google Drive", "AWS S3 Glacial Instance"])
    sync_frequency = st.slider("Automated Cloud Mirror Interval (Hours)", 1, 24, 6)
    
    if st.button("[ SAVE BACKUP POLICIES ]"):
        payload = {"backup_provider": backup_provider, "sync_frequency_hours": sync_frequency}
        save_system_configuration(payload)
        st.success("Backup Matrix State Updated Globally.")
    st.markdown('</div>', unsafe_allowed_with_html=True)

elif st.session_state.active_panel == "milestone":
    st.markdown('<div class="config-card">', unsafe_allowed_with_html=True)
    st.subheader("🎯 Milestone Flow & Verification Guidelines")
    st.info("Define the fixed checkpoints, tools, and constraints for this architecture layer.")
    
    # User-defined guideline matrices mapping tools directly to gates
    m1 = st.checkbox("Milestone 1: Web Selection Layer (Luvia AI Component API Verification)", value=True)
    m2 = st.checkbox("Milestone 2: Schematic Lock (Flux.ai .json Netlist Rule Verification)", value=True)
    m3 = st.checkbox("Milestone 3: Deep Technical Simulation (KiCad Local Headless SPICE Validation)", value=True)
    m4 = st.checkbox("Milestone 4: Geo-Routing Verification (Quilter ODB++ Autoroute Assessment)", value=True)
    m5 = st.checkbox("Milestone 5: Enclosure Integration (nTop/Fusion Physics Step Validation)", value=False)
    
    st.markdown("---")
    automation_mode = st.radio("Automation Constraint Rule Setup", [
        "Full Automated Pipeline (Conference Room AI Auto-Pass)",
        "Human-in-the-Loop Intercept (Pause at Checked Milestones for Manual Verification)"
    ])
    
    if st.button("[ LOCK MILESTONE COMPLIANCE ROADMAP ]"):
        milestone_map = {
            "m1_selection": m1, "m2_schematic": m2, "m3_analysis": m3, 
            "m4_layout": m4, "m5_enclosure": m5, "operational_mode": automation_mode
        }
        save_system_configuration(milestone_map, path=STATE_PATH)
        st.success("Milestone Guidelines Anchored to Active Board State Ledger.")
    st.markdown('</div>', unsafe_allowed_with_html=True)


# 3. MIDDLE & BOTTOM ROW: CONTROL TERMINATION AND RESERVED EXPANSION BAYS
st.markdown("<br><br>", unsafe_allowed_with_html=True)
bottom_col1, bottom_col2, bottom_col3 = st.columns([1.5, 1, 1.5])

with bottom_col1:
    # Blank Slot 1: Reserved for future Left Expansion Panel Hooks
    st.empty()

with bottom_col2:
    # Centered Master Close Button Anchor Block
    st.markdown('<div class="close-container">', unsafe_allowed_with_html=True)
    if st.button("CLOSE"):
        st.session_state.active_panel = None
        st.info("Returning to Core Grade Dashboard Canvas Area...")
    st.markdown('</div>', unsafe_allowed_with_html=True)

with bottom_col3:
    # Blank Slot 2: Reserved for future Right Expansion Panel Hooks
    st.empty()
