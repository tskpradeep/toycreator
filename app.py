import streamlit as st
import os

# Rule 10 & 11: Provider Independent and Frozen Logic
st.set_page_config(layout="wide", page_title="Workbench v1.5", initial_sidebar_state="collapsed")

# TOTAL RESET: Removes Streamlit's "web" look to allow the 1:1 Blueprint
st.markdown("""
    <style>
    /* Kill all Streamlit default spacing/padding */
    .block-container { padding: 0 !important; max-width: 100vw !important; height: 100vh !important; overflow: hidden !important; background-color: #d3d3d3; }
    header, footer { visibility: hidden !important; }
    [data-testid="stVerticalBlock"] { gap: 0 !important; }

    /* The Rigid 1:1 Master Grid */
    .blueprint-grid {
        display: grid;
        grid-template-columns: 1fr 4px 350px 80px; /* Locked AI and Matrix widths */
        grid-template-rows: 1fr 4px 200px 100px;   /* Locked Command and Footer heights */
        height: 100vh;
        width: 100vw;
        border: 2px solid black;
        box-sizing: border-box;
    }

    /* THE PARTITIONS (Verified to touch edges) */
    .v-red { grid-column: 2; grid-row: 1 / 4; background-color: red; cursor: col-resize; }
    .h-green-main { grid-row: 2; grid-column: 1; background-color: green; cursor: row-resize; }
    .h-green-ai { grid-row: 2; grid-column: 3; background-color: green; cursor: row-resize; }

    /* TEXT STYLING - 1:1 matching image_a30e62.png */
    .pane { padding: 15px; font-family: "Courier New", Courier, monospace; overflow: hidden; position: relative; }
    .txt-visual { color: #800000; font-size: 20px; font-weight: bold; line-height: 1.2; }
    .txt-ai { color: #008000; font-weight: bold; }
    .txt-user { color: #800080; font-weight: bold; }
    .txt-cmd { color: #ff0000; font-weight: bold; }

    /* BOX/BUTTON STYLING */
    .black-sq { width: 30px; height: 30px; background: black; border: 1px solid white; display: inline-block; margin: 3px; }
    .prompt-box { width: 100%; height: 120px; background: #fff; border: 1px solid black; }
    
    .matrix-wall { grid-column: 4; grid-row: 1 / 4; border-left: 1px solid black; background: #c0c0c0; text-align: center; padding-top: 20px; }
    .footer-matrix { grid-column: 3 / 5; grid-row: 4; border-top: 1px solid black; background: #808080; display: flex; flex-wrap: wrap; justify-content: center; align-items: center; }
    </style>
    """, unsafe_allow_html=True)

def main():
    # --- FROZEN AUTHENTICATION LOGIC ---
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
    cat = st.radio("Select Category:", ["Consumer Electronics", "Industrial Automation", "Military Systems"])
    if st.button("Access"):
        st.session_state['category'] = cat
        st.rerun()

def show_login_page():
    suffix = st.session_state['category'].replace(' ', '_')
    filename = f"auth_{suffix}.txt"
    st.subheader(f"Login: {st.session_state['category']}")
    u = st.text_input("ID")
    p = st.text_input("Passkey", type="password")
    if st.button("Login"):
        if check_credentials(u, p, filename):
            st.session_state['logged_in'] = True
            st.rerun()

def check_credentials(u, p, filename):
    if not os.path.exists(filename): return False
    with open(filename, "r") as f:
        return f"{u},{p}" in [line.strip() for line in f.readlines()]

# --- 1:1 WORKBENCH RECONSTRUCTION ---
def show_workbench():
    # Pre-generate button blocks to avoid Streamlit render errors
    rare_wall = "".join(['<div class="black-sq"></div><br>' for _ in range(10)])
    matrix_grid = "".join(['<div class="black-sq"></div>' for _ in range(12)])

    st.markdown(f"""
    <div class="blueprint-grid">
        <!-- TOP LEFT -->
        <div class="pane" style="grid-column: 1; grid-row: 1;">
            <div class="txt-visual">visual displays dynamic between coding and screen/CAD designs</div>
        </div>
        
        <!-- VERTICAL RED LINE -->
        <div class="v-red"></div>
        
        <!-- TOP RIGHT -->
        <div class="pane" style="grid-column: 3; grid-row: 1;">
            <div class="txt-ai">AI TEXT REPLYING WINDOW</div>
        </div>

        <!-- HORIZONTAL GREEN LINES -->
        <div class="h-green-main"></div>
        <div class="h-green-ai"></div>

        <!-- COMMAND PROMPT -->
        <div class="pane" style="grid-column: 1; grid-row: 3;">
            <div class="txt-cmd">command prompt for system programming for project</div>
        </div>

        <!-- USER PROMPTING -->
        <div class="pane" style="grid-column: 3; grid-row: 3;">
            <div class="txt-user">USER PROMPTING</div>
            <div class="prompt-box"></div>
        </div>

        <!-- RARELY USED WALL -->
        <div class="matrix-wall">
            <span style="font-size: 10px;">RARELY<br>USED</span><br><br>
            {rare_wall}
        </div>

        <!-- FOOTER: INDICATORS -->
        <div style="grid-column: 1; grid-row: 4; border-top: 1px solid black; display: flex;">
            <div style="width: 30%; border-right: 1px solid black; padding: 10px; color: green; font-weight: bold;">small indicators any</div>
            <div style="width: 70%; padding: 10px; color: blue; font-weight: bold;">buttons for controlling we will decide buttons as and when we</div>
        </div>

        <!-- FOOTER: SQUARE MATRIX -->
        <div class="footer-matrix">
            {matrix_grid}
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
