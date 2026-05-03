import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai

# --- [1. SYSTEM STATE] ---
if "gemini_key" not in st.session_state:
    st.session_state.gemini_key = ""
if "gemini_version" not in st.session_state:
    st.session_state.gemini_version = "gemini-1.5-flash"

# Initialize AI
model = None
if st.session_state.gemini_key:
    try:
        genai.configure(api_key=st.session_state.gemini_key)
        model = genai.GenerativeModel(st.session_state.gemini_version)
    except Exception:
        model = None

# --- [2. LAYOUT OVERRIDE] ---
st.set_page_config(layout="wide", page_title="CAD Designer Pro")

st.markdown("""
    <style>
        #MainMenu, footer, header {visibility: hidden;}
        .stApp { background-color: #000 !important; overflow: hidden !important; }
        .block-container { padding: 0rem !important; max-width: 100% !important; height: 100vh !important; }
    </style>
""", unsafe_allow_html=True)

# --- [3. THE INTERFACE] ---
cad_app_html = """
<style>
    html, body { margin: 0; padding: 0; height: 100%; width: 100%; overflow: hidden; background-color: #000; font-family: 'Segoe UI', sans-serif; color: white; }
    .master-container { display: flex; flex-direction: column; height: 100vh; width: 100vw; border: 2px solid #d3d3d3; box-sizing: border-box; position: relative; }
    
    /* MODAL: AI SETTINGS */
    #ai-modular-setup { position: absolute; top: 10%; left: 15%; width: 70%; height: 75%; background: #000; border: 2px solid #00ff00; z-index: 9999; display: none; flex-direction: column; box-shadow: 0 0 50px rgba(0,255,0,0.3); }
    .ai-setup-header { background: #0a1a0a; border-bottom: 1px solid #00ff00; padding: 10px; display: flex; justify-content: space-between; color: #00ff00; font-family: monospace; font-weight: bold; }
    .ai-setup-body { display: flex; flex: 1; overflow: hidden; }
    .ai-setup-sidebar { width: 30%; border-right: 1px solid #00ff00; padding: 10px; background: #050505; }
    .ai-setup-content { width: 70%; padding: 25px; color: #00ff00; font-family: monospace; display: flex; flex-direction: column; gap: 15px; }
    .ai-tool-item { padding: 12px; border: 1px solid #004400; margin-bottom: 8px; font-size: 12px; background: #00ff00; color: #000; font-weight: bold; }
    
    .ai-select { background: #000; border: 1px solid #00ff00; color: #00ff00; padding: 10px; width: 100%; font-family: monospace; }
    .ai-input { background: #000; border: 1px solid #00ff00; color: #00ff00; padding: 10px; width: 100%; box-sizing: border-box; }
    
    /* PANES */
    .window-title-bar { background: #1a1a1a; color: #888; height: 30px; display: flex; align-items: center; padding: 0 10px; font-size: 12px; border-bottom: 1px solid #333; }
    #dynamic-zone { display: flex; flex: 1; min-height: 0; width: 100%; }
    .pane { background: #000; border: 1px solid #333; display: flex; box-sizing: border-box; overflow: hidden; }
    
    /* TEXT AREAS */
    .ai-text-area { width: 100%; height: 100%; padding: 10px; color: #008000; font-family: monospace; overflow-y: auto; }
    .user-input-area { width: 100%; height: 100%; background: transparent; border: none; color: #800080; padding: 10px; font-family: monospace; outline: none; resize: none; font-weight: bold; }

    /* FOOTER */
    .fixed-footer { height: 64px; display: flex; border-top: 2px solid #333; background: #000; padding: 2px; }
    .dropup { width: 130px; height: 60px; background: #e1e1e1; color: #000; border: 1px solid #707070; display: flex; align-items: center; justify-content: center; cursor: pointer; font-size: 11px; font-weight: bold; }
</style>

<div class="master-container">
    <!-- MODAL -->
    <div id="ai-modular-setup">
        <div class="ai-setup-header"><span>[ SYSTEM AI-SET : TOOL CONFIGURATION ]</span><span onclick="toggleModal(false)" style="cursor:pointer;">[ X ]</span></div>
        <div class="ai-setup-body">
            <div class="ai-setup-sidebar"><div class="ai-tool-item">GEMINI AI</div></div>
            <div class="ai-setup-content">
                <div style="font-size: 18px; border-bottom: 1px solid #004400;">TOOL: Gemini AI</div>
                
                <label>CORE MODEL VERSION:</label>
                <select id="model-ver" class="ai-select">
                    <option value="gemini-1.5-flash">Gemini 1.5 Flash (Fast)</option>
                    <option value="gemini-1.5-pro">Gemini 1.5 Pro (Heavy)</option>
                </select>

                <label>API KEY:</label>
                <input type="password" id="api-key" class="ai-input" placeholder="ENTER ACCESS KEY...">
                
                <div style="margin-top: auto; display: flex; gap: 10px;">
                    <button style="background:#00ff00; color:#000; border:none; padding:10px 25px; font-weight:bold; cursor:pointer;" onclick="saveConfig()">SAVE TOOL</button>
                    <button style="background:#222; color:#fff; border:none; padding:10px; cursor:pointer;" onclick="toggleModal(false)">CANCEL</button>
                </div>
            </div>
        </div>
    </div>

    <div class="window-title-bar">CAD DESIGNER PRO</div>
    <div id="dynamic-zone">
        <div style="width: 70%; display: flex; flex-direction: column;">
            <div class="pane" style="flex:4; color:#b22222; justify-content:center; align-items:center; font-weight:bold;">Visual Monitor Active</div>
            <div class="pane" style="flex:1; padding:10px; color:#0f0; font-family:monospace; font-size:11px;">>_ SYSTEM INITIALIZED</div>
        </div>
        <div style="width: 30%; display: flex; flex-direction: column; border-left: 1px solid #333;">
            <div class="pane" style="flex:1;"><div id="chat" class="ai-text-area">AI READY</div></div>
            <div class="pane" style="height:120px;"><textarea id="prompt" class="user-input-area" placeholder="TYPE HERE..."></textarea></div>
        </div>
    </div>
    <div class="fixed-footer">
        <div class="dropup" onclick="toggleModal(true)">AI-SET ▲</div>
    </div>
</div>

<script>
    function toggleModal(s) { document.getElementById('ai-modular-setup').style.display = s ? 'flex' : 'none'; }
    
    function saveConfig() {
        const key = document.getElementById('api-key').value;
        const ver = document.getElementById('model-ver').value;
        if(key) {
            window.parent.postMessage({type: 'streamlit:setComponentValue', value: {act: 'SAVE', key: key, ver: ver}}, '*');
            toggleModal(false);
        }
    }

    const pInput = document.getElementById('prompt');
    pInput.addEventListener('keydown', (e) => {
        if(e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            const text = pInput.value.trim();
            if(text) {
                document.getElementById('chat').innerHTML += `<br><span style="color:#800080">[USER]:</span> ${text}`;
                window.parent.postMessage({type: 'streamlit:setComponentValue', value: {act: 'SEND', val: text}}, '*');
                pInput.value = '';
            }
        }
    });

    window.addEventListener('message', (e) => {
        if(e.data.type === 'AI_REPLY') {
            document.getElementById('chat').innerHTML += `<br><span style="color:#008000">[GEMINI]:</span> ${e.data.text}`;
            document.getElementById('chat').scrollTop = document.getElementById('chat').scrollHeight;
        }
    });
</script>
"""

# --- [4. THE BRIDGE] ---
# component_value remains None until JS sends a message, preventing crashes.
component_value = components.html(cad_app_html, height=0)

if isinstance(component_value, dict):
    act = component_value.get("act")
    
    if act == "SAVE":
        st.session_state.gemini_key = component_value.get("key")
        st.session_state.gemini_version = component_value.get("ver")
        st.rerun()
    
    elif act == "SEND" and model:
        try:
            response = model.generate_content(component_value.get("val"))
            safe_text = response.text.replace("'", "\\'").replace("\n", "<br>")
            components.html(f"<script>window.parent.postMessage({{type: 'AI_REPLY', text: '{safe_text}'}}, '*');</script>", height=0)
        except Exception as e:
            st.error(f"AI Connection Error: {e}")

# Inject iFrame Height Fix
st.components.v1.html("""<script>window.parent.document.querySelector('iframe').style.height = '98vh';</script>""", height=0)
