import streamlit as st
import os

# Rule 10 & 11: Provider Independent and Frozen Logic
st.set_page_config(layout="wide", page_title="System Gateway", initial_sidebar_state="collapsed")

# Rule 6: Professional Black Engineering Aesthetic
st.markdown("""
    <style>
    /* Force absolute black and hide all web elements */
    .block-container { padding: 0 !important; background-color: #000000; height: 100vh; width: 100vw; display: flex; justify-content: center; align-items: center; }
    header, footer { visibility: hidden !important; }
    
    /* THE CENTRAL CONTROL HUB - Locked width, no spreading */
    .control-hub {
        width: 320px;
        padding: 40px;
        border: 1px solid #333;
        background-color: #0a0a0a;
        text-align: center;
        font-family: 'Courier New', Courier, monospace;
    }

    /* Professional Small Bars */
    .stTextInput input {
        background-color: #000 !important;
        color: #00ff00 !important;
        border: 1px solid #444 !important;
        border-radius: 0px !important;
        text-align: center !important;
        height: 30px !important;
        font-size: 14px !important;
    }

    /* Text & Label Alignment */
    h1, h2, h3, label, .stMarkdown, .stRadio { 
        color: #cccccc !important; 
        text-align: center !important; 
        font-size: 14px !important;
    }
    
    /* Clean Buttons */
    .stButton>button {
        width: 100% !important;
        border-radius: 0px !important;
        background-color: #222 !important;
        color: white !important;
        border: 1px solid #444 !important;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    # Forced Central Container
    st.markdown('<div class="control-hub">', unsafe_allow_html=True)

    # --- AUTHENTICATION STATE ---
    if 'category' not in st.session_state: st.session_state['category'] = None
    if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False

    if st.session_state['category'] is None:
        st.markdown("### SYSTEM DOMAIN")
        cat = st.radio("Select Operational Domain:", ["Consumer Electronics", "Industrial Automation", "Military Systems"], label_visibility="collapsed")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("INITIALIZE"):
            st.session_state['category'] = cat
            st.rerun()
            
    elif not st.session_state['logged_in']:
        suffix = st.session_state['category'].replace(' ', '_')
        filename = f"auth_{suffix}.txt"
        
        st.markdown(f"### ACCESS PORTAL")
        st.markdown(f"<p style='color: #666;'>{st.session_state['category']}</p>", unsafe_allow_html=True)
        
        u = st.text_input("USER ID", placeholder="ID", label_visibility="collapsed")
        p = st.text_input("PASSKEY", type="password", placeholder="PASS", label_visibility="collapsed")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("AUTHENTICATE"):
            if check_credentials(u, p, filename):
                st.session_state['logged_in'] = True
                st.rerun()
        
        if st.button("REGISTER NEW ID"):
            with open(filename, "a") as f: f.write(f"{u},{p}\\n")
            st.toast("Credentials Logged.")

    else:
        st.markdown("<h3 style='color: #00ff00;'>SYSTEM ONLINE</h3>", unsafe_allow_html=True)
        st.markdown(f"<p>{st.session_state['category']}</p>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

def check_credentials(u, p, filename):
    if not os.path.exists(filename): return False
    with open(filename, "r") as f:
        return f"{u},{p}" in [line.strip() for line in f.readlines()]

if __name__ == "__main__":
    main()
