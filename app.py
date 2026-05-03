import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai

# --- [1. PERSISTENCE] ---
if "gemini_key" not in st.session_state:
    st.session_state.gemini_key = ""

# --- [2. AI CONFIGURATION] ---
model = None
if st.session_state.gemini_key:
    try:
        genai.configure(api_key=st.session_state.gemini_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception:
        model = None

# --- [3. UI OVERRIDE] ---
st.set_page_config(layout="wide", page_title="CAD Designer Pro")

st.markdown("""
    <style>
        #MainMenu, footer, header {visibility: hidden;}
        .stApp { background-color: #000 !important; }
        .block-container { padding: 0rem !important; max-width: 100% !important; height: 100vh !important; }
    </style>
""", unsafe_allow_html=True)

# --- [4. 1:1 INTERFACE] ---
cad_app_html = """
<style>
    body { margin: 0; background: #000; color: white; font-family: monospace; overflow: hidden; }
    .master { display: flex; flex-direction: column; height: 100vh; border: 2px solid #333; }
    #ai-setup { 
        position: absolute; top: 15%; left: 15%; width: 70%; height: 60%; 
        background: #000; border: 2px solid #0f0; z-index: 100; display: none; 
        flex-direction: column; padding: 20px;
    }
    .pane { border: 1px solid #333; display: flex; flex-direction: column; }
    .footer { height: 60px; background: #000; border-top: 2px solid #333; display: flex; align-items: center; padding: 0 10px; }
    .btn-key { width: 120px; height: 50px; background: #e1e1e1; color: #000; cursor: pointer; font-weight: bold; display: flex; align-items: center; justify-content: center; }
    .chat-box { flex: 1; color: #0f0; padding: 10px; overflow-y: auto; }
    .input-box { height: 80px; background: transparent; border-top: 1px solid #333; color: #800080; width: 100%; outline: none; padding: 10px; }
</style>

<div class="master">
    <div id="ai-setup">
        <h2 style="color:#0f0">[ AI CONFIG ]</h2>
        <input type="password" id="key-in" style="width:100%; padding:10px; background:#000; border:1px solid #0f0; color:#0f0;">
        <button onclick="save()" style="margin-top:20px; padding:10px; background:#0f0; color:#000; border:none; cursor:pointer;">SAVE KEY</button>
        <button onclick="toggle(false)" style="margin-top:10px; background:none; color:#444; border:none; cursor:pointer;">CANCEL</button>
    </div>

    <div style="flex: 1; display: flex;">
        <div style="width: 70%;" class="pane">
            <div style="flex:4; display:flex; align-items:center; justify-content:center; color:#b22222; font-size:24px;">VISUAL MONITOR</div>
            <div style="flex:1; border-top:1px solid #333; padding:5px; color:#0f0; font-size:12px;">>_ SYSTEM INITIALIZED</div>
        </div>
        <div style="width: 30%;" class="pane">
            <div id="display" class="chat-box">READY...</div>
            <textarea id="prompt" class="input-box" placeholder="TYPE HERE..."></textarea>
        </div>
    </div>
    
    <div class="footer">
        <div class="btn-key" onclick="toggle(true)">AI-SET</div>
    </div>
</div>

<script>
    function toggle(s) { document.getElementById('ai-setup').style.display = s ? 'flex' : 'none'; }
    
    function save() {
        const k = document.getElementById('key-in').value;
        if(k) {
            window.parent.postMessage({type: 'streamlit:setComponentValue', value: {action: 'KEY', val: k}}, '*');
            toggle(false);
        }
    }

    const p = document.getElementById('prompt');
    p.addEventListener('keydown', (e) => {
        if(e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            const t = p.value.trim();
            if(t) {
                document.getElementById('display').innerHTML += `<br><span style="color:#800080">[USER]:</span> ${t}`;
                window.parent.postMessage({type: 'streamlit:setComponentValue', value: {action: 'ASK', val: t}}, '*');
                p.value = '';
            }
        }
    });

    window.addEventListener('message', (e) => {
        if(e.data.type === 'AI_REPLY') {
            document.getElementById('display').innerHTML += `<br><span style="color:#0f0">[GEMINI]:</span> ${e.data.text}`;
        }
    });
</script>
"""

# --- [5. THE BRIDGE] ---
# component_value stays as None until user interacts. This prevents the .get() crash.
component_value = components.html(cad_app_html, height=0)

if isinstance(component_value, dict):
    act = component_value.get("action")
    val = component_value.get("val")
    
    if act == "KEY":
        st.session_state.gemini_key = val
        st.rerun()
    
    elif act == "ASK" and model:
        try:
            resp = model.generate_content(val)
            # Escaping for JS transfer
            safe_text = resp.text.replace("'", "\\'").replace("\n", "<br>")
            components.html(f"<script>window.parent.postMessage({{type: 'AI_REPLY', text: '{safe_text}'}}, '*');</script>", height=0)
        except Exception as e:
            st.error(f"Gemini Error: {e}")

# Maintain Fullscreen
st.components.v1.html("""<script>window.parent.document.querySelector('iframe').style.height = '95vh';</script>""", height=0)
