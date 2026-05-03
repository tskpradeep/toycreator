import streamlit as st
import streamlit.components.v1 as components

# 1. Page Configuration
st.set_page_config(layout="wide", page_title="CAD Designer Pro")

# 2. UI Reset & Dark Theme Enforcement
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
    }

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
        aspect-ratio: 1 / 1; width: 22px; height: 22px;
        background: #e1e1e1; color: #000;
        border-top: 2px solid #fff; border-left: 2px solid #fff;
        border-right: 2px solid #707070; border-bottom: 2px solid #707070;
        cursor: pointer; display: flex; align-items: center; justify-content: center;
        box-sizing: border-box; flex-shrink: 0; font-size: 8px;
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
    .footer-palette-grid { display: grid; grid-template-columns: repeat(6, 20px); grid-template-rows: repeat(3, 20px); gap: 1px; margin-left: 8px; margin-bottom: 2px; }

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

    .text-main { color: #b22222; font-size: 1.4vw; font-weight: bold; text-align: center; width:100%; height:100%; overflow:auto; }
    .ai-text-area { width: 100%; height: 100%; padding: 10px; color: #00ff00; font-family: 'Consolas', monospace; font-size: 13px; overflow-y: auto; text-align: left; }
    .user-input-area { width: 100%; height: 100%; background: transparent; border: none; color: #ff00ff; padding: 10px; font-family: 'Consolas', monospace; outline: none; resize: none; font-weight: bold; }
    .cmd-text { width: 100%; height: 100%; color: #0f0; font-family: monospace; font-size: 11px; padding: 5px; overflow-y: auto; white-space: pre-wrap; }
</style>

<div class="master-container">
    <div class="window-title-bar">
        <div>[SYSTEM] CAD DESIGNER PRO - INDUSTRIAL CORE</div>
        <div><span>−</span><span style="margin:0 10px;">❐</span><span>×</span></div>
    </div>

    <div id="dynamic-zone">
        <div id="split-container" style="display:flex; flex:1; width:100%;">
            <div id="left-stack" style="display:flex; flex-direction:column; width:70%;">
                <div id="cad-pane" class="pane">
                    <div id="visual-monitor" class="text-main">
                        <div style="font-size: 12px; color: #555;">IDLE: AWAITING COMPILER INPUT</div>
                    </div>
                </div>
                <div id="cmd-pane" class="pane" style="justify-content: flex-start; align-items: flex-start;">
                    <div id="terminal-out" class="cmd-text">>_ SYSTEM INITIALIZED... READY.</div>
                </div>
            </div>
            <div id="right-stack" style="display:flex; flex-direction:column; width:30%;">
                <div id="ai-output" class="pane">
                    <div id="ai-chat" class="ai-text-area">[AI CORE]: ONLINE</div>
                </div>
                <div id="ai-input" class="pane">
                    <textarea id="user-prompt" class="user-input-area" placeholder="ENTER ARCHITECTURAL CMD..."></textarea>
                </div>
            </div>
        </div>
        <div class="fixed-right-strip" id="side-strip"></div>
    </div>

    <div class="fixed-footer">
        <div class="footer-left-content">
            <span style="color:#00ff00; font-family:monospace; font-size: 11px; margin-right: 20px;">[READY]</span>
            <span style="color:#0088ff; font-family:monospace; font-size: 11px;">BUS STATUS: NOMINAL</span>
        </div>
        <div id="foot-palette" class="footer-palette-grid"></div>
        <div class="selection-a-stack">
            <div class="dropup" onclick="toggleMenu(this)"><span>FILE</span><span>▲</span><div class="dropup-content"><a>NEW PROJECT</a><a>OPEN SCHEMA</a><a>SAVE ALL</a></div></div>
            <div class="dropup" onclick="toggleMenu(this)"><span>TOOLS</span><span>▲</span><div class="dropup-content"><a>BOM GEN</a><a>NETLIST</a><a>PART SEARCH</a></div></div>
            <div class="dropup" onclick="toggleMenu(this)"><span>VIEW</span><span>▲</span><div class="dropup-content"><a>2D TRACE</a><a>3D MESH</a><a>LAYERS</a></div></div>
        </div>
        <div class="selection-b-container">
            <div class="dropup tall" onclick="toggleMenu(this)"><span>EXPORT TECH BUNDLE</span><span>▲</span><div class="dropup-content"><a>GERBER (RS-274X)</a><a>STEP (3D)</a><a>PDF DOCUMENTATION</a></div></div>
        </div>
    </div>
</div>

<script>
    // Partitioning
    Split(['#left-stack', '#right-stack'], { sizes: [70, 30], gutterSize: 6 });
    Split(['#cad-pane', '#cmd-pane'], { direction: 'vertical', sizes: [80, 20], gutterSize: 6 });
    Split(['#ai-output', '#ai-input'], { direction: 'vertical', sizes: [60, 40], gutterSize: 6 });

    // Populate Sidebar Buttons
    const side = document.getElementById('side-strip');
    const icons = ['+', '-', '⬚', '○', '▧', '▨', '▤', '▥', '▦', '▧'];
    for(let i=0; i<100; i++) {
        side.innerHTML += `<div class="btn-cell">${icons[i%10]}</div>`;
    }
    
    // Populate Footer Palette
    const palette = document.getElementById('foot-palette');
    const colors = ['#000', '#800', '#080', '#880', '#008', '#808', '#088', '#ccc', '#888', '#f00', '#0f0', '#ff0', '#00f', '#f0f', '#0ff', '#fff', '#ddd', '#444'];
    colors.forEach(c => {
        palette.innerHTML += `<div class="btn-cell" style="background:${c}"></div>`;
    });

    function toggleMenu(el) {
        event.stopPropagation();
        const isActive = el.classList.contains('active');
        document.querySelectorAll('.dropup').forEach(d => d.classList.remove('active'));
        if(!isActive) el.classList.add('active');
    }

    window.onclick = function() {
        document.querySelectorAll('.dropup').forEach(d => d.classList.remove('active'));
    };

    // Logic Integration
    const promptInput = document.getElementById('user-prompt');
    const aiChat = document.getElementById('ai-chat');
    const terminal = document.getElementById('terminal-out');
    const monitor = document.getElementById('visual-monitor');

    promptInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            const text = promptInput.value.trim();
            if(text !== "") {
                aiChat.innerHTML += `<br><br><span style="color:#ff00ff">[USR]:</span> ${text}`;
                const query = text.toLowerCase();
                
                terminal.innerHTML += `\\n> PROCESSING REQUEST: ${text.toUpperCase()}`;
                
                if(query.includes("circuit") || query.includes("led") || query.includes("block")) {
                    aiChat.innerHTML += "<br><span style='color:#00ff00'>[AI]:</span> ARCHITECTING BLOCK DIAGRAM...";
                    terminal.innerHTML += "\\n> COMPILING SCHEMA DATA... DONE.";
                    
                    monitor.innerHTML = `
                        <div style="padding:20px; border:1px dashed #444; background:#050505;">
                            <svg width="300" height="150" viewBox="0 0 300 150">
                                <rect x="20" y="50" width="80" height="50" stroke="#00ff00" fill="none" stroke-width="2"/>
                                <text x="35" y="80" fill="#00ff00" font-size="10">INPUT</text>
                                <line x1="100" y1="75" x2="150" y2="75" stroke="#ff00ff" stroke-width="2" />
                                <circle cx="180" cy="75" r="30" stroke="#0088ff" fill="none" stroke-width="2"/>
                                <text x="165" y="80" fill="#0088ff" font-size="10">CORE</text>
                            </svg>
                            <div style="font-size:10px; color:#aaa;">SYS_GEN: ${text.toUpperCase()}</div>
                        </div>
                    `;
                } else {
                    aiChat.innerHTML += "<br><span style='color:#00ff00'>[AI]:</span> COMMAND RECOGNIZED. READY FOR NEXT TASK.";
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
