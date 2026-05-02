import streamlit as st
import os

# Rule 10 & 11: Frozen logic and Provider Independence
st.set_page_config(layout="wide", page_title="Workbench v1.0", initial_sidebar_state="collapsed")

# Hard-coded 1:1 Blueprint CSS
st.markdown("""
    <style>
    /* Remove all default spacing */
    .block-container { padding: 0 !important; max-height: 100vh; overflow: hidden; }
    header { visibility: hidden; }
    
    /* Main Layout Grid - Forced 1:1 Mapping to image_a30e62.png */
    .grid-wrapper {
        display: grid;
        grid-template-columns: 1fr 300px 180px; /* Workspace | AI Panel | Square Matrix */
        grid-template-rows: 1fr 150px 80px;     /* Content | Command | Footer */
        height: 100vh;
        width: 100vw;
        background-color: white;
        border: 2px solid black;
    }

    /* Cell Borders to match Blueprint colors */
    .cell { border: 1px solid black; position: relative; overflow: hidden; }
    .v-red { border-right: 3px solid red !important; }
    .h-green { border-bottom: 3px solid green !important; }
    
    /* Square Matrix Button Style */
    .matrix-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        padding: 5px;
        gap: 5px;
    }
    .sq-box { 
        width: 45px; height: 45px; 
        background-color: white; 
        border: 2px solid black; 
        display: inline-block;
    }
    
    /* Labels */
    .lbl { padding: 5px; font-weight: bold; font-family: 'Comic Sans MS'; }
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
        show_workbench()

# --- FROZEN AUTHENTICATION ---
def show_category_selection():
    st.title("System Domain")
    cat = st.radio("Domain:", ["Consumer Electronics", "Industrial Automation", "Military Systems"])
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

# --- 1:1 BLUEPRINT WORKBENCH ---
def show_workbench():
    # We use Streamlit columns but force them into a strict bordered container
    # Column Group A: Main & AI | Column Group B: Vertical Right Buttons
    main_cols = st.columns([0.88, 0.12])

    with main_cols[0]:
        # Top Row: Visuals and AI Replying
        t_left, t_right = st.columns([0.7, 0.3])
        with t_left:
            st.markdown("<div style='height:450px; border-bottom:3px solid green; border-right:3px solid red; padding:10px;'>"
                        "<h2 style='color:brown;'>visual displays dynamic between coding and screen/CAD designs</h2></div>", unsafe_allow_html=True)
            # Bottom Row: Command Prompt
            st.markdown("<div style='height:150px; padding:10px;'>"
                        "<p style='color:red;'>command prompt for system programming for project</p></div>", unsafe_allow_html=True)
        
        with t_right:
            st.markdown("<div style='height:300px; border-bottom:3px solid green; padding:10px;'>"
                        "<h4 style='color:green;'>AI TEXT REPLYING WINDOW</h4></div>", unsafe_allow_html=True)
            # Bottom Row: User Prompting
            st.markdown("<div style='height:300px; padding:10px;'>"
                        "<h4 style='color:purple;'>USER PROMPTING</h4></div>", unsafe_allow_html=True)

    with main_cols[1]:
        # Vertical Right Wall - "Rearlly selected or used buttons"
        st.markdown("<div style='border-left:1px solid black; height:600px; text-align:center;'>", unsafe_allow_html=True)
        for _ in range(12):
            st.button("⬛", key=f"wall_{_}")
        st.markdown("</div>", unsafe_allow_html=True)

    # FOOTER
    st.markdown("<div style='border-top:2px solid black;'></div>", unsafe_allow_html=True)
    f1, f2, f3 = st.columns([0.2, 0.6, 0.2])
    with f1:
        st.markdown("<div style='padding:20px; border-right:1px solid black; color:green;'>small indicators any</div>", unsafe_allow_html=True)
    with f2:
        st.markdown("<div style='padding:20px; color:blue;'>buttons for controlling we will decide buttons as and when we</div>", unsafe_allow_html=True)
    with f3:
        # The 3x3 Matrix in bottom right
        m_cols = st.columns(3)
        for i in range(9):
            m_cols[i%3].button("⬛", key=f"mat_{i}")

if __name__ == "__main__":
    main()
