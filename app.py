import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai

# --- 1. SESSION STATE FOR THE KEY ---
if "gemini_key" not in st.session_state:
    st.session_state.gemini_key = ""

# Configure model if key exists
if st.session_state.gemini_key:
    genai.configure(api_key=st.session_state.gemini_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None

# --- 2. PAGE CONFIG ---
st.set_page_config(layout="wide", page_title="CAD Designer Pro")

# --- 3. UI RESET (1:1) ---
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stApp { background-color: #000 !important; overflow: hidden !important; }
        .block-container { padding: 0rem !important; max-width: 100% !important; height: 100vh !important; overflow: hidden !important; }
    </style>
""", unsafe_allow_html=True)

# --- 4. YOUR GUI (1:1) ---
cad_app_html = """
<script src="https://cdnjs.cloudflare.com/ajax/libs/split.js/1.6.0/split.min.js"></script>
<style>
    html, body { margin: 0; padding: 0; height: 100%; width: 100%; overflow: hidden !important; background-color: #000; font-family: 'Segoe UI', Tahoma, sans-serif; color: white; }
    .master-container { display: flex; flex-direction: column; height: 100vh; width: 100vw; background: #000; border: 2px solid #d3d3d3; box-sizing: border-box; position: relative; }
    #ai-modular-setup { position: absolute; top: 10%; left: 15%; width: 70%; height: 75%; background: #000; border: 2px solid #00ff00; z-index: 9999; display: none; flex-direction: column; box-shadow: 0 0 50px rgba(0,255,0,0.3); }
    .ai-setup-header { background: #0a1a0a; border-bottom: 1px solid #00ff00; padding: 10px; display: flex; justify-content: space-between; color: #00ff00; font-family: monospace; font-weight: bold; }
    .ai-setup-body { display: flex; flex: 1; overflow: hidden; }
    .ai-setup-sidebar { width: 30%; border-right: 1px solid #00ff00; padding: 10px; background: #050505; overflow-y: auto; }
    .ai-setup-content { width: 70%; padding: 25px; color: #00ff00; font-family: monospace; display: flex; flex-direction: column; gap: 20px; }
    .ai-tool-item { padding: 12px; border: 1px solid #004400; margin-bottom: 8px; cursor: pointer; font-size: 12px; transition: 0.2s; }
    .ai-tool-item.active { background: #00ff00; color: #000; font-weight: bold; }
    .ai-select { background: #000; border: 1px solid #00ff00; color: #00ff00; padding: 10px; width: 100%; font-family: monospace; }
    .ai-input { background: #000; border: 1px solid #00ff00; color: #00ff00; padding: 10px; width: 100%; box-sizing: border-box; }
    .window-title-bar { background: #1a1a1a; color: #888; height: 30px; display: flex; align-items: center; justify-content: space-between; padding: 0 10px; font-size: 12px; border-bottom: 1px solid #333; }
    #dynamic-zone { display: flex; flex-direction: row; flex: 1; min-height: 0; width: 100%; }
    .fixed-right-strip { width: 65px; border-left: 1px solid #333; display: grid; grid-template-columns: 1fr 1fr; padding: 5px; background: #000; overflow-y: scroll; }
    .btn-cell { aspect-ratio: 1 / 1; width: 20px; height: 20px; background: #e1e1e1; color: #000; border-top: 2px solid #fff; border-left: 2px solid #fff; border-right: 2px solid #707070; border-bottom: 2px solid #707070; cursor: pointer; display: flex; align-items: center; justify-content: center; box-sizing: border-box; }
    .pane { background: #000 !important; border: 1px solid #333 !important; overflow: hidden; display: flex; align-items: center; justify-content: center; box-sizing: border-box; }
    .fixed-footer { height: 64px; display: flex; flex-direction: row; border-top: 2px solid #333; background: #000; padding: 0px 4px 2px 4px; }
    .dropup { position: relative; width: 100%; height: 20px; background: #e1e1e1; color: #000; border: 1px solid #707070; display: flex; align-items: center; justify-content: space-between; padding: 0 5px; cursor: pointer; font-size: 9px; box-sizing: border-box; }
    .dropup.tall { height: 62px; }
    .ai-text-area { width: 100%; height: 100%; padding: 10px; color: #008000; font-family: 'Consolas', monospace; font-size: 13px; overflow-y: auto; text-align: left; }
    .user-input-area { width: 100%; height: 100%; background: transparent; border: none; color: #800080; padding: 10px; font-family: 'Consolas', monospace; outline: none; resize: none; font-weight: bold; }
    .cmd-text { width: 100%; height: 100%; color: #0f0; font-family: monospace; font-size: 11px; padding: 5px; overflow-y: auto; white-space: pre-wrap; }
</style>

<div class="master-container">
    <div id="ai-modular-setup">
        <div class="ai-setup-header"><span>[ SYSTEM AI-SET : TOOL CONFIGURATION ]</span><span onclick="toggleAISet(false)" style="cursor:pointer;">[ X ]</span></div>
        <div class="ai-setup-body">
            <div class="ai-setup-sidebar">
                <div class="ai-tool-item active">LUVIA AI</div>
                <div class="ai-tool-item">FLUX.AI</div>
            </div>
            <div class="ai-setup-content">
                <div style="font-size: 20px; border-bottom: 2px solid #004400; padding-bottom: 5px;">TOOL: <span id="tool-name">Luvia AI</span></div>
                <div><label>API KEY / LOCAL PATH:</label>
                <input type="password" id="api-key-input" class="ai-input" placeholder="ENTER ACCESS KEY OR PATH..."></div>
                <div style="margin-top: auto; display: flex; gap: 10px;">
                    <button class="btn-cell" style="width: 120px; height: 35px; background:#00ff00;" onclick="saveApiKey()">SAVE TOOL</button>
                </div>
            </div>
        </div>
    </div>

    <div class="window-title-bar"><div>CAD DESIGNER PRO</div><div><span>−</span><span style="margin:0 10px;">❐</span><span>×</span></div></div>
    <div id="dynamic-zone">
        <div id="split-container" style="display:flex; flex:1; width:100%;">
            <div id="left-stack" style="display:flex; flex-direction:column; width:70%;">
                <div id="cad-pane" class="pane" style="color:#b22222; font-weight:bold;">Visual Monitor Active</div>
                <div id="cmd-pane" class="pane"><div id="terminal-out" class="cmd-text">>_ SYSTEM INITIALIZED</div></div>
            </div>
            <div id="right-stack" style="display:flex; flex-direction:column; width:30%;">
                <div id="ai-output" class="pane"><div id="ai-chat" class="ai-text-area">AI READY</div></div>
                <div id="ai-input" class="pane"><textarea id="user-prompt" class="user-input-area" placeholder="TYPE HERE..."></textarea></div>
            </div>
        </div>
        <div class="fixed-right-strip" id="side-strip"></div>
    </div>
    <div class="fixed-footer">
        <div class="selection-b-container" style="width:130px;"><div class="dropup tall" onclick="toggleAISet(true)"><span>AI-SET</span><span>▲</span></div></div>
    </div>
</div>

<script>
    function toggleAISet(show) { document.getElementById('ai-modular-setup').style.display = show ? 'flex' : 'none'; }
    
    function saveApiKey() {
        const key = document.getElementById('api-key-input').value;
        window.parent.postMessage({type: 'streamlit:setComponentValue', value: {action: 'SAVE_KEY', key: key}}, '*');
        toggleAISet(false);
    }

    const promptInput = document.getElementById('user-prompt');
    promptInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            const text = promptInput.value.trim();
            if(text !== "") {
                document.getElementById('ai-chat').innerHTML += "<br><span style='color:#800080'>[USER]:</span> " + text;
                window.parent.postMessage({type: 'streamlit:setComponentValue', value: {action: 'SEND_PROMPT', text: text}}, '*');
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

# --- 5. THE BRIDGE ---
bridge_data = components.html(cad_app_html, height=0)

if bridge_data:
    if bridge_data.get("action") == "SAVE_KEY":
        st.session_state.gemini_key = bridge_data.get("key")
        st.rerun()
    
    elif bridge_data.get("action") == "SEND_PROMPT":
        if model:
            response = model.generate_content(bridge_data.get("text"))
            ai_reply = response.text.replace("'", "\\'").replace("\n", "<br>")
            components.html(f"<script>window.parent.postMessage({{type: 'AI_REPLY', text: '{ai_reply}'}}, '*');</script>", height=0)
        else:
            st.error("SYSTEM OFFLINE: Use AI-SET to enter key.")

st.components.v1.html("""<script>window.parent.document.querySelector('iframe').style.height = '94vh';</script>""", height=0)
