import streamlit as st
import os

# Rule 10: Provider Independent. Rule 1: High-Density CAD Style.
st.set_page_config(layout="wide", page_title="Engineering Workbench")

# Rule 6: No explanation of CSS, just the functional implementation.
st.markdown("""
    <style>
    .block-container { padding: 0.5rem 1rem !important; }
    div.stTextArea textarea { font-family: 'Consolas', monospace; font-size: 11px; }
    div.stContainer { border: 1px solid #999 !important; border-radius: 0px !important; }
    /* Thin splitter line style */
    .splitter { border-top: 1px solid #333; margin: 2px 0; text-align: center; font-size: 10px; color: #666; }
    </style>
    """, unsafe_allow_html=True)

def main():
    if 'category' not in st.session_state: st.session_state['category'] = None
    if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
    if 'vh' not in st.session_state: st.session_state['vh'] = 450

    if st.session_state['category'] is None:
        show_category_selection()
    elif not st.session_state['logged_in']:
        show_login_page()
    else:
        show_workbench()

# --- AUTH LOGIC (FROZEN) ---
def show_category_selection():
    st.title("System Selection")
    cat = st.radio("Domain", ["Consumer Electronics", "Industrial Automation", "Military Systems"])
    if st.button("Proceed"):
        st.session_state['category'] = cat
        st.rerun()

def show_login_page():
    suffix = st.session_state['category'].replace(' ', '_')
    filename = f"auth_{suffix}.txt"
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    with tab1:
        u = st.text_input("User")
        p = st.text_input("Pass", type="password")
        if st.button("Enter"):
            if check_credentials(u, p, filename):
                st.session_state['logged_in'] = True
                st.rerun()
    with tab2:
        nu = st.text_input("New User")
        np = st.text_input("New Pass", type="password")
        if st.button("Create"):
            with open(filename, "a") as f: f.write(f"{nu},{np}\n")

def check_credentials(u, p, filename):
    if not os.path.exists(filename): return False
    with open(filename, "r") as f:
        return f"{u},{p}" in [line.strip() for line in f.readlines()]

# --- WORKBENCH (CADENCE-STYLE DENSITY) ---
def show_workbench():
    # 1. TOP TOOL RIBBON (Engineering Style)
    ribbon = st.columns(15)
    icons = ["📄", "📁", "💾", "📐", "🔍", "⚡", "🧩", "🛠️", "🔗", "🔄", "⚙️", "🔒"]
    for i, icon in enumerate(icons):
        ribbon[i].button(icon, key=f"rib_{i}")

    # 2. MAIN LAYOUT (Mirroring Image 2)
    left_side, right_side = st.columns([0.75, 0.25])

    with left_side:
        # CAD Window (Top)
        st.container(height=st.session_state['vh'], border=True).write("CAD DRAWING ENGINE / DESIGN VIEW")
        
        # Professional Splitter (Rule 1: Compact/Manufacturable)
        st.markdown('<div class="splitter">▲ ADJUST VIEWPORT ▼</div>', unsafe_allow_html=True)
        sz_col1, sz_col2, _ = st.columns([0.1, 0.1, 0.8])
        if sz_col1.button("＋", key="inc"): st.session_state['vh'] += 50; st.rerun()
        if sz_col2.button("－", key="dec"): st.session_state['vh'] -= 50; st.rerun()

    with right_side:
        # AI Stack (Mirroring Image 2 Right Side)
        st.caption("AI ANALYSIS")
        st.container(height=350, border=True).write("Waiting for system instructions...")
        st.caption("USER PROMPT")
        st.text_input("CMD>", key="p_box", label_visibility="collapsed")
        st.button("SEND", use_container_width=True)

    # 3. FULL-WIDTH TERMINAL (Mirroring Image 2 Bottom)
    st.markdown("---")
    st.caption("COMMAND WINDOW / SESSION LOG")
    st.text_area("Log", "Ready.", height=120, label_visibility="collapsed")

if __name__ == "__main__":
    main()
