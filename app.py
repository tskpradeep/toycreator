import streamlit as st
import os

# Rule 10 & 11: Frozen Logic and Provider Independence
st.set_page_config(layout="wide", page_title="Workbench v1.0", initial_sidebar_state="collapsed")

# CSS to force the exact 1:1 Grid Layout from image_a30e62.png
st.markdown("""
    <style>
    .block-container { padding: 0 !important; max-height: 100vh; overflow: hidden; background-color: white; }
    header { visibility: hidden; }
    footer { visibility: hidden; }

    /* The Master Grid - Matches the blueprint exactly */
    .master-container {
        display: grid;
        grid-template-columns: 1fr 3px 350px 100px; /* Main | Red Line | AI | Matrix */
        grid-template-rows: 1fr 3px 180px 100px;    /* Visuals | Green Line | Command | Footer */
        height: 100vh;
        width: 100vw;
        border: 2px solid black;
    }

    /* Fixed Border Lines */
    .red-line { background-color: red; grid-row: 1 / 4; grid-column: 2; }
    .green-line-top { background-color: green; grid-column: 1; grid-row: 2; }
    .green-line-ai { background-color: green; grid-column: 3; grid-row: 2; }

    /* Content Area Styles */
    .cell { overflow: hidden; padding: 10px; font-family: 'Comic Sans MS', cursive; }
    .matrix-box { width: 30px; height: 30px; background: white; border: 2px solid black; margin: 2px; display: inline-block; }
    .btn-rare { background: black; width: 40px; height: 40px; border: 1px solid white; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

def main():
    # RESTORING FROZEN LOGIC - DO NOT TOUCH
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
    cat = st.radio("Domain:", ["Consumer Electronics", "Industrial Automation", "Military Systems"])
    if st.button("Initialize Gateway"):
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
        credentials = [line.strip() for line in f.readlines()]
        return f"{u},{p}" in credentials

# --- 1:1 WORKBENCH IMPLEMENTATION ---
def show_workbench():
    # Structure based on image_a30e62.png
    col_main, col_ai, col_rare = st.columns([0.65, 0.25, 0.1])

    with col_main:
        # VISUAL DISPLAYS
        st.markdown("<h2 style='color: brown; height: 450px;'>visual displays dynamic between coding and screen/CAD designs</h2>", unsafe_allow_html=True)
        # GREEN BORDER
        st.markdown("<div style='background-color: green; height: 4px; width: 100%;'></div>", unsafe_allow_html=True)
        # COMMAND PROMPT
        st.markdown("<p style='color: red; height: 150px; font-weight: bold;'>command prompt for system programming for project</p>", unsafe_allow_html=True)
        # FOOTER (LEFT)
        f_left, f_mid = st.columns([0.3, 0.7])
        f_left.markdown("<div style='border: 1px solid black; color: green; padding: 10px;'>small indicators any</div>", unsafe_allow_html=True)
        f_mid.markdown("<div style='border: 1px solid black; color: blue; padding: 10px;'>buttons for controlling we will decide buttons as and when we</div>", unsafe_allow_html=True)

    with col_ai:
        # RED LINE SIMULATION (Vertical divider)
        st.markdown("<div style='border-left: 3px solid red; height: 100vh; position: absolute; left: -10px;'></div>", unsafe_allow_html=True)
        # AI REPLYING
        st.markdown("<h4 style='color: green; height: 300px;'>AI TEXT REPLYING WINDOW</h4>", unsafe_allow_html=True)
        # GREEN BORDER
        st.markdown("<div style='background-color: green; height: 4px; width: 100%;'></div>", unsafe_allow_html=True)
        # USER PROMPTING
        st.text_area("USER PROMPTING", height=200, label_visibility="collapsed")
        # BOTTOM MATRIX (3x3)
        m1, m2, m3 = st.columns(3)
        for i in range(9):
            [m1, m2, m3][i%3].button("⬛", key=f"mat_{i}")

    with col_rare:
        # RIGHT WALL BUTTONS
        for i in range(12):
            st.button("⬛", key=f"rare_{i}")

if __name__ == "__main__":
    main()
