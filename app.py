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
        font-family: 'Consolas', 'Courier New', monospace; color: #0f0;
    }
    
    .master-container { 
        display: flex; flex-direction: column; 
        height: 100vh; width: 100vw; background: #000;
        border: 2px solid #0f0; box-sizing: border-box;
        position: relative;
    }

    .window-title-bar {
        background: #0a1a0a; color: #0f0; height: 30px;
        flex-shrink: 0; display: flex; align-items: center; 
        justify-content: space-between; padding: 0 10px; font-size: 12px;
        border-bottom: 1px solid #0f0;
    }

    #dynamic-zone { display: flex; flex-direction: row; flex: 1; min-height: 0; width: 100%; }

    /* DIMMED SLIDERS */
    .gutter.gutter-horizontal { background-color: #550000 !important; cursor: col-resize; } 
    .gutter.gutter-vertical { background-color: #003300 !important; cursor: row-resize; }

    .fixed-right-strip { 
        width: 65px; border-left: 1px solid #0f0; 
        display: grid; grid-template-columns: 1fr 1fr;
        grid-auto-rows: min-content; gap: 2px;
        padding: 5px; background: #000; 
        overflow-y: scroll; 
    }

    .btn-cell {
        aspect-ratio: 1 / 1; width: 20px; height: 20px;
        background: #0f0; color: #000;
        border: 1px solid #000;
        cursor: pointer; display: flex; align-items: center; justify-content: center;
        box-sizing: border-box; flex-shrink: 0; font-size: 10px; font-weight: bold;
    }

    .pane { background: #000 !important; border: 1px solid #050 !important; overflow: hidden; display: flex; align-items: center; justify-content: center; box-sizing: border-box; }

    /* BREATHING ANIMATION */
    @keyframes breathe {
        0% { box-shadow: 0 0 5px #0f0; border-color: #050; }
        50% { box-shadow: 0 0 20px #0f0; border-color: #0f0; }
        100% { box-shadow: 0 0 5px #0f0; border-color: #050; }
    }

    #ai-modal {
        position: absolute; top: 10%; left: 10%; width: 80%; height: 70%;
        background: #000; border: 2px solid #0f0; z-index: 5000;
        display: none; flex-direction: column;
        animation: breathe 3s infinite ease-in-out;
    }
    
    .modal-header { background: #0a1a0a; border-bottom: 1px solid #0f0; padding: 10px; display: flex; justify-content: space-between; color: #0f0; font-weight: bold; }
    .modal-body { display: flex; flex: 1; overflow: hidden; }
    .modal-sidebar { width: 30%; border-right: 1px solid #0f0; padding: 10px; display: flex; flex-direction: column; gap: 10px; background: #050505; }
    .modal-main { width: 70%; padding: 25px; display: flex; flex-direction: column; gap: 20px; background: #000; }
    
    .ai-option { 
        padding: 12px; border: 1px solid #050; color: #0f0; cursor: pointer; font-size: 11px; transition: 0.2s;
    }
    .ai-option:hover { background: #001a00; border-color: #0f0; }
    .ai-option.selected { background: #0f0; color: #000; font-weight: bold; }

    .field-label { font-size: 10px; color: #0f0; text-transform: uppercase; margin-bottom: 5px; display: block; opacity: 0.8; }
    .field-input { background: #000; border: 1px solid #0f0; color: #0f0; padding: 10px; width: 100%; box-sizing: border-box; font-family: monospace; outline: none; }

    .fixed-footer { 
        height: 64px; display: flex; flex-direction: row; 
        border-top: 2px solid #0f0; background: #000; flex-shrink: 0;
        align-items: flex-end; padding: 0px 4px 2px 4px;
    }

    .footer-left-content { flex: 1; display: flex; height: 100%; align-items: center; padding-left: 10px; color: #0f0; font-size: 11px;}
    .selection-b-container { width: 130px; height: 62px; margin-left: 5px; }
    .selection-a-stack { display: flex; flex-direction: column; gap: 1px; width: 130px; margin-left: 5px; }
    
    .dropup { 
        position: relative; width: 100%; height: 20px; 
        background: #000; color: #0f0; border: 1px solid #0f0; 
        display: flex; align-items: center; justify-content: space-between;
        padding: 0 5px; cursor: pointer; font-size: 9px; box-sizing: border-box;
    }
    .dropup.tall { height: 62px; font-weight: bold; font-size: 12px; animation: breathe 4s infinite; }
    
    .text-main { color: #0f0; font-size: 1.5vw; text-align: center; }
    .ai-text-area { width: 100%; height: 100%; padding: 10px; color: #0f0; font-size: 13px; overflow-y: auto; }
    .user-input-area { width: 100%; height: 100%; background: transparent; border: none; color: #fff; padding: 10px; font-family: monospace; outline: none; resize: none; }
</style>

<div class="master-container">
    <!-- AI SETTINGS MODAL -->
    <div id="ai-modal">
        <div class="modal-header">
            <span>AI CORE DISPATCHER</span>
            <span style="cursor:pointer" onclick="closeAI()">[ X ]</span>
        </div>
        <div class="modal-body">
            <div class="modal-sidebar">
                <div class="ai-option selected" onclick="selectAI(this, 'Gemini 2.0 Pro', 'Hardware Architect')">UNIT 01: GEMINI 2.0</div>
                <div class="ai-option" onclick="selectAI(this, 'Llama 3.1 405B', 'Industrial Automation')">UNIT 02: LLAMA 3.1</div>
                <div class="ai-option" onclick="selectAI(this, 'Groq-Mixtral', 'Code Specialist')">UNIT 03: GROQ-MIXTRAL</div>
            </div>
            <div id="config-ui" class="modal-main">
                <div>
                    <span class="field-label">Active Module</span>
                    <div id="active-name" style="font-size:18px; font-weight:bold;">Gemini 2.0 Pro</div>
                </div>
                <div>
                    <span class="field-label">Endpoint API Key</span>
                    <input type="password" class="field-input" value="••••••••••••••••">
                </div>
                <div>
                    <span class="field-label">Assigned Engineering Domain</span>
                    <select id="active-domain" class="field-input">
                        <option>Hardware Architect</option>
                        <option>Industrial Automation</option>
                        <option>Consumer Electronics</option>
                        <option>Systems Design</option>
                    </select>
                </div>
                <button style="background:#0f0; color:#000; border:none; padding:12px; font-weight:bold; cursor:pointer; margin-top:auto;">SAVE CONFIGURATION</button>
            </div>
        </div>
    </div>

    <div class="window-title-bar">
        <div>CAD DESIGNER PRO [VER 4.2]</div>
        <div><span>_</span><span style="margin:0 10px;">[ ]</span><span>X</span></div>
    </div>

    <div id="dynamic-zone">
        <div id="split-container" style="display:flex; flex:1; width:100%;">
            <div id="left-stack" style="display:flex; flex-direction:column; width:70%;">
                <div id="cad-pane" class="pane text-main">CAD ENGINE STANDBY</div>
                <div id="cmd-pane" class="pane" style="justify-content:flex-start; align-items:flex-start;">
                    <div id="terminal" style="color:#0f0; font-size:11px; padding:10px;">>_ KERNEL LOADED</div>
                </div>
            </div>
            <div id="right-stack" style="display:flex; flex-direction:column; width:30%;">
                <div id="ai-output" class="pane">
                    <div id="ai-chat" class="ai-text-area">AWAITING INPUT...</div>
                </div>
                <div id="ai-input" class="pane">
                    <textarea id="user-prompt" class="user-input-area" placeholder="ENTER SYSTEM COMMAND..."></textarea>
                </div>
            </div>
        </div>
        <div class="fixed-right-strip" id="side-strip"></div>
    </div>

    <div class="fixed-footer">
        <div class="footer-left-content">
            <span>STATUS: NOMINAL</span>
            <span style="margin-left:20px;">AI-LINK: ENCRYPTED</span>
        </div>
        <div class="selection-a-stack">
            <div class="dropup"><span>FILE</span><span>▲</span></div>
            <div class="dropup"><span>TOOLS</span><span>▲</span></div>
            <div class="dropup"><span>VIEW</span><span>▲</span></div>
        </div>
        <div class="selection-b-container">
            <div class="dropup tall" onclick="openAI()"><span>AI-SET</span><span>▲</span></div>
        </div>
    </div>
</div>

<script>
    Split(['#left-stack', '#right-stack'], { sizes: [70, 30], gutterSize: 6 });
    Split(['#cad-pane', '#cmd-pane'], { direction: 'vertical', sizes: [80, 20], gutterSize: 6 });
    Split(['#ai-output', '#ai-input'], { direction: 'vertical', sizes: [50, 50], gutterSize: 6 });

    const side = document.getElementById('side-strip');
    for(let i=0; i<100; i++) side.innerHTML += '<div class="btn-cell">+</div>';

    function openAI() { document.getElementById('ai-modal').style.display = 'flex'; }
    function closeAI() { document.getElementById('ai-modal').style.display = 'none'; }

    function selectAI(el, name, domain) {
        document.querySelectorAll('.ai-option').forEach(opt => opt.classList.remove('selected'));
        el.classList.add('selected');
        document.getElementById('active-name').innerText = name;
        document.getElementById('active-domain').value = domain;
    }

    const promptInput = document.getElementById('user-prompt');
    const aiChat = document.getElementById('ai-chat');
    const terminal = document.getElementById('terminal');

    promptInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            const text = promptInput.value.trim();
            if(text !== "") {
                aiChat.innerHTML += "<br><br><span style='color:#fff'>[USER]:</span> " + text;
                terminal.innerHTML += "\\n> DISPATCHING TO " + document.getElementById('active-name').innerText.toUpperCase() + "...";
                aiChat.innerHTML += "<br><span style='color:#0f0'>[AI]:</span> Processing technical request...";
                promptInput.value = ""; 
                aiChat.scrollTop = aiChat.scrollHeight;
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
