import streamlit as st
import os

# Rule 10 & 1: Wide layout, Provider Independent
st.set_page_config(layout="wide", page_title="ToyCreator Workbench")

def main():
    # Initialize session states
    if 'category' not in st.session_state:
        st.session_state['category'] = None
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    # Logic Gate
    if st.session_state['category'] is None:
        show_category_selection()
    elif not st.session_state['logged_in']:
        show_login_page()
    else:
        show_workbench()

def show_category_selection():
    st.title("Technology Domain Selection")
    cat = st.radio("Select the infrastructure type to build:", 
                  ["Consumer Electronics", "Industrial Automation", "Military Systems"])
    if st.button("Initialize Gateway"):
        st.session_state['category'] = cat
        st.rerun()

def show_login_page():
    st.title(f"Access Portal: {st.session_state['category']}")
    if st.button("← Change Domain"):
        st.session_state['category'] = None
        st.rerun()
        
    tab1, tab2 = st.tabs(["Secure Login", "Register Account"])
    suffix = st.session_state['category'].replace(' ', '_')
    filename = f"auth_{suffix}.txt"
    
    with tab1:
        u = st.text_input("Username", key="login_u")
        p = st.text_input("Password", type="password", key="login_p")
        if st.button("Login"):
            if check_credentials(u, p, filename):
                st.session_state['logged_in'] = True
                st.rerun()
    with tab2:
        nu = st.text_input("Create Username", key="reg_u")
        np = st.text_input("Create Password", type="password", key="reg_p")
        if st.button("Create"):
            save_credentials(nu, np, filename)
            st.success("Account Ready")

def save_credentials(u, p, filename):
    with open(filename, "a") as f: f.write(f"{u},{p}\n")

def check_credentials(u, p, filename):
    if not os.path.exists(filename): return False
    with open(filename, "r") as f:
        for line in f:
            if f"{u},{p}" == line.strip(): return True
    return False

def show_workbench():
    # Layout based on image_b135de.png
    # Col 1: Workspace (Left) | Col 2: AI Interaction (Right) | Col 3: Wall (Edge)
    col_work, col_ai, col_wall = st.columns([0.65, 0.30, 0.05])

    with col_work:
        # Dynamic CAD/Code Vertical Split
        st.subheader("Visual Display / CAD")
        # Dynamic Height Slider (Rule 5: Practical solution for resizing)
        h_adj = st.slider("Adjust Split", 100, 800, 400, label_visibility="collapsed")
        st.container(height=h_adj, border=True).write("CAD / Design Viewport")
        
        st.subheader("Command Prompt")
        st.text_area("System Programming Window", height=250)

    with col_ai:
        st.subheader("AI Replying Window")
        st.container(height=400, border=True).write("AI Response...")
        
        st.subheader("User Prompting")
        st.text_area("Type here...", height=100, key="prompt_box")
        st.button("Send", use_container_width=True)

    with col_wall:
        # The Wall - Mobile optimized tooltips
        st.button("⚙️", help="Settings", key="w1")
        st.button("📁", help="Project Files", key="w2")
        st.button("💾", help="Save Architecture", key="w3")
        st.button("🛠️", help="Tools", key="w4")

    # Fixed Bottom Bar
    st.markdown("---")
    b_left, b_center, b_right = st.columns([2, 2, 1])
    with b_left:
        st.caption(f"Status: Connected | Domain: {st.session_state.category}")
    with b_right:
        if st.button("EXIT SYSTEM", type="primary", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

if __name__ == "__main__":
    main()
