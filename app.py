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

    .window-title-bar { background: #1a1a1a; color: #888; height: 30px; flex-shrink: 0; display: flex; align-items: center; justify-content: space-between; padding: 0 10px; font-size: 12px; border-bottom: 1px solid #333; }
    #dynamic-zone { display: flex; flex-direction: row; flex: 1; min-height: 0; width: 100%; }
    .fixed-right-strip { width: 65px; border-left: 1px solid #333; display: grid; grid-template-columns: 1fr 1fr; grid-auto-rows: min-content; gap: 2px; padding: 5px; background: #000; overflow-y: scroll; }
    .btn-cell { aspect-ratio: 1 / 1; width: 20px; height: 20px; background: #e1e1e1; color: #000; border-top: 2px solid #fff; border-left: 2px solid #fff; border-right: 2px solid #707070; border-bottom: 2px solid #707070; cursor: pointer; display: flex; align-items: center; justify-content: center; box-sizing: border-box; flex-shrink: 0; }
    .pane { background: #000 !important; border: 1px solid #333 !important; overflow: hidden; display: flex; align-items: center; justify-content: center; box-sizing: border-box; }
    .gutter { background-color: #444 !important; }
    .fixed-footer { height: 64px; display: flex; flex-direction: row; border-top: 2px solid #333; background: #000; flex-shrink: 0; align-items: flex-end; padding: 0px 4px 2px 4px; }
    .footer-palette-grid { display: grid; grid-template-columns: repeat(6, 20px); grid-template-rows: repeat(3, 20px); gap: 1px; margin-left: 8px; }
    .dropup { position: relative; width: 100%; height: 20px; background: #e1e1e1; color: #000; border: 1px solid #707070; display: flex; align-items: center; justify-content: space-between; padding: 0 5px; cursor: pointer; font-size: 9px; box-sizing: border-box; }
    .dropup.tall { height: 62px; }
    .ai-text-area { width: 100%; height: 100%; padding: 10px; color: #00ff00; font-family: 'Consolas', monospace; font-size: 13px; overflow-y: auto; text-align: left; }
    .user-input-area { width: 100%; height: 100%; background: transparent; border: none; color: #800080; padding: 10px; font-family: 'Consolas', monospace; outline: none; resize: none; font-weight: bold; }
    .cmd-text { width: 100%; height: 100%; color: #0f0; font-family: monospace; font-size: 11px; padding: 5px; overflow-y: auto; white-space: pre-wrap; }
    .viz-container { width: 90%; height: 90%; border: 1px dashed #00ff00; display: flex; flex-direction: column; padding: 10px; color: #00ff00; font-family: monospace; }
    .block { border: 2px solid #00ff00; padding: 10px; margin: 10px; text-align: center; background: #050505; }
</style>

<div class="master-container">
    <div id="ai-modular-setup">
        <div class="ai-setup-header">
            <span>[ SYSTEM AI-SET : TOOL CONFIGURATION ]</span>
            <div class="ai-header-controls">
                <button onclick="saveData()" style="padding: 2px 12px; cursor: pointer; border: 1px solid #00ff00; background: #000; color: #00ff00;">SAVE</button>
                <button onclick="toggleAISet(false)" style="padding: 2px 12px; cursor: pointer; border: 1px solid #fff; background: #000; color: #fff;">[ X ]</button>
            </div>
        </div>
        <div class="ai-setup-body">
            <div class="ai-setup-sidebar">
                <div class="ai-tool-item active">GOOGLE GEMINI</div>
                <div class="ai-tool-item">LUVIA AI</div>
                <div class="ai-tool-item">FLUX.AI</div>
                <div class="ai-tool-item">KICAD</div>
                <div class="ai-tool-item">QUILTER</div>
                <div class="ai-tool-item">NTOP / FUSION</div>
            </div>
            <div class="ai-setup-content">
                <div style="font-size: 20px; color:#fff;">TOOL: <span id="tool-name">Google Gemini</span></div>
                <label>AVAILABLE VERSIONS:</label>
                <select class="ai-select" id="version-select">
                    <option value="gemini-1.5-flash">Gemini 1.5 Flash (Speed)</option>
                    <option value="gemini-1.5-pro">Gemini 1.5 Pro (Logic)</option>
                </select>
                <label>API KEY:</label>
                <input type="password" id="api-field-input" class="ai-input" placeholder="PASTE GEMINI API KEY HERE...">
            </div>
        </div>
    </div>

    <div class="window-title-bar">
        <div>CAD DESIGNER PRO</div>
        <div><span>−</span><span style="margin:0 10px;">❐</span><span>×</span></div>
    </div>

    <div id="dynamic-zone">
        <div id="split-container" style="display:flex; flex:1; width:100%;">
            <div id="left-stack" style="width:70%;">
                <div id="cad-pane" class="pane" style="height:80%;">
                    <div id="visual-monitor" style="color: #444; font-size: 12px; font-family: monospace;">[ IDLE ]</div>
                </div>
                <div id="cmd-pane" class="pane" style="height:20%;">
                    <div id="terminal-out" class="cmd-text">>_ SYSTEM INITIALIZED</div>
                </div>
            </div>
            <div id="right-stack" style="width:30%;">
                <div id="ai-output" class="pane" style="height:50%;">
                    <div id="ai-chat" class="ai-text-area">AWAITING PROMPT...</div>
                </div>
                <div id="ai-input" class="pane" style="height:50%;">
                    <textarea id="user-prompt" class="user-input-area" placeholder="TYPE HERE..."></textarea>
                </div>
            </div>
        </div>
        <div class="fixed-right-strip" id="side-strip"></div>
    </div>

    <div class="fixed-footer">
        <div class="footer-left-content">
            <span style="color:#00ff00; font-size: 11px;">CAD_ENGINE_ONLINE</span>
        </div>
        <div id="foot-palette" class="footer-palette-grid"></div>
        <div class="selection-b-container">
            <div class="dropup tall" onclick="toggleAISet(true)"><span>AI-SET</span><span>▲</span></div>
        </div>
    </div>
</div>

<script>
    Split(['#left-stack', '#right-stack'], { sizes: [70, 30], gutterSize: 4 });
    for(let i=0; i<100; i++) document.getElementById('side-strip').innerHTML += '<div class="btn-cell"></div>';
    for(let i=0; i<18; i++) document.getElementById('foot-palette').innerHTML += '<div class="btn-cell"></div>';

    function toggleAISet(show) { document.getElementById('ai-modular-setup').style.display = show ? 'flex' : 'none'; }

    function saveData() {
        const key = document.getElementById('api-field-input').value;
        if(key) localStorage.setItem('gemini_api_key', key);
        toggleAISet(false);
    }

    const promptInput = document.getElementById('user-prompt');
    const chatBox = document.getElementById('ai-chat');

    promptInput.addEventListener('keydown', async function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            const text = promptInput.value.trim();
            const key = localStorage.getItem('gemini_api_key');
            const version = document.getElementById('version-select').value;

            if(!text) return;
            chatBox.innerHTML += `<br><br><span style="color:#800080">[USER]:</span> ${text}`;
            promptInput.value = "";
            chatBox.scrollTop = chatBox.scrollHeight;

            if(!key) {
                chatBox.innerHTML += `<br><span style="color:red">[SYSTEM]: ERROR - NO API KEY FOUND IN AI-SET.</span>`;
                return;
            }

            chatBox.innerHTML += `<br><span id="loading" style="color:#555">[GEMINI]: Processing...</span>`;

            try {
                const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${version}:generateContent?key=${key}`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ contents: [{ parts: [{ text: text }] }] })
                });
                const data = await response.json();
                document.getElementById('loading').remove();
                const aiMsg = data.candidates[0].content.parts[0].text;
                chatBox.innerHTML += `<br><span style="color:#00ff00">[GEMINI]:</span> ${aiMsg}`;
                
                // Visualization Trigger
                if(text.toLowerCase().includes('circuit')) {
                    document.getElementById('visual-monitor').innerHTML = '<div class="viz-container"><div class="block">GENERATED ARCHITECTURE</div></div>';
                }
            } catch (err) {
                if(document.getElementById('loading')) document.getElementById('loading').remove();
                chatBox.innerHTML += `<br><span style="color:red">[SYSTEM]: API ERROR. Check Key.</span>`;
            }
            chatBox.scrollTop = chatBox.scrollHeight;
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
