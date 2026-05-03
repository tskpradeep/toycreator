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

    /* --- NEW AI MODULAR WINDOW (GREEN VIBE) --- */
    #ai-modular-setup {
        position: absolute; top: 10%; left: 15%; width: 70%; height: 75%;
        background: #000; border: 2px solid #00ff00; z-index: 9999;
        display: none; flex-direction: column; box-shadow: 0 0 40px rgba(0,255,0,0.2);
    }
    .ai-setup-header { background: #0a1a0a; border-bottom: 1px solid #00ff00; padding: 10px; display: flex; justify-content: space-between; color: #00ff00; font-family: monospace; }
    .ai-setup-body { display: flex; flex: 1; overflow: hidden; }
    .ai-setup-sidebar { width: 30%; border-right: 1px solid #00ff00; padding: 10px; background: #050505; overflow-y: auto; }
    .ai-setup-content { width: 70%; padding: 20px; color: #00ff00; font-family: monospace; display: flex; flex-direction: column; gap: 15px; }
    .ai-model-item { padding: 8px; border: 1px solid #004400; margin-bottom: 5px; cursor: pointer; font-size: 11px; }
    .ai-model-item:hover { border-color: #00ff00; background: #0a1a0a; }
    .ai-model-item.active { background: #00ff00; color: #000; font-weight: bold; }
    .ai-input { background: #000; border: 1px solid #00ff00; color: #00ff00; padding: 10px; width: 100%; outline: none; box-sizing: border-box; }
    .live-link { color: #00ff00; text-decoration: underline; font-size: 11px; cursor: pointer; }

    /* --- ORIGINAL GUI CSS --- */
    .window-title-bar {
        background: #1a1a1a; color: #888; height: 30px;
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
    .btn-cell:active { 
        border-top: 2px solid #707070; border-left: 2px solid #707070;
        border-right: 2px solid #fff; border-bottom: 2px solid #fff;
        background: #bebebe;
    }
    .pane { background: #000 !important; border: 1px solid #333 !important; overflow: hidden; display: flex; align-items: center; justify-content: center; box-sizing: border-box; }
    .gutter { background-color: #444 !important; }
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
    <!-- MODULAR SETUP WINDOW -->
    <div id="ai-modular-setup">
        <div class="ai-setup-header">
            <span>[ SYSTEM AI-SET : DISPATCHER CONFIG ]</span>
            <span onclick="toggleAISet(false)" style="cursor:pointer">[ EXIT ]</span>
        </div>
        <div class="ai-setup-body">
            <div class="ai-setup-sidebar" id="model-list">
                <div class="ai-model-item active" onclick="configModel(this, 'Gemini 3.0 Pro', 'Hardware Architect')">GEMINI 3.0 PRO (AUTO)</div>
                <div class="ai-model-item" onclick="configModel(this, 'Gemini 3.0 Flash', 'Code Specialist')">GEMINI 3.0 FLASH</div>
                <div class="ai-model-item" onclick="configModel(this, 'Gemini 2.0 Pro', 'Layout Optimizer')">GEMINI 2.0 PRO</div>
                <div class="ai-model-item" onclick="configModel(this, 'Gemini 1.5 Ultra', 'BOM Manager')">GEMINI 1.5 ULTRA</div>
            </div>
            <div class="ai-setup-content">
                <div style="font-size: 18px; border-bottom: 1px solid #004400; padding-bottom: 5px;">ACTIVE: <span id="model-title">Gemini 3.0 Pro</span></div>
                <div>
                    <label>MANUFACTURER ENDPOINT:</label>
                    <input type="text" class="ai-input" id="ai-endpoint" value="https://generativelanguage.googleapis.com/v1beta/">
                </div>
                <div>
                    <label>AUTHORIZATION KEY:</label>
                    <input type="password" class="ai-input" placeholder="ENTER API KEY...">
                    <a href="https://aistudio.google.com/app/apikey" target="_blank" class="live-link">GENERATE KEY VIA GOOGLE AI STUDIO ↗</a>
                </div>
                <div>
                    <label>AUTO-ASSIGNED ROLE:</label>
                    <input type="text" class="ai-input" id="ai-role" value="Hardware Architect">
                </div>
                <div style="margin-top: auto; display: flex; gap: 10px;">
                    <button class="btn-cell" style="width: auto; height: 30px; padding: 0 15px;" onclick="toggleAISet(false)">APPLY</button>
                    <button class="btn-cell" style="width: auto; height: 30px; padding: 0 15px;" onclick="toggleAISet(false)">RESET</button>
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
            <div class="dropup tall" onclick="toggleAISet(true)"><span>AI-SET</span><span>▲</span><div class="dropup-content"><a>Gerber</a><a>STEP</a><a>Tech Bundle</a></div></div>
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

    /* AI SETUP LOGIC */
    function toggleAISet(show) {
        document.getElementById('ai-modular-setup').style.display = show ? 'flex' : 'none';
    }

    function configModel(el, name, role) {
        document.querySelectorAll('.ai-model-item').forEach(i => i.classList.remove('active'));
        el.classList.add('active');
        document.getElementById('model-title').innerText = name;
        document.getElementById('ai-role').value = role;
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
    const monitor = document.getElementById('visual-monitor');

    promptInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            const text = promptInput.value.trim();
            if(text !== "") {
                aiChat.innerHTML += "<br><br><span style='color:#800080'>[USER]:</span> " + text;
                const query = text.toLowerCase();
                
                if(query.includes("led") || query.includes("circuit") || query.includes("power supply")) {
                    aiChat.innerHTML += "<br><span style='color:#008000'>[AI]:</span> Architecting system blocks...";
                    terminal.innerHTML += "\\n> COMPILING TECH BUNDLE LOGIC...";
                    
                    monitor.innerHTML = `
                        <div style="border:1px solid #fff; padding:10px; font-size:12px;">
                            <svg width="200" height="100">
                                <rect x="10" y="30" width="50" height="40" stroke="white" fill="none" />
                                <text x="15" y="55" fill="white" font-size="8">SOURCE</text>
                                <line x1="60" y1="50" x2="90" y2="50" stroke="#0f0" />
                                <circle cx="110" cy="50" r="20" stroke="#0f0" fill="none" />
                                <text x="102" y="53" fill="#0f0" font-size="8">LOAD</text>
                            </svg>
                            <div style="font-size:10px; margin-top:5px;">${text.toUpperCase()} DIAGRAM</div>
                        </div>
                    `;
                } else {
                    aiChat.innerHTML += "<br><span style='color:#008000'>[AI]:</span> Ready for architectural prompts.";
                }

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
