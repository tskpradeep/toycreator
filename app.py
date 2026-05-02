import streamlit as st
import os

# Rule 10 & 11: Provider Independent and Frozen Logic
st.set_page_config(layout="wide", page_title="Engineering Workbench", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* Rule 6: Minimalist/Plain Gray Background */
    .block-container { padding: 0 !important; background-color: #d3d3d3; height: 100vh; overflow: hidden; }
    header, footer { visibility: hidden; }

    /* Rigid 1:1 Grid Construction */
    .master-grid {
        display: grid;
        grid-template-columns: 1fr 5px 350px 80px;
        grid-template-rows: 1fr 5px 180px 100px;
        height: 100vh;
        width: 100vw;
        border: 2px solid black;
    }

    /* Partitions - Rule 7: Verified real CSS properties */
    .v-partition { grid-column: 2; grid-row: 1 / 4; background-color: red; cursor: col-resize; }
    .h-partition { grid-row: 2; grid-column: 1; background-color: green; cursor: row-resize; }
    .h-partition-right { grid-row: 2; grid-column: 3; background-color: green; cursor: row-resize; }

    /* Content Styling per image_a30e62.png */
    .cell { padding: 10px; font-family: "Courier New", Courier, monospace; overflow: auto; }
    .title-visual { color: #800000; font-size: 24px; font-weight: bold; }
    .title-ai { color: #008000; font-weight: bold; }
    .title-user { color: #800080; font-weight: bold; }
    .cmd-text { color: #ff0000; font-weight: bold; }

    /* Matrix Buttons - Rule 5: Suggested only one fit */
    .matrix-sq {
        width: 25px; height: 25px;
        background-color: black;
        border: 1px solid white;
        display: inline-block;
        margin: 2px;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    # --- FROZEN AUTHENTICATION ---
    if 'category' not in st.session_state: st.session_state['category'] = None
    if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False

    if st.session_state['category'] is None:
        show_category_selection()
    elif not st.session_state['logged_in']:
        show_login_page()
    else:
        show_workbench()

def show_category_selection():
    st.title("System Domain")
    cat = st.radio("Select Domain:", ["Consumer Electronics", "Industrial Automation", "Military Systems"])
    if st.button("Initialize"):
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

# --- 1:1 WORKBENCH ---
def show_workbench():
    # Use raw HTML for the grid to ensure partitions touch the edges exactly
    matrix_html = "".join(['<div class="matrix-sq"></div>' for _ in range(12)])
    rare_btns_html = "".join(['<div class="matrix-sq" style="display:block; margin: 10px auto;"></div>' for _ in range(8)])

    st.markdown(f"""
    <div class="master-grid">
        <!-- TOP LEFT -->
        <div class="cell" style="grid-column: 1; grid-row: 1;">
            <div class="title-visual">visual displays dynamic between coding and screen/CAD designs</div>
        </div>
        
        <!-- RED VERTICAL PARTITION -->
        <div class="v-partition"></div>
        
        <!-- TOP RIGHT -->
        <div class="cell" style="grid-column: 3; grid-row: 1;">
            <div class="title-ai">AI TEXT REPLYING WINDOW</div>
        </div>

        <!-- GREEN HORIZONTAL PARTITIONS -->
        <div class="h-partition"></div>
        <div class="h-partition-right"></div>

        <!-- COMMAND PROMPT -->
        <div class="cell" style="grid-column: 1; grid-row: 3;">
            <div class="cmd-text">command prompt for system programming for project</div>
        </div>

        <!-- USER PROMPTING -->
        <div class="cell" style="grid-column: 3; grid-row: 3;">
            <div class="title-user">USER PROMPTING</div>
            <textarea style="width:100%; height:100px; background:#eee; border:1px solid black;"></textarea>
        </div>

        <!-- RARE BUTTONS WALL -->
        <div style="grid-column: 4; grid-row: 1 / 4; border-left: 1px solid black; background: #c0c0c0;">
            <div style="text-align:center; font-size:10px; padding:5px;">REARLLY USED</div>
            {rare_btns_html}
        </div>

        <!-- FOOTER LEFT -->
        <div style="grid-column: 1; grid-row: 4; display: flex; border-top: 1px solid black;">
            <div style="width:30%; border-right:1px solid black; color:green; padding:5px;">small indicators any</div>
            <div style="width:70%; color:blue; padding:5px;">buttons for controlling we will decide buttons as and when we</div>
        </div>

        <!-- FOOTER RIGHT (MATRIX) -->
        <div style="grid-column: 3 / 5; grid-row: 4; border-top: 1px solid black; padding: 10px; background: #808080;">
            {matrix_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
