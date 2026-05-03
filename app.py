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

# 3. Native UI Application
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
        border: 2px solid #222; box-sizing: border-box;
        position: relative;
    }

    .window-title-bar {
        background: #111; color: #666; height: 30px;
        flex-shrink: 0; display: flex; align-items: center; 
        justify-content: space-between; padding: 0 10px; font-size: 12px;
        border-bottom: 1px solid #333;
    }

    #dynamic-zone { display: flex; flex-direction: row; flex: 1; min-height: 0; width: 100%; }

    .fixed-right-strip { 
        width: 65px; border-left: 1px solid #333; 
        display: grid; grid-template-columns: 1fr 1fr;
        grid-auto-rows: min-content; gap: 2px;
        padding: 5px; background: #000; 
        overflow-y: scroll; 
    }

    .btn-cell {
        aspect-ratio: 1 / 1; width: 20px; height: 20px;
        background: #e1e1e1; color: #000;
        border-top: 2px solid #fff; border-left: 2px solid #fff;
        border-right: 2px solid #707070; border-bottom: 2px solid #707070;
        cursor: pointer; display: flex; align-items: center; justify-content: center;
        box-sizing: border-box; flex-shrink: 0;
    }

    .pane { background: #000 !important; border: 1px solid #222 !important; overflow: hidden; display: flex; align-items: center; justify-content: center; box-sizing: border-box; }
    
    /* THE MAGMA MODAL - AMBER GLOW + MASTER-DETAIL ARCHITECTURE */
    #ai-modal {
        position: absolute; top: 10%; left: 10%; width: 80%; height: 75%;
        background: #000; border: 2px solid #ffaa00; z-index: 5000;
        display: none; flex-direction: column; padding: 0;
        box-shadow: 0 0 40px rgba(255, 170, 0, 0.3);
    }
    .modal-header { background: #1a1000; border-bottom: 1px solid #ffaa00; padding: 10px; display: flex; justify-content: space-between; font-size: 12px; color: #ffaa00; font-family: monospace; font-weight: bold;}
    .modal-content { display: flex; flex: 1; overflow: hidden; background: #000; }
    .modal-left { width: 30%; border-right: 1px solid #ffaa00; display: flex; flex-direction: column; padding: 10px; gap: 10px; background: #050300; }
    .modal-right { width: 70%; padding: 20px; display: flex; flex-direction: column; gap: 20px; background: #000; }
    
    .ai-list-item { background: #1a1000; border: 1px solid #ffaa00; color: #ffaa00; padding: 10px; cursor: pointer; font-family: monospace; font-size: 11px; }
    .ai-list-item:hover { background: #332200; }
    .add-ai-btn { background: #ffaa00; color: #000; border: none; padding: 10px; font-weight: bold; cursor: pointer; margin-top: auto; font-family: monospace; }

    .input-field { background: #000; border: 1px solid #ffaa00; color: #ffaa00; padding: 8px; width: 100%; box-sizing: border-box; font-family: monospace; outline: none; }
    .label-text { font-size: 10px; color: #ffaa00; text-transform: uppercase; margin-bottom: 5px; display: block; font-family: monospace; opacity: 0.8; }

    .fixed-footer { 
        height: 64px; display: flex; flex-direction: row; 
        border-top: 2px solid #333; background: #000; flex-shrink: 0;
        align-items: flex-end; 
        padding: 0px 4px 2px 4px;
    }

    .footer-left-content { flex: 1; display: flex; height: 100%; align-items: center; padding-left: 10px;}
    .selection-b-container { width: 130px; height: 62px; margin-left: 5px; }
    .selection-a-stack { display: flex; flex-direction: column; gap: 1px; width: 130px; margin-left: 5px; }
    .footer-palette-grid { display: grid; grid-template-columns: repeat(6, 20px); grid-template-rows: repeat(3, 20px); gap: 1px; margin-left: 8px; }

    .dropup { 
        position: relative; width: 100%; height: 20px; 
        background: #e1e1e1; color: #000; border: 1px solid #707070; 
        display: flex; align-items: center; justify-content: space-between;
        padding: 0 5px; cursor: pointer; font-size: 9px; box-sizing: border-box;
    }
    .dropup.tall { height: 62px; background: #ffaa00; color: #000; border: 1px solid #fff; font-weight: bold; font-size: 11px; }
    .dropup-content { display: none; position: absolute; bottom: 100%; left: -1px; background-color: #f0f0f0; min-width: 140px; border: 1px solid #707070; z-index: 1000; }
    .dropup.active .dropup-content { display: block; }
    .dropup-content a { color: #000; padding: 6px; text-decoration: none; display: block; border-bottom: 1px solid #ccc; font-size: 10px; }

    .text-main { color: #ffaa00; font-size: 1.4vw; font-weight: bold; font-family: monospace; text-align: center; width:100%; height:100%; overflow:auto; display:flex; flex-direction:column; align-items:center; justify-content:center;}
    .ai-text-area { width: 100%; height: 100%; padding: 10px; color: #ffaa00; font-family: monospace; font-size: 13px; overflow-y: auto; text-align: left; }
    .user-input-area { width: 100%; height: 100%; background: transparent; border: none; color: #fff; padding: 10px; font-family: monospace; outline: none; resize: none; font-weight: bold; }
    .cmd-text { width: 100%; height: 100%; color: #ffaa00; font-family: monospace; font-size: 11px; padding: 5px; overflow-y: auto; white-space: pre-wrap; opacity: 0.9; }
</style>

<div class="master-container">
    <div id="ai-modal">
        <div class="modal-header">
            <span>[ AI DISPATCH COMMANDER ]</span>
            <span style="cursor:pointer;" onclick="closeModal()">[ EXIT ]</span>
        </div>
        <div class="modal-content">
            <div class="modal-left">
                <div class="ai-list-item" onclick="loadAI('UNIT 01: GEMINI 1.5')">UNIT 01: GEMINI 1.5 (ARCHITECT)</div>
                <div class="ai-list-item" onclick="loadAI('UNIT 02: GROQ')">UNIT 02: GROQ (SYSTEMS)</div>
                <button class="add-ai-btn">[ + INITIALIZE NEW MODULE ]</button>
            </div>
            <div class="modal-right" id="config-panel">
                <div style="color:#442200; font-family:monospace; text-align:center; margin-top:20%;">SELECT MODULE TO ACCESS CORE SETTINGS...</div>
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
                    <div id="visual-monitor">SYSTEM READY</div>
                </div>
                <div id="cmd-pane" class="pane" style="justify-content: flex-start; align-items: flex-start;">
                    <div id="terminal-out" class="cmd-text">>_ BOOT SEQUENCE COMPLETE</div>
                </div>
            </div>
            <div id="right-stack" style="display:flex; flex-direction:column; width:30%;">
                <div id="ai-output" class="pane">
                    <div id="ai-chat" class="ai-text-area">AWAITING TECHNICAL PROMPTS...</div>
                </div>
                <div id="ai-input" class="pane">
                    <textarea id="user-prompt" class="user-input-area" placeholder="TYPE COMMAND..."></textarea>
                </div>
            </div>
        </div>
        <div class="fixed-right-strip" id="side-strip"></div>
    </div>

    <div class="fixed-footer">
        <div class="footer-left-content">
            <span style="color:#ffaa00; font-size: 11px; margin-right: 20px; font-weight:bold;">MAGMA-LINK: ACTIVE</span>
            <span style="color:#666; font-size: 11px;">ENCRYPTION: AES-256</span>
        </div>
        <div id="foot-palette" class="footer-palette-grid"></div>
        <div class="selection-a-stack">
            <div class="dropup" onclick="toggleMenu(this)"><span>File</span><span>▲</span><div class="dropup-content"><a>New Project</a><a>Open</a></div></div>
            <div class="dropup" onclick="toggleMenu(this)"><span>Tools</span><span>▲</span><div class="dropup-content"><a>BOM Gen</a><a>Netlist</a></div></div>
            <div class="dropup" onclick="toggleMenu(this)"><span>View</span><span>▲</span><div class="dropup-content"><a>2D View</a><a>3D Render</a></div></div>
        </div>
        <div class="selection-b-container">
            <div class="dropup tall" onclick="openModal()"><span>AI-SET</span><span>▲</span></div>
        </div>
    </div>
</div>

<script>
    Split(['#left-stack', '#right-stack'], { sizes: [70, 30], gutterSize: 4 });
    Split(['#cad-pane', '#cmd-pane'], { direction: 'vertical', sizes: [80, 20], gutterSize: 4 });
    Split(['#ai-output', '#ai-input'], { direction: 'vertical', sizes: [50, 50], gutterSize: 4 });

    const side = document.getElementById('side-strip');
    for(let i=0; i<100; i++) side.innerHTML += '<div class="btn-cell"></div>';
    
    const palette = document.getElementById('foot-palette');
    for(let i=0; i<18; i++) palette.innerHTML += '<div class="btn-cell"></div>';

    function openModal() { document.getElementById('ai-modal').style.display = 'flex'; }
    function closeModal() { document.getElementById('ai-modal').style.display = 'none'; }
    
    function loadAI(name) {
        const panel = document.getElementById('config-panel');
        panel.innerHTML = `
            <div style="color:#ffaa00; font-weight:bold; margin-bottom:15px; border-bottom:1px solid #ffaa00; font-family:monospace; font-size:14px;">CONFIGURING ${name}</div>
            <div>
                <span class="label-text">SECURITY ACCESS KEY:</span>
                <input type="password" class="input-field" placeholder="AMBER-XXXX-XXXX">
            </div>
            <div>
                <span class="label-text">PRIMARY ARCHITECTURAL ROLE:</span>
                <select class="input-field">
                    <option>Hardware Architect</option>
                    <option>Industrial Automation</option>
                    <option>Logistics / BOM Manager</option>
                    <option>Code & Logic Engineer</option>
                </select>
            </div>
            <div style="font-size:10px; color:#ffaa00; margin-top:20px; opacity:0.5; font-family:monospace; line-height:1.4;">
                CRITICAL: THIS UNIT WILL INTERCEPT QUERIES TAGGED WITH THE ASSIGNED ROLE. ENSURE KEYS ARE VALID FOR CONTINUOUS UPTIME.
            </div>
        `;
    }

    function toggleMenu(el) {
        event.stopPropagation();
        const isActive = el.classList.contains('active');
        document.querySelectorAll('.dropup').forEach(d => d.classList.remove('active'));
        if(!isActive) el.classList.add('active');
    }

    window.onclick = function() {
        document.querySelectorAll('.dropup').forEach(d => d.classList.remove('active'));
    };

    const promptInput = document.getElementById('user-prompt');
    const aiChat = document.getElementById('ai-chat');
    const terminal = document.getElementById('terminal-out');

    promptInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            const text = promptInput.value.trim();
            if(text !== "") {
                aiChat.innerHTML += "<br><br><span style='color:#fff'>[USER]:</span> " + text;
                terminal.innerHTML += "\\n> DISPATCHING COMMAND TO CORE ARCHITECT...";
                aiChat.innerHTML += "<br><span style='color:#ffaa00'>[AI]:</span> Executing analysis on request parameters...";
                promptInput.value = ""; 
                aiChat.scrollTop = aiChat.scrollHeight;
                terminal.scrollTop = terminal.scrollHeight;
            }
        }
    });
</script>
"""

components.html(cad_app_html, height=0)
st.components.v1.html(
    f"""<script>
        window.parent.document.querySelector('iframe').style.height = '94vh';
    </script>""",
    height=0
)
