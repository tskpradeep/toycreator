import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai

# --- 1. THE BRAIN (GEMINI CONFIG) ---
# Insert your key from https://aistudio.google.com/app/apikey here
API_KEY = "AIzaSyDKkohD9a0D0AF1yMr5QDzCzDUEUjebfSs"

if API_KEY != "AIzaSyDKkohD9a0D0AF1yMr5QDzCzDUEUjebfSs":
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None

# --- 2. PAGE CONFIG ---
st.set_page_config(layout="wide", page_title="CAD Designer Pro")

# --- 3. UI RESET (RETAINED 1:1) ---
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

# --- 4. YOUR NATIVE UI (RETAINED 1:1) ---
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
    .window-title-bar { background: #1a1a1a; color: #888; height: 30px; flex-shrink: 0; display: flex; align-items: center; justify-content: space-between; padding: 0 10px; font-size: 12px; border-bottom: 1px solid #333; }
    #dynamic-zone { display: flex; flex-direction: row; flex: 1; min-height: 0; width: 100%; }
    .fixed-right-strip { width: 65px; border-left: 1px solid #333; display: grid; grid-template-columns: 1fr 1fr; grid-auto-rows: min-content; gap: 2px; padding: 5px; background: #000; overflow-y: scroll; }
    .btn-cell { aspect-ratio: 1 / 1; width: 20px; height: 20px; background: #e1e1e1; color: #000; border-top: 2px solid #fff; border-left: 2px solid #fff; border-right: 2px solid #707070; border-bottom: 2px solid #707070; cursor: pointer; display: flex; align-items: center; justify-content: center; box-sizing: border-box; flex-shrink: 0; }
    .pane { background: #000 !important; border: 1px solid #333 !important; overflow: hidden; display: flex; align-items: center; justify-content: center; box-sizing: border-box; }
    .gutter { background-color: #444 !important; }
    .fixed-footer { height: 64px; display: flex; flex-direction: row; border-top: 2px solid #333; background: #000; flex-shrink: 0; align-items: flex-end; padding: 0px 4px 2px 4px; }
    .footer-left-content { flex: 1; display: flex; height: 100%; align-items: center; padding-left: 10px;}
    .selection-b-container { width: 130px; height: 62px; margin-left: 5px; }
    .selection-a-stack { display: flex; flex-direction: column; gap: 1px; width: 130px; margin-left: 5px; }
    .footer-palette-grid { display: grid; grid-template-columns: repeat(6, 20px); grid-template-rows: repeat(3, 20px); gap: 1px; margin-left: 8px; }
    .dropup { position: relative; width: 100%; height: 20px; background: #e1e1e1; color: #000; border: 1px solid #707070; display: flex; align-items: center; justify-content: space-between; padding: 0 5px; cursor: pointer; font-size: 9px; box-sizing: border-box; }
    .dropup.tall { height: 62px; }
    .dropup-content { display: none; position: absolute; bottom: 100%; left: -1px; background-color: #f0f0f0; min-width: 140px; border: 1px solid #707070; z-index: 1000; }
    .dropup.active .dropup-content { display: block; }
    .dropup-content a { color: #000; padding: 6px; text-decoration: none; display: block; border-bottom: 1px solid #ccc; font-size: 10px; }
    .text-main { color: #b22222; font-size: 1.4vw; font-weight: bold; text-align: center; width:100%; height:100%; overflow:auto; display:flex; flex-direction:column; align-items:center; justify-content:center;}
    .ai-text-area { width: 100%; height: 100%; padding: 10px; color: #008000; font-family: 'Consolas', monospace; font-size: 13px; overflow-y: auto; text-align: left; }
    .user-input-area { width: 100%; height: 100%; background: transparent; border: none; color: #800080; padding: 10px; font-family: 'Consolas', monospace; outline: none; resize: none; font-weight: bold; }
    .cmd-text { width: 100%; height: 100%; color: #0f0; font-family: monospace; font-size: 11px; padding: 5px; overflow-y: auto; white-space: pre-wrap; }
</style>

<div class="master-container">
    <div id="ai-modular-setup">
        <div class="ai-setup-header">
            <span>[ SYSTEM AI-SET : TOOL CONFIGURATION ]</span>
            <span onclick="toggleAISet(false)" style="cursor:pointer; color:#fff;">[ X ]</span>
        </div>
        <div class="ai-setup-body">
            <div class="ai-setup-sidebar" id="tool-list">
                <div class="ai-tool-item active" onclick="updateToolView(this, 'Luvia AI', 'Selection', 'MPN Text', 'Sourcing only.')">LUVIA AI</div>
                <div class="ai-tool-item" onclick="updateToolView(this, 'Flux.ai', 'Schematic', '.json / .net', 'Non-proprietary concept.')">FLUX.AI</div>
                <div class="ai-tool-item" onclick="updateToolView(this, 'KiCad', 'Analysis', '.kicad_sch', 'Local & Private.')">KICAD</div>
                <div class="ai-tool-item" onclick="updateToolView(this, 'Quilter', 'Layout', 'ODB++', 'Best for high-end CAM.')">QUILTER</div>
                <div class="ai-tool-item" onclick="updateToolView(this, 'nTop / Fusion', 'Enclosure', 'STEP / STL', 'Physics-verified.')">NTOP / FUSION</div>
            </div>
            <div class="ai-setup-content">
                <div style="font-size: 20px; border-bottom: 2px solid #004400; padding-bottom: 5px; color:#fff;">TOOL: <span id="tool-name">Luvia AI</span></div>
                <div>
                    <label>CORE FUNCTION (OUTPUT):</label>
                    <select class="ai-select" id="function-select">
                        <option value="MPN Text">MPN Text / Sourcing only</option>
                        <option value="json">.json / .net</option>
                        <option value="kicad">.kicad_sch</option>
                        <option value="odb">ODB++</option>
                        <option value="step">STEP / STL</option>
                    </select>
                    <div class="tool-note" id="tool-desc">Sourcing only.</div>
                </div>
                <div>
                    <label>DEPLOYMENT MODE:</label>
                    <select class="ai-select">
                        <option>Local / Dropbox (Privacy Mode)</option>
                        <option>Virtual Machine (Cloud Server)</option>
                    </select>
                </div>
                <div>
                    <label id="key-label">API KEY / LOCAL PATH:</label>
                    <input type="password" class="ai-input" placeholder="ENTER ACCESS KEY OR PATH...">
                    <a href="https://aistudio.google.com/app/apikey" target="_blank" style="color:#00ff00; font-size:10px; display:block; margin-top:5px;">GET FREE API KEY (IF CLOUD) ↗</a>
                </div>
                <div style="margin-top: auto; display: flex; gap: 10px;">
                    <button class="btn-cell" style="width: 120px; height: 35px; background:#00ff00;" onclick="toggleAISet(false)">SAVE TOOL</button>
                    <button class="btn-cell" style="width: 120px; height: 35px; background:#444; color:#fff;" onclick="toggleAISet(false)">CANCEL</button>
                </div>
            </div>
        </div>
    </div>

    <div class="window-title-bar">
        <div>CAD DESIGNER PRO</div>
        <div><span>−</span><span style="margin:0 10px;">❐</span><span>×</span></div>
    </div>

    <div id="dynamic-zone">
        <div id="split-container" style="display:flex; flex:1; width:100%;">
            <div id="left-stack" style="display:flex; flex-direction:column; width:70%;">
                <div id="cad-pane" class="pane text-main">
                    <div id="visual-monitor">visual displays dynamic between coding and screen/CAD designs</div>
                </div>
                <div id="cmd-pane" class="pane" style="justify-content: flex-start; align-items: flex-start;">
                    <div id="terminal-out" class="cmd-text">>_ SYSTEM INITIALIZED</div>
                </div>
            </div>
            <div id="right-stack" style="display:flex; flex-direction:column; width:30%;">
                <div id="ai-output" class="pane">
                    <div id="ai-chat" class="ai-text-area">AI TEXT REPLYING WINDOW</div>
                </div>
                <div id="ai-input" class="pane">
                    <textarea id="user-prompt" class="user-input-area" placeholder="TYPE HERE..."></textarea>
                </div>
            </div>
        </div>
        <div class="fixed-right-strip" id="side-strip"></div>
    </div>

    <div class="fixed-footer">
        <div class="footer-left-content">
            <span style="color:#008000; font-size: 11px; margin-right: 20px;">READY</span>
            <span style="color:#0000ff; font-size: 11px;">SYSTEM STATUS: ONLINE</span>
        </div>
        <div id="foot-palette" class="footer-palette-grid"></div>
        <div class="selection-a-stack">
            <div class="dropup" onclick="toggleMenu(this)"><span>File</span><span>▲</span><div class="dropup-content"><a>New Project</a><a>Open</a></div></div>
            <div class="dropup" onclick="toggleMenu(this)"><span>Tools</span><span>▲</span><div class="dropup-content"><a>BOM Gen</a><a>Netlist</a></div></div>
            <div class="dropup" onclick="toggleMenu(this)"><span>View</span><span>▲</span><div class="dropup-content"><a>2D View</a><a>3D Render</a></div></div>
        </div>
        <div class="selection-b-container">
            <div class="dropup tall" onclick="toggleAISet(true)"><span>AI-SET</span><span>▲</span><div class="dropup-content"><a>Tool Config</a><a>AI Dispatcher</a></div></div>
        </div>
    </div>
</div>

<script>
    Split(['#left-stack', '#right-stack'], { sizes: [70, 30], gutterSize: 4 });
    Split(['#cad-pane', '#cmd-pane'], { direction: 'vertical', sizes: [80, 20], gutterSize: 4 });
    Split(['#ai-output', '#ai-input'], { direction: 'vertical', sizes: [50, 50], gutterSize: 4 });

    for(let i=0; i<100; i++) document.getElementById('side-strip').innerHTML += '<div class="btn-cell"></div>';
    for(let i=0; i<18; i++) document.getElementById('foot-palette').innerHTML += '<div class="btn-cell"></div>';

    function toggleAISet(show) { document.getElementById('ai-modular-setup').style.display = show ? 'flex' : 'none'; }

    function updateToolView(el, name, cat, func, note) {
        document.querySelectorAll('.ai-tool-item').forEach(i => i.classList.remove('active'));
        el.classList.add('active');
        document.getElementById('tool-name').innerText = name;
        document.getElementById('function-select').value = func;
        document.getElementById('tool-desc').innerText = note;
    }

    function toggleMenu(el) {
        event.stopPropagation();
        const isActive = el.classList.contains('active');
        document.querySelectorAll('.dropup').forEach(d => d.classList.remove('active'));
        if(!isActive) el.classList.add('active');
    }

    window.onclick = function() { document.querySelectorAll('.dropup').forEach(d => d.classList.remove('active')); };

    const promptInput = document.getElementById('user-prompt');
    const chatWindow = document.getElementById('ai-chat');
    const terminal = document.getElementById('terminal-out');

    promptInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            const text = promptInput.value.trim();
            if(text !== "") {
                chatWindow.innerHTML += "<br><br><span style='color:#800080'>[USER]:</span> " + text;
                terminal.innerHTML += "\\n> PROCESSING CMD: " + text.toUpperCase();
                
                // INVISIBLE BRIDGE: Sends text to Streamlit backend
                window.parent.postMessage({type: 'streamlit:setComponentValue', value: text}, '*');
                promptInput.value = "";
            }
        }
    });

    // INVISIBLE BRIDGE: Receives text from Streamlit backend
    window.addEventListener('message', function(event) {
        if (event.data.type === 'AI_REPLY') {
            chatWindow.innerHTML += "<br><br><span style='color:#008000'>[GEMINI]:</span> " + event.data.text;
            terminal.innerHTML += "\\n> AI RESPONSE COMPLETED";
            chatWindow.scrollTop = chatWindow.scrollHeight;
        }
    });
</script>
"""

# --- 5. THE BRIDGE (BACKEND PROCESSING) ---
# Captures user_prompt from JS
user_prompt = components.html(cad_app_html, height=0)

# Resizes the iframe to fill the screen
st.components.v1.html(
    f"""<script>window.parent.document.querySelector('iframe').style.height = '94vh';</script>""",
    height=0
)

# If the JS sent a message, call Gemini and send it back
if user_prompt:
    if model:
        response = model.generate_content(user_prompt)
        ai_reply = response.text.replace("'", "\\'").replace("\\n", "<br>")
        components.html(f"""
            <script>
            window.parent.postMessage({{type: 'AI_REPLY', text: '{ai_reply}'}}, '*');
            </script>
        """, height=0)
    else:
        st.error("MISSING API KEY: Open 'AI-SET' to configure connection.")
