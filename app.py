import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="CAD Designer Pro")

st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stApp { background-color: #000 !important; overflow: hidden !important; }
        .block-container { padding: 0rem !important; max-width: 100% !important; height: 100vh !important; }
    </style>
""", unsafe_allow_html=True)

cad_app_html = """
<script src="https://cdnjs.cloudflare.com/ajax/libs/split.js/1.6.0/split.min.js"></script>
<style>
    html, body { margin: 0; padding: 0; height: 100%; width: 100%; overflow: hidden; background-color: #000; font-family: monospace; color: white; }
    .master-container { display: flex; flex-direction: column; height: 100vh; width: 100vw; border: 2px solid #333; box-sizing: border-box; }
    #ai-modular-setup { position: absolute; top: 15%; left: 20%; width: 60%; height: 60%; background: #000; border: 2px solid #00ff00; z-index: 9999; display: none; flex-direction: column; }
    .ai-setup-header { background: #0a1a0a; border-bottom: 1px solid #00ff00; padding: 10px; display: flex; justify-content: space-between; color: #00ff00; }
    .ai-setup-content { padding: 20px; display: flex; flex-direction: column; gap: 15px; }
    .ai-select, .ai-input { background: #000; border: 1px solid #00ff00; color: #00ff00; padding: 8px; width: 100%; outline: none; }
    .window-title-bar { background: #1a1a1a; color: #888; height: 30px; display: flex; align-items: center; justify-content: space-between; padding: 0 10px; font-size: 12px; border-bottom: 1px solid #333; }
    #dynamic-zone { display: flex; flex: 1; width: 100%; min-height: 0; }
    .fixed-right-strip { width: 65px; border-left: 1px solid #333; display: grid; grid-template-columns: 1fr 1fr; gap: 2px; padding: 5px; overflow-y: auto; }
    .btn-cell { width: 20px; height: 20px; background: #e1e1e1; border: 2px solid; border-color: #fff #707070 #707070 #fff; }
    .pane { background: #000; border: 1px solid #333; display: flex; overflow: hidden; }
    .fixed-footer { height: 60px; display: flex; border-top: 2px solid #333; background: #000; }
    .ai-text-area { width: 100%; height: 100%; padding: 10px; color: #00ff00; font-size: 13px; overflow-y: auto; white-space: pre-wrap; }
    .user-input-area { width: 100%; height: 100%; background: transparent; border: none; color: #800080; padding: 10px; font-weight: bold; resize: none; outline: none; }
    .cmd-text { width: 100%; height: 100%; color: #0f0; font-size: 11px; padding: 5px; overflow-y: auto; }
</style>

<div class="master-container">
    <div id="ai-modular-setup">
        <div class="ai-setup-header"><span>[ CONFIGURATION ]</span><button onclick="toggleAISet(false)" style="color:#fff; background:0; border:0; cursor:pointer;">[X]</button></div>
        <div class="ai-setup-content">
            <label>API MODEL:</label>
            <select class="ai-select" id="version-select">
                <option value="gemini-1.5-pro">gemini-1.5-pro</option>
                <option value="gemini-1.5-flash">gemini-1.5-flash</option>
            </select>
            <label>API KEY:</label>
            <input type="password" id="api-field-input" class="ai-input" placeholder="Paste Key Here">
            <button onclick="saveData()" style="background:#00ff00; color:#000; border:0; padding:10px; cursor:pointer; font-weight:bold;">APPLY & SAVE</button>
        </div>
    </div>

    <div class="window-title-bar"><div>CAD_PRO_V3.2</div><div>_ □ ×</div></div>

    <div id="dynamic-zone">
        <div id="left-stack" style="display:flex; flex-direction:column; width:70%;">
            <div id="cad-pane" class="pane" style="flex:4; justify-content:center; align-items:center; color:#333;">[VIEWPORT]</div>
            <div id="cmd-pane" class="pane" style="flex:1;"><div id="terminal-out" class="cmd-text">>_ SYSTEM READY</div></div>
        </div>
        <div id="right-stack" style="display:flex; flex-direction:column; width:30%;">
            <div id="ai-output" class="pane" style="flex:1;"><div id="ai-chat" class="ai-text-area">AWAITING API KEY...</div></div>
            <div id="ai-input" class="pane" style="flex:1;"><textarea id="user-prompt" class="user-input-area" placeholder="TYPE..."></textarea></div>
        </div>
        <div class="fixed-right-strip" id="side-strip"></div>
    </div>

    <div class="fixed-footer">
        <div style="flex:1; display:flex; align-items:center; color:#00ff00; padding-left:15px; font-size:12px;">CORE_STATUS: OK</div>
        <div style="width:120px; background:#e1e1e1; color:#000; text-align:center; cursor:pointer; line-height:60px; font-weight:bold;" onclick="toggleAISet(true)">AI-SET ▲</div>
    </div>
</div>

<script>
    Split(['#left-stack', '#right-stack'], { sizes: [70, 30], gutterSize: 4 });
    for(let i=0; i<60; i++) document.getElementById('side-strip').innerHTML += '<div class="btn-cell"></div>';
    
    function toggleAISet(show) { document.getElementById('ai-modular-setup').style.display = show ? 'flex' : 'none'; }

    function saveData() {
        const key = document.getElementById('api-field-input').value;
        const model = document.getElementById('version-select').value;
        localStorage.setItem('gemini_api_key', key);
        localStorage.setItem('gemini_model', model);
        document.getElementById('terminal-out').innerHTML += "\\n> UPDATED: " + model;
        toggleAISet(false);
    }

    async function callGemini(text) {
        const apiKey = localStorage.getItem('gemini_api_key');
        const model = localStorage.getItem('gemini_model') || 'gemini-1.5-flash';
        const chat = document.getElementById('ai-chat');
        const term = document.getElementById('terminal-out');
        
        if(!apiKey) { chat.innerHTML = "[ERROR]: OPEN AI-SET AND ENTER KEY"; return; }

        try {
            term.innerHTML += "\\n> REQ: " + model;
            const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ contents: [{ parts: [{ text: text }] }] })
            });
            const data = await response.json();
            if(data.error) throw new Error(data.error.message);
            
            const result = data.candidates[0].content.parts[0].text;
            chat.innerHTML += `<br><br><span style="color:#00ff00">[${model}]:</span> ${result}`;
            term.innerHTML += "\\n> RES: 200 OK";
            chat.scrollTop = chat.scrollHeight;
        } catch (e) {
            chat.innerHTML += `<br><span style="color:red">[FAIL]: ${e.message}</span>`;
            term.innerHTML += "\\n> RES: ERR";
        }
    }

    document.getElementById('user-prompt').addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            const val = this.value.trim();
            if(val) {
                document.getElementById('ai-chat').innerHTML += "<br><br><span style='color:#800080'>[USER]:</span> " + val;
                callGemini(val);
                this.value = "";
            }
        }
    });
</script>
"""

components.html(cad_app_html, height=0)
st.components.v1.html(
    f"""<script>window.parent.document.querySelector('iframe').style.height = '94vh';</script>""",
    height=0
)
