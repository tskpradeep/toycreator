import streamlit as st
import importlib
import sys

# --- CONFIG MASTER FRAME ---
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# --- HIGH-DENSITY TERMINAL STYLE SHEET ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00FF00; font-family: 'Courier New', monospace; }
    
    /* Merged Right-Hand Control Deck Button Array */
    div.merged-deck button {
        background-color: #000000 !important;
        color: #00FF00 !important;
        border: 2px solid #00FF00 !important;
        border-radius: 6px !important;
        font-weight: bold !important;
        font-size: 13px !important;
        padding: 12px 2px !important;
        width: 100% !important;
        margin-bottom: 8px !important;
    }
    div.merged-deck button:hover {
        background-color: #00FF00 !important;
        color: #000000 !important;
        box-shadow: 0px 0px 10px #00FF00 !important;
    }
    
    /* Workspace Borders */
    .canvas-border { border: 2px solid #333333; padding: 20px; height: 500px; background-color: #050505; }
    .log-box { border: 1px solid #00FF00; background-color: #020202; padding: 10px; font-size: 11px; height: 180px; overflow-y: scroll; }
    </style>
""", unsafe_allowed_with_html=True)

# Initialize global tracking session navigation rules
if "current_view" not in st.session_state:
    st.session_state.current_view = "MAIN_CANVAS"

# --- MAIN RENDER APPLICATION MATRIX ---
# Layout allocation: 90% Workspace/Logs Area, 10% Merged Right-Hand Action Deck
main_layout, control_deck = st.columns([9, 1])

with main_layout:
    # Top Section: Active Content Display Area
    if st.session_state.current_view == "MAIN_CANVAS":
        st.markdown('<div class="canvas-border">', unsafe_allowed_with_html=True)
        st.subheader("[ IDLE: AWAITING CIRCUIT REQUEST ]")
        st.caption("Broadcast state engine online. 5 Specialized Domain AI instances sitting in conference room standby mode.")
        st.markdown('</div>', unsafe_allowed_with_html=True)
        
    elif st.session_state.current_view == "REPO_SET":
        # Dynamic Native Context Mounting for repo_set panel
        st.markdown('<div class="canvas-border" style="height:auto; overflow-y:auto;">', unsafe_allowed_with_html=True)
        if os.path.exists("engineering_windows/repo_set.py"):
            with open("engineering_windows/repo_set.py") as f:
                exec(f.read())
        else:
            st.warning("repo_set.py target sub-module missing from path environment index.")
        st.markdown('</div>', unsafe_allowed_with_html=True)

    st.markdown("<br>", unsafe_allowed_with_html=True)
    
    # Bottom Section: Shared System Infrastructure Real-Time Feed
    st.markdown("**&gt;_ SYSTEM LOG TERMINAL FEED**")
    st.markdown("""
        <div class="log-box">
        &gt;_ SYSTEM INITIALIZED SUCCESSFULLY<br>
        &gt;_ CONFIG_SAVE: STATUS DIRECTORY LOADED FROM COMUTOY.JSON<br>
        &gt;_ DISPATCH: CENTRAL PROTOCOL HANDSHAKE VERIFIED COMPLIANT<br>
        &gt;_ BROADCAST ENGINE: ACTIVE_BOARD_STATE LEDGER MONITORING STARTED<br>
        &gt;_ READY: SYSTEM STATUS ACTIVE / PORTABLE MATRIX HUB ONLINE
        </div>
    """, unsafe_allowed_with_html=True)

with control_deck:
    st.markdown('<div class="merged-deck">', unsafe_allowed_with_html=True)
    st.markdown("<p style='color:#FFFFFF; font-size:11px; text-align:center; font-weight:bold;'>CONTROL DECK</p>", unsafe_allowed_with_html=True)
    
    # Merged Button Assignments 
    if st.button("REPO SET", key="btn_merged_1"):
        st.session_state.current_view = "REPO_SET" if st.session_state.current_view != "REPO_SET" else "MAIN_CANVAS"
        st.rerun()
        
    if st.button("FILE STRUCT", key="btn_merged_2"):
        st.session_state.current_view = "FILE_STRUCT"
        
    if st.button("AI PROMPTS", key="btn_merged_3"):
        st.session_state.current_view = "AI_PROMPTS"
        
    if st.button("MILESTONES", key="btn_merged_4"):
        st.session_state.current_view = "MILESTONES"
        
    # Vertical Expansion Padding matching the blank elements on the right of your drawing
    for i in range(5, 15):
        st.button(f"BAY SLOT {i}", key=f"btn_merged_{i}")
        
    st.markdown('</div>', unsafe_allowed_with_html=True)
