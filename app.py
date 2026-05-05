import streamlit as st
import streamlit.components.v1 as components

# 1. Page Configuration
st.set_page_config(layout="wide", page_title="CAD Designer Pro")

# 2. UI Reset
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

# 3. Native UI Application with State Persistence
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
    .ai-setup-header { 
        background: #0a1a0a; border-bottom: 1px solid #00ff00; 
        padding: 10px; display: flex; justify-content: space-between; 
        color: #00ff00; font-family: monospace; font-weight: bold; 
        align-items: center;
    }
    .ai-header-controls { display: flex; gap: 10px; align-items: center; }
    .ai-setup-body { display: flex; flex: 1; overflow: hidden; }
    .ai-setup-sidebar { width: 30%; border-right: 1px solid #00ff00; padding: 10px; background: #050505; overflow-y: auto; }
    .ai-setup-content { width: 70%; padding: 25px; color: #00ff00; font-family: monospace; display: flex; flex-direction: column; gap: 20px; }
    
    .ai-tool-item { padding: 12px; border: 1px solid #004400; margin-bottom: 8px; cursor: pointer; font-size: 12px; transition: 0.2s; }
    .ai-tool-item:hover { border-color: #00ff00; background: #0a2a0a; }
    .ai-tool-item.active { background: #00ff00; color: #000; font-weight: bold; }
    
    .ai-select { background: #000; border: 1px solid #00ff00; color: #00ff00; padding: 10px; width: 100%; outline: none; cursor: pointer; font-family: monospace; appearance: none; }
    .ai-input { background: #000; border: 1px solid #00ff00; color: #00ff00; padding: 10px; width: 100%; outline: none; box-sizing: border-box; }
    .tool-note { font-size: 11px; color: #008800; border-left: 2px solid #00ff00; padding-left: 10px; margin-top: 5px; }

    .title-action-btn { 
        padding: 2px 12px; font-size: 10px; cursor: pointer; 
        border: 1px solid #00ff00; background: #000; color: #00ff00;
        font-family: monospace; text-transform: uppercase;
    }
    .title-action-btn:hover { background: #00ff00; color: #000; }
    .title-action-btn.close { border-color: #fff; color: #fff; }

    /* --- DASHBOARD STYLES --- */
    .window-title-bar { background: #1a1a1a; color: #888; height: 30px; flex-shrink: 0; display: flex; align-items: center; justify-content: space-between; padding: 0 10px; font-size: 12px; border-bottom: 1px solid #333; }
    #dynamic-zone { display: flex; flex-direction: row; flex: 1; min-height: 0; width: 100%; }
    .fixed-right-strip { width: 65px; border-left: 1px solid #333; display: grid; grid-template-columns: 1fr 1fr; grid-auto-rows: min-content; gap: 2px; padding: 5px; background: #000; overflow-y: scroll; }
    .btn-cell { aspect-ratio: 1 / 1; width: 20px; height: 20px; background: #e1e1e1; color: #000; border-top: 2px solid #fff; border-left: 2px solid #fff; border-right: 2px solid #707070; border-bottom: 2px solid #707070; cursor: pointer; display: flex; align-items: center; justify-content: center; box-sizing: border-box; flex-shrink: 0; }
    .pane { background: #000 !important; border: 1px solid #333 !important; overflow: hidden; display: flex; align-items: center; justify-content: center; box-sizing: border-box; }
    .gutter { background-color: #444 !important; }
    .fixed-footer { height: 64px; display: flex; flex-direction: row; border-top: 2px solid #333; background: #000; flex-shrink: 0; align-items: flex-end; padding: 0px 4px 2px 4px; }
    .footer-left-content { flex: 1; display: flex; height: 100%; align-items: center; padding-left: 10px;}
    .selection-a-stack { display: flex; flex-direction: column; gap: 1px; width: 130px; margin-left: 5px; }
    .footer-palette-grid { display: grid; grid-template-columns: repeat(6, 20px); grid-template-rows: repeat(3, 20px); gap: 1px; margin-left: 8px; }
    .dropup { position: relative; width: 100%; height: 20px; background: #e1e1e1; color: #000; border: 1px solid #707070; display: flex; align-items: center; justify-content: space-between; padding: 0 5px; cursor: pointer; font-size: 9px; box-sizing: border-box; }
    .dropup.tall { height: 62px; }
    .dropup-content { display: none; position: absolute; bottom: 100%; left: -1px; background-color: #f0f0f0; min-width: 140px; border: 1px solid #707070; z-index: 1000; }
    .dropup.active .dropup-content { display: block; }
    .dropup-content a { color: #000; padding: 6px; text-decoration: none; display: block; border-bottom: 1px solid #ccc; font-size: 10px; }
    .ai-text-area { width: 100%; height: 100%; padding: 10px; color: #008000; font-family: 'Consolas', monospace; font-size: 13px; overflow-y: auto; text-align: left; }
    .user-input-area { width: 100%; height: 100%; background: transparent; border: none; color: #800080; padding: 10px; font-family: 'Consolas', monospace; outline: none; resize: none; font-weight: bold; }
    .cmd-text { width: 100%; height: 100%; color: #0f0; font-family: monospace; font-size: 11px; padding: 5px; overflow-y: auto; white-space: pre-wrap; }
</style>

<div class="master-container">
    <div id="ai-modular-setup">
        <div class="ai-setup-header">
            <span>[ SYSTEM AI-SET : TOOL CONFIGURATION ]</span>
            <div class="ai-header-controls">
                <button class="title-action-btn" onclick="saveAISettings()">SAVE</button>
                <button class="title-action-btn close" onclick="toggleAISet(false)">[ X ]</button>
            </div>
        </div>
        <div class="ai-setup-body">
            <div class="ai-setup-sidebar" id="tool-list">
                <div class="ai-tool-item active" onclick="updateToolView(this, 'Google Gemini', 'Multi-modal Reasoning', 'Official Google Integration.')">GOOGLE GEMINI</div>
                <div class="ai-tool-item" onclick="updateToolView(this, 'Luvia AI', 'MPN Text / Sourcing only', 'Sourcing only.')">LUVIA AI</div>
            </div>
            <div class="ai-setup-content">
                <div style="font-size: 20px; border-bottom: 2px solid #004400; padding-bottom: 5px; color:#fff;">TOOL: <span id="tool-name">Google Gemini</span></div>
                <div id="version-container">
                    <label>AVAILABLE VERSIONS:</label>
                    <select class="ai-select" id="version-select">
                        <option value="gemini-3-flash">Gemini 3 Flash (PhD reasoning/Speed)</option>
                        <option value="gemini-2.5-pro">Gemini 2.5 Pro (Standard reasoning)</option>
                    </select>
                </div>
                <div>
                    <label>CORE FUNCTION:</label>
                    <input type="text" class="ai-input" id="function-display" value="Multi-modal Reasoning" readonly>
                </div>
                <div>
                    <label>API KEY / LOCAL PATH:</label>
                    <input type="password" class="ai-input" id="api-key-input" placeholder="ENTER ACCESS KEY OR PATH...">
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
                <div id="cad-pane" class="pane" style="color: #b22222; font-weight: bold;">
                    <div id="visual-monitor">READY FOR DIAGRAM COMMANDS</div>
                </div>
                <div id="cmd-pane" class="pane"><div id="terminal-out" class="cmd-text">>_ SYSTEM ONLINE</div></div>
            </div>
            <div id="right-stack" style="display:flex; flex-direction:column; width:30%;">
                <div id="ai-output" class="pane"><div id="ai-chat" class="ai-text-area">AI WAITING...</div></div>
                <div id="ai-input" class="pane"><textarea id="user-prompt" class="user-input-area" placeholder="TYPE HERE..."></textarea></div>
            </div>
        </div>
        <div class="fixed-right-strip" id="side-strip"></div>
    </div>

    <div class="fixed-footer">
        <div class="footer-left-content"><span style="color:#008000; font-size: 11px;">READY</span></div>
        <div id="foot-palette" class="footer-palette-grid"></div>
        <div class="selection-a-stack">
            <div class="dropup" onclick="toggleMenu(this)"><span>File</span><span>▲</span><div class="dropup-content"><a>New</a></div></div>
            <div class="dropup" onclick="toggleMenu(this)"><span>Tools</span><span>▲</span><div class="dropup-content"><a>BOM</a></div></div>
        </div>
        <div style="width: 130px; margin-left: 5px;">
            <div class="dropup tall" onclick="toggleAISet(true)"><span>AI-SET</span><span>▲</span></div>
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

    function updateToolView(el, name, func, note) {
        document.querySelectorAll('.ai-tool-item').forEach(i => i.classList.remove('active'));
        el.classList.add('active');
        document.getElementById('tool-name').innerText = name;
        document.getElementById('function-display').value = func;
    }

    /* THE SAVE LOGIC */
    function saveAISettings() {
        const key = document.getElementById('api-key-input').value;
        const version = document.getElementById('version-select').value;
        const tool = document.getElementById('tool-name').innerText;
        
        // This stores the data in the browser so the AI "knows" it
        localStorage.setItem('active_tool', tool);
        localStorage.setItem('api_key', key);
        localStorage.setItem('version', version);
        
        document.getElementById('terminal-out').innerHTML += "\\n> SETTINGS SAVED FOR: " + tool;
        toggleAISet(false);
    }

    function toggleMenu(el) {
        event.stopPropagation();
        document.querySelectorAll('.dropup').forEach(d => d.classList.remove('active'));
        el.classList.add('active');
    }
    window.onclick = function() { document.querySelectorAll('.dropup').forEach(d => d.classList.remove('active')); };
</script>
"""

components.html(cad_app_html, height=0)
st.components.v1.html(f"<script>window.parent.document.querySelector('iframe').style.height = '94vh';</script>", height=0)
