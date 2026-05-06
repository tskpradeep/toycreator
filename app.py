import streamlit as st
import streamlit.components.v1 as components

# 1. Page Configuration
st.set_page_config(layout="wide", page_title="CAD Designer Pro")

# 2. UI Reset (Strictly Restored)
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

# 3. Native UI Application (All 6 AIs & Original GUI untouched)
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
    
    /* THE 100 BUTTON STRIP */
    .fixed-right-strip { width: 65px; border-left: 1px solid #333; display: grid; grid-template-columns: 1fr 1fr; grid-auto-rows: min-content; gap: 2px; padding: 5px; background: #000; overflow-y: scroll; }
    .btn-cell { aspect-ratio: 1 / 1; width: 20px; height: 20px; background: #e1e1e1; color: #000; border-top: 2px solid #fff; border-left: 2px solid #fff; border-right: 2px solid #707070; border-bottom: 2px solid #707070; cursor: pointer; display: flex; align-items: center; justify-content: center; box-sizing: border-box; flex-shrink: 0; }
    .btn-cell:active { border-top: 2px solid #707070; border-left: 2px solid #707070; border-right: 2px solid #fff; border-bottom: 2px solid #fff; background: #bebebe; }
    
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

    /* CHAT WINDOWS */
    .ai-text-area { width: 100%; height: 100%; padding: 15px; color: #00ff00; font-family: 'Consolas', monospace; font-size: 13px; overflow-y: auto; text-align: left; scroll-behavior: smooth;}
    .user-input-area { width: 100%; height: 100%; background: #000; border: none; color: #800080; padding: 15px; font-family: 'Consolas', monospace; outline: none; resize: none; font-weight: bold; }
</style>

<div class="master-container">
    <!-- RESTORED AI-SET MENU -->
    <div id="ai-modular-setup">
        <div class="ai-setup-header">
            <span>[ SYSTEM AI-SET : TOOL CONFIGURATION ]</span>
            <div class="ai-header-controls">
                <button onclick="saveData()" style="cursor:pointer; background:#000; color:#00ff00; border:1px solid #00ff00;">SAVE</button>
                <button onclick="toggleAISet(false)" style="cursor:pointer; background:#000; color:#fff; border:1px solid #fff;">[ X ]</button>
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
                <div style="font-size: 20px; color:#fff;">TOOL: GOOGLE GEMINI</div>
                <label>VERSION:</label>
                <select class="ai-select" id="v-sel">
                    <option value="gemini-1.5-flash">Gemini 1.5 Flash</option>
                    <option value="gemini-1.5-pro">Gemini 1.5 Pro</option>
                </select>
                <label>API KEY:</label>
                <input type="password" id="api-in" class="ai-input" placeholder="ENTER KEY...">
            </div>
        </div>
    </div>

    <div class="window-title-bar">
        <div>CAD DESIGNER PRO - SYSTEM ACTIVE</div>
        <div><span>−</span><span style="margin:0 10px;">❐</span><span>×</span></div>
    </div>

    <div id="dynamic-zone">
        <div id="split-container" style="display:flex; flex:1;">
            <div id="left-stack" style="width:70%;">
                <div id="cad-pane" class="pane" style="height:80%; color:#b22222; font-weight:bold;">VISUALIZATION ENGINE</div>
                <div id="cmd-pane" class="pane" style="height:20%; color:#0f0; font-family:monospace; font-size:11px; padding:10px;">>_ SYSTEM READY</div>
            </div>
            <div id="right-stack" style="width:30%;">
                <div id="ai-output" class="pane" style="height:50%;">
                    <div id="ai-chat" class="ai-text-area">Awaiting API Key Configuration...</div>
                </div>
                <div id="ai-input" class="pane" style="height:50%;">
                    <textarea id="user-prompt" class="user-input-area" placeholder="Type message to Gemini... (Press Enter)"></textarea>
                </div>
            </div>
        </div>
        <div class="fixed-right-strip" id="side-strip"></div>
    </div>

    <div class="fixed-footer">
        <div class="footer-left-content"><span style="color:#00ff00; font-size:11px;">MODULAR CAD v1.0.4</span></div>
        <div id="foot-palette" class="footer-palette-grid"></div>
        <div class="selection-a-stack">
            <div class="dropup"><span>File</span><span>▲</span></div>
            <div class="dropup"><span>Tools</span><span>▲</span></div>
            <div class="dropup"><span>View</span><span>▲</span></div>
        </div>
        <div class="selection-b-container">
            <div class="dropup tall" onclick="toggleAISet(true)"><span>AI-SET</span><span>▲</span></div>
        </div>
    </div>
</div>

<script>
    // Restore Splits
    Split(['#left-stack', '#right-stack'], { sizes: [70, 30], gutterSize: 4 });
    
    // Fill the 100 button strip
    const strip = document.getElementById('side-strip');
    for(let i=0; i<100; i++) strip.innerHTML += '<div class="btn-cell"></div>';
    
    // Fill footer palette
    const pal = document.getElementById('foot-palette');
    for(let i=0; i<18; i++) pal.innerHTML += '<div class="btn-cell"></div>';

    function toggleAISet(show) { document.getElementById('ai-modular-setup').style.display = show ? 'flex' : 'none'; }
    
    function saveData() {
        const key = document.getElementById('api-in').value;
        if(key) {
            localStorage.setItem('gemini_key', key);
            document.getElementById('ai-chat').innerHTML = "SYSTEM: Gemini API connected. Ready for prompt.";
        }
        toggleAISet(false);
    }

    // GEMINI LOGIC (Studio Style)
    async function callGemini(prompt) {
        const key = localStorage.getItem('gemini_key');
        if(!key) return "ERROR: Enter API Key in AI-SET menu.";
        
        try {
            const resp = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${key}`, {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({ contents: [{ parts: [{ text: prompt }] }] })
            });
            const data = await resp.json();
            return data.candidates[0].content.parts[0].text;
        } catch (e) { return "SYSTEM ERROR: Check connection or API Key."; }
    }

    const input = document.getElementById('user-prompt');
    input.addEventListener('keydown', async (e) => {
        if(e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            const msg = input.value;
            input.value = "";
            const chat = document.getElementById('ai-chat');
            chat.innerHTML += `<div style="color:#800080; margin-top:10px;">[USER]: ${msg}</div>`;
            chat.innerHTML += `<div id="loading" style="color:#555;">[GEMINI]: Thinking...</div>`;
            
            const reply = await callGemini(msg);
            document.getElementById('loading').remove();
            chat.innerHTML += `<div style="color:#00ff00; margin-top:5px;">[GEMINI]: ${reply}</div>`;
            chat.scrollTop = chat.scrollHeight;
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
