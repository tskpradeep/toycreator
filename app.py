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
        border: 2px solid #d3d3d3; box-sizing: border-box;
        position: relative;
    }

    .window-title-bar {
        background: #1a1a1a; color: #888; height: 30px;
        flex-shrink: 0; display: flex; align-items: center; 
        justify-content: space-between; padding: 0 10px; font-size: 12px;
        border-bottom: 1px solid #333;
    }

    #dynamic-zone { display: flex; flex-direction: row; flex: 1; min-height: 0; width: 100%; }

    /* DIMMED SLIDERS */
    .gutter.gutter-horizontal { background-color: #8b0000 !important; cursor: col-resize; } /* Dark Crimson */
    .gutter.gutter-vertical { background-color: #006400 !important; cursor: row-resize; }   /* Forest Green */

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

    .pane { background: #000 !important; border: 1px solid #333 !important; overflow: hidden; display: flex; align-items: center; justify-content: center; box-sizing: border-box; }

    /* AI CONFIGURATION MODAL (From image_ef9739.png) */
    #ai-modal {
        position: absolute; top: 15%; left: 15%; width: 70%; height: 60%;
        background: #000; border: 1px solid #0055ff; z-index: 5000;
        display: none; flex-direction: column; box-shadow: 0 0 20px rgba(0, 85, 255, 0.2);
    }
    .modal-header { background: #001133; border-bottom: 1px solid #0055ff; padding: 8px 12px; display: flex; justify-content: space-between; font-size: 11px; color: #00ccff; font-weight: bold; }
    .modal-body { display: flex; flex: 1; overflow: hidden; }
    .modal-sidebar { width: 35%; border-right: 1px solid #222; padding: 10px; display: flex; flex-direction: column; gap: 8px; }
    .modal-main { width: 65%; padding: 20px; display: flex; flex-direction: column; gap: 15px; }
    
    .ai-slot { background: #111; border: 1px solid #333; color: #aaa; padding: 8px; cursor: pointer; font-size: 11px; }
    .ai-slot.active { border-color: #00ccff; color: #fff; }
    .input-group { display: flex; flex-direction: column; gap: 5px; }
    .input-group label { font-size: 10px; color: #ffcc00; text-transform: uppercase; }
    .modal-input { background: #000; border: 1px solid #444; color: #fff; padding: 6px; font-size: 12px; outline: none; }
    .modal-input:focus { border-color: #00ccff; }

    .fixed-footer { 
        height: 64px; display: flex; flex-direction: row; 
        border-top: 2px solid #333; background: #000; flex-shrink: 0;
        align-items: flex-end; padding: 0px 4px 2px 4px;
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
    .dropup.tall { height: 62px; font-weight: bold; }
    .dropup-content { display: none; position: absolute; bottom: 100%; left: -1px; background-color: #f0f0f0; min-width: 140px; border: 1px solid #707070; z-index: 1000; }
    .dropup.active .dropup-content { display: block; }

    .text-main { color: #b22222; font-size: 1.4vw; font-weight: bold; text-align: center; width:100%; height:100%; }
    .ai-text-area { width: 100%; height: 100%; padding: 10px; color: #008000; font-family: 'Consolas', monospace; font-size: 13px; overflow-y: auto; text-align: left; }
    .user-input-area { width: 100%; height: 100%; background: transparent; border: none; color: #800080; padding: 10px; font-family: 'Consolas', monospace; outline: none; resize: none; font-weight: bold; }
    .cmd-text { width: 100%; height: 100%; color: #0f0; font-family: monospace; font-size: 11px; padding: 5px; overflow-y: auto; white-space: pre-wrap; }
</style>

<div class="master-container">
    <!-- AI DISPATCHER MODAL -->
    <div id="ai-modal">
        <div class="modal-header">
            <span>DISPATCHER CONFIGURATION</span>
            <span style="cursor:pointer" onclick="closeAIModal()">[ CLOSE X ]</span>
        </div>
        <div class="modal-body">
            <div class="modal-sidebar">
                <div class="ai-slot active">AI 01: Gemini 2.0 (Active)</div>
                <div class="ai-slot">AI 02: Llama 3 (Standby)</div>
                <button style="margin-top:auto; background:#ffcc00; border:none; padding:8px; font-weight:bold; cursor:pointer;">+ ADD NEW AI</button>
            </div>
            <div class="modal-main">
                <div class="input-group">
                    <label>Configuring Module</label>
                    <div style="color:#fff; font-weight:bold;">Gemini 2.0 Pro</div>
                </div>
                <div class="input-group">
                    <label>API Key Connection</label>
                    <input type="password" class="modal-input" value="sk-........................">
                </div>
                <div class="input-group">
                    <label>Assigned Technical Domain</label>
                    <select class="modal-input">
                        <option>Hardware Architect</option>
                        <option>Consumer Electronics</option>
                        <option>Industrial Automation</option>
                        <option>Firmware Specialist</option>
                    </select>
                </div>
                <p style="font-size:9px; color:#666; margin-top:10px;">Note: This AI will trigger automatically when prompts match the domain above.</p>
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
            <div class="dropup tall" style="background:#003366; color:#00ccff;" onclick="openAIModal()"><span>AI-SET</span><span>▲</span></div>
        </div>
    </div>
</div>

<script>
    Split(['#left-stack', '#right-stack'], { sizes: [70, 30], gutterSize: 6 });
    Split(['#cad-pane', '#cmd-pane'], { direction: 'vertical', sizes: [80, 20], gutterSize: 6 });
    Split(['#ai-output', '#ai-input'], { direction: 'vertical', sizes: [50, 50], gutterSize: 6 });

    const side = document.getElementById('side-strip');
    for(let i=0; i<100; i++) side.innerHTML += '<div class="btn-cell"></div>';
    
    const palette = document.getElementById('foot-palette');
    for(let i=0; i<18; i++) palette.innerHTML += '<div class="btn-cell"></div>';

    function openAIModal() { document.getElementById('ai-modal').style.display = 'flex'; }
    function closeAIModal() { document.getElementById('ai-modal').style.display = 'none'; }

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
                aiChat.innerHTML += "<br><br><span style='color:#800080'>[USER]:</span> " + text;
                terminal.innerHTML += "\\n> DISPATCHING TO HARDWARE ARCHITECT...";
                aiChat.innerHTML += "<br><span style='color:#008000'>[AI]:</span> Executing analysis via Gemini 2.0...";
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
