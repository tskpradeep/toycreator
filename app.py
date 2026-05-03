import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai

# --- 1. SYSTEM INITIALIZATION ---
if "gemini_key" not in st.session_state:
    st.session_state.gemini_key = ""
if "gemini_version" not in st.session_state:
    st.session_state.gemini_version = "gemini-1.5-flash"

# Configure Model Backend
model = None
if st.session_state.gemini_key:
    try:
        genai.configure(api_key=st.session_state.gemini_key)
        model = genai.GenerativeModel(st.session_state.gemini_version)
    except:
        model = None

# --- 2. UI RESET ---
st.set_page_config(layout="wide", page_title="CAD Designer Pro")

st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stApp { background-color: #000 !important; overflow: hidden !important; }
        .block-container {
            padding: 0rem !important;
            max-width: 100% !important;
            height: 100vh !important;
            overflow: hidden !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. NATIVE UI WITH GEMINI INSERTION ---
cad_app_html = """
<script src="https://cdnjs.cloudflare.com/ajax/libs/split.js/1.6.0/split.min.js"></script>
<style>
    html, body { 
        margin: 0; padding: 0; height: 100%; width: 100%; 
        overflow: hidden !important; background-color: #000; 
        font-family: 'Segoe UI', Tahoma, sans-serif; color: white;
    }
    .master-container { 
        display: flex; flex-direction: column; 
        height: 100vh; width: 100vw; background: #000;
        border: 2px solid #d3d3d3; box-sizing: border-box;
        position: relative;
    }

    /* --- SYSTEM AI-SET MODULAR WINDOW --- */
    #ai-modular-setup {
        position: absolute; top: 10%; left: 15%; width: 70%; height: 75%;
        background: #000; border: 2px solid #00ff00; z-index: 9999;
        display: none; flex-direction: column; box-shadow: 0 0 50px rgba(0,255,0,0.3);
    }
    .ai-setup-header { background: #0a1a0a; border-bottom: 1px solid #00ff00; padding: 10px; display: flex; justify-content: space-between; color: #00ff00; font-family: monospace; font-weight: bold; }
    .ai-setup-body { display: flex; flex: 1; overflow: hidden; }
    .ai-setup-sidebar { width: 30%; border-right: 1px solid #00ff00; padding: 10px; background: #050505; overflow-y: auto; }
    .ai-setup-content { width: 70%; padding: 25px; color: #00ff00; font-family: monospace; display: flex; flex-direction: column; gap: 20px; }
    
    .ai-tool-item { padding: 12px; border: 1px solid #004400; margin-bottom: 8px; cursor: pointer; font-size: 12px; transition: 0.2s; }
    .ai-tool-item:hover { border-color: #00ff00; background: #0a2a0a; }
    .ai-tool-item.active { background: #00ff00; color: #000; font-weight: bold; }
    
    .ai-select { background: #000; border: 1px solid #00ff00; color: #00ff00; padding: 10px; width: 100%; outline: none; cursor: pointer; font-family: monospace; }
    .ai-input { background: #000; border: 1px solid #00ff00; color: #00ff00; padding: 10px; width: 100%; outline: none; box-sizing: border-box; }
    .tool-note { font-size: 11px; color: #008800; border-left: 2px solid #00ff00; padding-left: 10px; margin-top: 5px; }

    /* --- ORIGINAL GUI CSS --- */
    .window-title-bar { background: #1a1a1a; color: #888; height: 30px; flex-shrink: 0; display: flex; align-items: center; justify-content: space-between; padding: 0 10px; font-size: 12px; border-bottom: 1px solid #333; }
    #dynamic-zone { display: flex; flex-direction: row; flex: 1; min-height: 0; width: 100%; }
    .fixed-right-strip { width: 65px; border-left: 1px solid #333; display: grid; grid-template-columns: 1fr 1fr; grid-auto-rows: min-content; gap: 2px; padding: 5px; background: #000; overflow-y: scroll; }
    .btn-cell { aspect-ratio: 1 / 1; width: 20px; height: 20px; background: #e1e1e1; color: #000; border-top: 2px solid #fff; border-left: 2px solid #fff; border-right: 2px solid #707070; border-bottom: 2px solid #707070; cursor: pointer; display: flex; align-items: center; justify-content: center; box-sizing: border-box; flex-shrink: 0; }
    .pane { background: #000 !important; border: 1px solid #333 !important; overflow: hidden; display: flex; align-items: center; justify-content: center; box-sizing: border-box; }
    .gutter { background-color: #444 !important; }
    .fixed-footer { height: 64px; display: flex; flex-direction: row; border-top: 2px solid #333; background: #000; flex-shrink: 0; align-items: flex-end; padding: 0px 4px 2px 4px; }
    .selection-b-container { width: 130px; height: 62px; margin-left: 5px; }
    .dropup { position: relative; width: 100%; height: 20px; background: #e1e1e1; color: #000; border: 1px solid #707070; display: flex; align-items: center; justify-content: space-between; padding: 0 5px; cursor: pointer; font-size: 9px; box-sizing: border-box; }
    .dropup.tall { height: 62px; }
    .text-main { color: #b22222; font-size: 1.4vw; font-weight: bold; text-align: center; width:100%; height:100%; overflow:auto; display:flex; flex-direction:column; align-items:center; justify-content:center;}
    .ai-text-area { width: 100%; height: 100%; padding: 10px; color: #008000; font-family: 'Consolas', monospace; font-size: 13px; overflow-y: auto; text-align: left; }
    .user-input-area { width: 100%; height: 100%; background: transparent; border: none; color: #800080; padding: 10px; font-family: 'Consolas', monospace; outline: none; resize: none; font-weight: bold; }
    .cmd-text { width: 100%; height: 100%; color: #0f0; font-family: monospace; font-size: 11px; padding: 5px; overflow-y: auto; white-space: pre-wrap; }
</style>

<div class="master-container">
    <!-- MODULAR AI-SET WINDOW -->
    <div id="ai-modular-setup">
        <div class="ai-setup-header">
            <span>[ SYSTEM AI-SET : TOOL CONFIGURATION ]</span>
            <span onclick="toggleAISet(false)" style="cursor:pointer; color:#fff;">[ X ]</span>
        </div>
        <div class="ai-setup-body">
            <div class="ai-setup-sidebar" id="tool-list">
                <div class="ai-tool-item active" onclick="updateToolView(this, 'Google Gemini')">GOOGLE GEMINI</div>
                <div class="ai-tool-item" onclick="updateToolView(this, 'Luvia AI')">LUVIA AI</div>
                <div class="ai-tool-item" onclick="updateToolView(this, 'Flux.ai')">FLUX.AI</div>
                <div class="ai-tool-item" onclick="updateToolView(this, 'KiCad')">KICAD</div>
            </div>
            <div class="ai-setup-content">
                <div style="font-size: 20px; border-bottom: 2px solid #004400; padding-bottom: 5px; color:#fff;">TOOL: <span id="tool-name">Google Gemini</span></div>
                
                <div>
                    <label>CORE MODEL VERSION:</label>
                    <select class="ai-select" id="gemini-version-select">
                        <option value="gemini-1.5-flash">Gemini 1.5 Flash (Fast/Drafting)</option>
                        <option value="gemini-1.5-pro">Gemini 1.5 Pro (Precision/Logical)</option>
                    </select>
                </div>

                <div>
                    <label>API KEY:</label>
                    <input type="password" id="gemini-api-key" class="ai-input" placeholder="ENTER ACCESS KEY...">
                    <a href="https://aistudio.google.com/app/apikey" target="_blank" style="color:#00ff00; font-size:10px; display:block; margin-top:5px;">GET FREE API KEY ↗</a>
                </div>

                <div style="margin-top: auto; display: flex; gap: 10px;">
                    <button class="btn-cell" style="width: 120px; height: 35px; background:#00ff00;" onclick="saveGeminiConfig()">SAVE TOOL</button>
                    <button class="btn-cell" style="width: 120px; height: 35px; background:#444; color:#fff;" onclick="toggleAISet(false)">CANCEL</button>
                </div>
            </div>
        </div>
    </div>

    <!-- MAIN DASHBOARD -->
    <div class="window-title-bar"><div>CAD DESIGNER PRO</div></div>

    <div id="dynamic-zone">
        <div id="split-container" style="display:flex; flex:1; width:100%;">
            <div id="left-stack" style="display:flex; flex-direction:column; width:70%;">
                <div id="cad-pane" class="pane text-main">Visual Monitor Active</div>
                <div id="cmd-pane" class="pane"><div id="terminal-out" class="cmd-text">>_ SYSTEM READY</div></div>
            </div>
            <div id="right-stack" style="display:flex; flex-direction:column; width:30%;">
                <div id="ai-output" class="pane"><div id="ai-chat" class="ai-text-area">AI READY</div></div>
                <div id="ai-input" class="pane"><textarea id="user-prompt" class="user-input-area" placeholder="TYPE HERE..."></textarea></div>
            </div>
        </div>
        <div class="fixed-right-strip" id="side-strip"></div>
    </div>

    <div class="fixed-footer">
        <div class="selection-b-container">
            <div class="dropup tall" onclick="toggleAISet(true)"><span>AI-SET</span><span>▲</span></div>
        </div>
    </div>
</div>

<script>
    Split(['#left-stack', '#right-stack'], { sizes: [70, 30], gutterSize: 4 });
    Split(['#cad-pane', '#cmd-pane'], { direction: 'vertical', sizes: [80, 20], gutterSize: 4 });
    Split(['#ai-output', '#ai-input'], { direction: 'vertical', sizes: [50, 50], gutterSize: 4 });

    for(let i=0; i<100; i++) document.getElementById('side-strip').innerHTML += '<div class="btn-cell"></div>';

    function toggleAISet(show) { document.getElementById('ai-modular-setup').style.display = show ? 'flex' : 'none'; }

    function saveGeminiConfig() {
        const key = document.getElementById('gemini-api-key').value;
        const ver = document.getElementById('gemini-version-select').value;
        if(key) {
            window.parent.postMessage({type: 'streamlit:setComponentValue', value: {action: 'SAVE_KEY', key: key, ver: ver}}, '*');
            toggleAISet(false);
        }
    }

    const pInput = document.getElementById('user-prompt');
    pInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            const text = pInput.value.trim();
            if(text !== "") {
                document.getElementById('ai-chat').innerHTML += "<br><span style='color:#800080'>[USER]:</span> " + text;
                window.parent.postMessage({type: 'streamlit:setComponentValue', value: {action: 'SEND_PROMPT', text: text}}, '*');
                pInput.value = "";
            }
        }
    });

    window.addEventListener('message', function(event) {
        if (event.data.type === 'AI_REPLY') {
            document.getElementById('ai-chat').innerHTML += "<br><span style='color:#008000'>[GEMINI]:</span> " + event.data.text;
            document.getElementById('ai-chat').scrollTop = document.getElementById('ai-chat').scrollHeight;
        }
    });
</script>
"""

# --- 4. THE PYTHON BRIDGE ---
res = components.html(cad_app_html, height=0)

if isinstance(res, dict):
    if res.get("action") == "SAVE_KEY":
        st.session_state.gemini_key = res.get("key")
        st.session_state.gemini_version = res.get("ver")
        st.rerun()
    
    elif res.get("action") == "SEND_PROMPT" and model:
        try:
            response = model.generate_content(res.get("text"))
            clean_reply = response.text.replace("'", "\\'").replace("\n", "<br>")
            components.html(f"<script>window.parent.postMessage({{type: 'AI_REPLY', text: '{clean_reply}'}}, '*');</script>", height=0)
        except Exception as e:
            st.error(f"AI ERROR: {str(e)}")

# Force Sizing
st.components.v1.html("""<script>window.parent.document.querySelector('iframe').style.height = '94vh';</script>""", height=0)
