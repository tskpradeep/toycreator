import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai

# --- [SYSTEM CONFIG] ---
if "gemini_key" not in st.session_state:
    st.session_state.gemini_key = ""

if st.session_state.gemini_key:
    try:
        genai.configure(api_key=st.session_state.gemini_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except:
        model = None
else:
    model = None

# --- [UI INITIALIZATION] ---
st.set_page_config(layout="wide", page_title="CAD Designer Pro")

st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stApp { background-color: #000 !important; overflow: hidden !important; }
        .block-container { padding: 0rem !important; max-width: 100% !important; height: 100vh !important; }
    </style>
""", unsafe_allow_html=True)

# --- [GUI CODE] ---
cad_app_html = """
<script src="https://cdnjs.cloudflare.com/ajax/libs/split.js/1.6.0/split.min.js"></script>
<style>
    html, body { margin: 0; padding: 0; height: 100%; width: 100%; overflow: hidden; background-color: #000; font-family: 'Segoe UI', sans-serif; color: white; }
    .master-container { display: flex; flex-direction: column; height: 100vh; width: 100vw; border: 2px solid #d3d3d3; box-sizing: border-box; position: relative; }
    
    /* AI Setup Overlay */
    #ai-modular-setup { position: absolute; top: 10%; left: 15%; width: 70%; height: 75%; background: #000; border: 2px solid #00ff00; z-index: 9999; display: none; flex-direction: column; }
    .ai-setup-header { background: #0a1a0a; border-bottom: 1px solid #00ff00; padding: 10px; display: flex; justify-content: space-between; color: #00ff00; font-family: monospace; }
    .ai-setup-content { padding: 25px; color: #00ff00; font-family: monospace; display: flex; flex-direction: column; gap: 20px; }
    .ai-input { background: #000; border: 1px solid #00ff00; color: #00ff00; padding: 10px; width: 100%; box-sizing: border-box; }
    
    .window-title-bar { background: #1a1a1a; color: #888; height: 30px; display: flex; align-items: center; justify-content: space-between; padding: 0 10px; font-size: 12px; border-bottom: 1px solid #333; }
    #dynamic-zone { display: flex; flex: 1; min-height: 0; width: 100%; }
    .pane { background: #000; border: 1px solid #333; overflow: hidden; display: flex; box-sizing: border-box; }
    .gutter { background-color: #444 !important; }
    
    .fixed-footer { height: 64px; display: flex; border-top: 2px solid #333; background: #000; padding: 2px; align-items: center; }
    .dropup-btn { width: 130px; height: 60px; background: #e1e1e1; color: #000; border: 1px solid #707070; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: bold; }
    
    .ai-text-area { width: 100%; height: 100%; padding: 10px; color: #008000; font-family: monospace; overflow-y: auto; }
    .user-input-area { width: 100%; height: 100%; background: transparent; border: none; color: #800080; padding: 10px; font-family: monospace; outline: none; resize: none; font-weight: bold; }
    .cmd-text { width: 100%; height: 100%; color: #0f0; font-family: monospace; font-size: 11px; padding: 5px; }
</style>

<div class="master-container">
    <div id="ai-modular-setup">
        <div class="ai-setup-header"><span>[ SYSTEM AI-SET : CONFIG ]</span><span onclick="toggleAISet(false)" style="cursor:pointer;">[ X ]</span></div>
        <div class="ai-setup-content">
            <label>ENTER GEMINI API KEY:</label>
            <input type="password" id="api-key-input" class="ai-input">
            <button style="width: 120px; height: 35px; background:#00ff00; cursor:pointer;" onclick="saveKey()">SAVE KEY</button>
        </div>
    </div>

    <div class="window-title-bar"><div>CAD DESIGNER PRO</div></div>
    <div id="dynamic-zone">
        <div id="left-stack" style="width:70%; display:flex; flex-direction:column;">
            <div id="cad-pane" class="pane" style="flex:4; color:#b22222; justify-content:center; align-items:center;">VISUAL MONITOR</div>
            <div id="cmd-pane" class="pane" style="flex:1;"><div id="terminal-out" class="cmd-text">>_ SYSTEM READY</div></div>
        </div>
        <div id="right-stack" style="width:30%; display:flex; flex-direction:column;">
            <div id="ai-output" class="pane" style="flex:1;"><div id="ai-chat" class="ai-text-area">AI WAITING...</div></div>
            <div id="ai-input" class="pane" style="flex:1;"><textarea id="user-prompt" class="user-input-area" placeholder="TYPE HERE..."></textarea></div>
        </div>
    </div>
    <div class="fixed-footer">
        <div class="dropup-btn" onclick="toggleAISet(true)">AI-SET</div>
    </div>
</div>

<script>
    function toggleAISet(show) { document.getElementById('ai-modular-setup').style.display = show ? 'flex' : 'none'; }
    
    function saveKey() {
        const key = document.getElementById('api-key-input').value;
        if(key) {
            window.parent.postMessage({type: 'streamlit:setComponentValue', value: {action: 'SAVE_KEY', data: key}}, '*');
            toggleAISet(false);
        }
    }

    const promptInput = document.getElementById('user-prompt');
    promptInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            const text = promptInput.value.trim();
            if(text) {
                document.getElementById('ai-chat').innerHTML += "<br><span style='color:#800080'>[USER]:</span> " + text;
                window.parent.postMessage({type: 'streamlit:setComponentValue', value: {action: 'SEND_PROMPT', data: text}}, '*');
                promptInput.value = "";
            }
        }
    });

    window.addEventListener('message', function(event) {
        if (event.data.type === 'AI_REPLY') {
            document.getElementById('ai-chat').innerHTML += "<br><span style='color:#008000'>[GEMINI]:</span> " + event.data.text;
        }
    });
</script>
"""

# --- [BRIDGE LOGIC] ---
# component_value will be None until a postMessage is sent from JS
component_value = components.html(cad_app_html, height=0)

if component_value is not None:
    action = component_value.get("action")
    payload = component_value.get("data")
    
    if action == "SAVE_KEY":
        st.session_state.gemini_key = payload
        st.rerun()
    
    elif action == "SEND_PROMPT" and model:
        try:
            response = model.generate_content(payload)
            clean_reply = response.text.replace("'", "\\'").replace("\n", "<br>")
            components.html(f"<script>window.parent.postMessage({{type: 'AI_REPLY', text: '{clean_reply}'}}, '*');</script>", height=0)
        except Exception as e:
            st.error(f"Gemini Error: {str(e)}")

# Force iframe height
st.components.v1.html("""<script>window.parent.document.querySelector('iframe').style.height = '95vh';</script>""", height=0)
