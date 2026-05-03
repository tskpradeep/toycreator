import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai

# --- 1. PERSISTENT STATE ---
if "gemini_key" not in st.session_state:
    st.session_state.gemini_key = ""

# Configure Gemini
model = None
if st.session_state.gemini_key:
    try:
        genai.configure(api_key=st.session_state.gemini_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception:
        model = None

# --- 2. PAGE CONFIG & STYLING ---
st.set_page_config(layout="wide", page_title="CAD Designer Pro")

st.markdown("""
    <style>
        #MainMenu, footer, header {visibility: hidden;}
        .stApp { background-color: #000 !important; overflow: hidden; }
        .block-container { padding: 0rem !important; max-width: 100% !important; height: 100vh !important; }
        iframe { border: none !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. THE INTERFACE (HTML/CSS/JS) ---
cad_app_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body, html { margin: 0; padding: 0; height: 100%; width: 100%; background: #000; color: white; font-family: 'Segoe UI', Tahoma, sans-serif; overflow: hidden; }
        .master { display: flex; flex-direction: column; height: 100vh; width: 100vw; border: 2px solid #333; box-sizing: border-box; }
        
        /* Layout Grid */
        .main-row { display: flex; flex: 1; min-height: 0; }
        .left-col { width: 70%; display: flex; flex-direction: column; border-right: 1px solid #333; }
        .right-col { width: 30%; display: flex; flex-direction: column; }
        
        /* Panes */
        .pane { border: 1px solid #222; display: flex; position: relative; overflow: hidden; }
        .visual-monitor { flex: 4; justify-content: center; align-items: center; color: #b22222; font-weight: bold; font-size: 20px; text-transform: uppercase; letter-spacing: 2px; }
        .terminal { flex: 1; border-top: 1px solid #333; background: #050505; color: #0f0; font-family: monospace; font-size: 11px; padding: 8px; }
        .ai-output { flex: 1; border-bottom: 1px solid #333; background: #000; color: #008000; font-family: monospace; padding: 10px; overflow-y: auto; font-size: 13px; }
        .user-input { height: 120px; background: #000; position: relative; }
        .user-input textarea { width: 100%; height: 100%; background: transparent; border: none; color: #800080; padding: 10px; font-family: monospace; font-weight: bold; outline: none; resize: none; box-sizing: border-box; }
        
        /* Footer & AI-SET */
        .footer { height: 64px; border-top: 2px solid #333; display: flex; align-items: center; padding: 0 5px; background: #000; }
        .btn-aiset { width: 130px; height: 50px; background: #e1e1e1; color: #000; border: 1px solid #707070; font-weight: bold; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 11px; }
        
        /* Setup Modal */
        #setup-modal { position: absolute; top: 15%; left: 20%; width: 60%; background: #000; border: 2px solid #00ff00; z-index: 1000; display: none; flex-direction: column; padding: 20px; box-shadow: 0 0 30px rgba(0,255,0,0.2); }
        .modal-header { color: #00ff00; font-family: monospace; margin-bottom: 20px; border-bottom: 1px solid #004400; padding-bottom: 5px; }
        .modal-input { background: #000; border: 1px solid #00ff00; color: #00ff00; padding: 10px; width: 100%; margin-bottom: 15px; box-sizing: border-box; }
    </style>
</head>
<body>

<div class="master">
    <div id="setup-modal">
        <div class="modal-header">[ SYSTEM AI-SET : CONFIGURATION ]</div>
        <div style="color: #00ff00; font-size: 12px; margin-bottom: 5px;">ENTER GOOGLE GEMINI API KEY:</div>
        <input type="password" id="key-field" class="modal-input" placeholder="...">
        <div style="display: flex; gap: 10px;">
            <button onclick="saveKey()" style="background: #00ff00; color: #000; border: none; padding: 10px 20px; font-weight: bold; cursor: pointer;">SAVE TOOL</button>
            <button onclick="toggleModal(false)" style="background: transparent; color: #444; border: none; cursor: pointer;">CANCEL</button>
        </div>
    </div>

    <div class="main-row">
        <div class="left-col">
            <div class="pane visual-monitor">Visual Monitor Active</div>
            <div class="pane terminal" id="term">>_ SYSTEM INITIALIZED</div>
        </div>
        <div class="right-col">
            <div class="pane ai-output" id="chat-box">AI READY</div>
            <div class="user-input">
                <textarea id="cmd-in" placeholder="TYPE HERE..."></textarea>
            </div>
        </div>
    </div>

    <div class="footer">
        <div class="btn-aiset" onclick="toggleModal(true)">AI-SET ▲</div>
    </div>
</div>

<script>
    function toggleModal(show) { document.getElementById('setup-modal').style.display = show ? 'flex' : 'none'; }
    
    function saveKey() {
        const key = document.getElementById('key-field').value;
        if(key) {
            window.parent.postMessage({type: 'streamlit:setComponentValue', value: {act: 'SET_KEY', val: key}}, '*');
            toggleModal(false);
        }
    }

    const input = document.getElementById('cmd-in');
    input.addEventListener('keydown', (e) => {
        if(e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            const val = input.value.trim();
            if(val) {
                document.getElementById('chat-box').innerHTML += `<br><span style="color:#800080">[USER]:</span> ${val}`;
                window.parent.postMessage({type: 'streamlit:setComponentValue', value: {act: 'SEND_MSG', val: val}}, '*');
                input.value = '';
            }
        }
    });

    window.addEventListener('message', (e) => {
        if(e.data.type === 'AI_REPLY') {
            document.getElementById('chat-box').innerHTML += `<br><span style="color:#008000">[GEMINI]:</span> ${e.data.text}`;
            document.getElementById('chat-box').scrollTop = document.getElementById('chat-box').scrollHeight;
        }
    });
</script>
</body>
</html>
"""

# --- 4. THE BRIDGE ---
# Using a fixed height in the component call to prevent the "collapsed" look from your image
res = components.html(cad_app_html, height=900)

if isinstance(res, dict):
    action = res.get("act")
    value = res.get("val")
    
    if action == "SET_KEY":
        st.session_state.gemini_key = value
        st.rerun()
    
    elif action == "SEND_MSG" and model:
        try:
            response = model.generate_content(value)
            clean_reply = response.text.replace("'", "\\'").replace("\n", "<br>")
            components.html(f"<script>window.parent.postMessage({{type: 'AI_REPLY', text: '{clean_reply}'}}, '*');</script>", height=0)
        except Exception as e:
            st.error(f"AI Error: {e}")

# Inject final sizing fix
st.components.v1.html("""<script>window.parent.document.querySelector('iframe').style.height = '98vh';</script>""", height=0)
