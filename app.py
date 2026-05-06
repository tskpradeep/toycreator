import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="CAD Designer Pro")

st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stApp { background-color: #000 !important; overflow: hidden !important; }
        .block-container { padding: 0rem !important; max-width: 100% !important; height: 100vh !important; overflow: hidden !important; }
    </style>
""", unsafe_allow_html=True)

cad_app_html = """
<script src="https://cdnjs.cloudflare.com/ajax/libs/split.js/1.6.0/split.min.js"></script>
<style>
    html, body { margin: 0; padding: 0; height: 100%; width: 100%; overflow: hidden; background-color: #000; font-family: 'Segoe UI', Tahoma, sans-serif; color: white; }
    .master-container { display: flex; flex-direction: column; height: 100vh; width: 100vw; background: #000; border: 2px solid #d3d3d3; box-sizing: border-box; position: relative; }
    #ai-modular-setup { position: absolute; top: 10%; left: 15%; width: 70%; height: 75%; background: #000; border: 2px solid #00ff00; z-index: 9999; display: none; flex-direction: column; }
    .ai-setup-header { background: #0a1a0a; border-bottom: 1px solid #00ff00; padding: 10px; display: flex; justify-content: space-between; color: #00ff00; font-family: monospace; }
    .ai-setup-body { display: flex; flex: 1; overflow: hidden; }
    .ai-setup-sidebar { width: 30%; border-right: 1px solid #00ff00; padding: 10px; background: #050505; }
    .ai-setup-content { width: 70%; padding: 25px; color: #00ff00; font-family: monospace; display: flex; flex-direction: column; gap: 20px; }
    .ai-tool-item { padding: 12px; border: 1px solid #004400; margin-bottom: 8px; cursor: pointer; font-size: 12px; }
    .ai-tool-item.active { background: #00ff00; color: #000; font-weight: bold; }
    .ai-select { background: #000; border: 1px solid #00ff00; color: #00ff00; padding: 10px; width: 100%; font-family: monospace; }
    .ai-input { background: #000; border: 1px solid #00ff00; color: #00ff00; padding: 10px; width: 100%; box-sizing: border-box; }
    .tool-link { font-size: 11px; color: #00ff00; text-decoration: underline; cursor: pointer; }
    .window-title-bar { background: #1a1a1a; color: #888; height: 30px; display: flex; align-items: center; justify-content: space-between; padding: 0 10px; font-size: 12px; border-bottom: 1px solid #333; }
    #dynamic-zone { display: flex; flex: 1; width: 100%; min-height: 0; }
    .fixed-right-strip { width: 65px; border-left: 1px solid #333; display: grid; grid-template-columns: 1fr 1fr; gap: 2px; padding: 5px; background: #000; overflow-y: scroll; }
    .btn-cell { width: 20px; height: 20px; background: #e1e1e1; border: 2px solid; border-color: #fff #707070 #707070 #fff; }
    .pane { background: #000; border: 1px solid #333; overflow: hidden; display: flex; align-items: center; justify-content: center; }
    .fixed-footer { height: 64px; display: flex; border-top: 2px solid #333; background: #000; padding: 0 4px; }
    .ai-text-area { width: 100%; height: 100%; padding: 10px; color: #00ff00; font-family: monospace; font-size: 13px; overflow-y: auto; }
    .user-input-area { width: 100%; height: 100%; background: transparent; border: none; color: #800080; padding: 10px; font-family: monospace; font-weight: bold; resize: none; outline: none; }
    .cmd-text { width: 100%; height: 100%; color: #0f0; font-family: monospace; font-size: 11px; padding: 5px; overflow-y: auto; white-space: pre-wrap; }
</style>

<div class="master-container">
    <div id="ai-modular-setup">
        <div class="ai-setup-header">
            <span>[ TOOL CONFIGURATION ]</span>
            <div>
                <button onclick="saveData()" style="color:#00ff00; background:0; border:1px solid #00ff00; cursor:pointer;">SAVE</button>
                <button onclick="toggleAISet(false)" style="color:#fff; background:0; border:1px solid #fff; cursor:pointer; margin-left:10px;">[ X ]</button>
            </div>
        </div>
        <div class="ai-setup-body">
            <div class="ai-setup-sidebar"><div class="ai-tool-item active">GOOGLE GEMINI</div></div>
            <div class="ai-setup-content">
                <label>MODEL:</label>
                <select class="ai-select" id="version-select">
                    <option value="gemini-1.5-pro">gemini-1.5-pro</option>
                    <option value="gemini-1.5-flash">gemini-1.5-flash</option>
                </select>
                <label>API KEY:</label>
                <input type="password" id="api-field-input" class="ai-input">
                <a class="tool-link" href="https://aistudio.google.com/app/apikey" target="_blank">Get Official API Key</a>
            </div>
        </div>
    </div>

    <div class="window-title-bar"><div>CAD DESIGNER PRO</div><div><span>−</span><span style="margin:0 10px;">❐</span><span>×</span></div></div>

    <div id="dynamic-zone">
        <div id="left-stack" style="display:flex; flex-direction:column; width:70%;">
            <div id="cad-pane" class="pane" style="flex:4;"><div style="color: #444; font-family: monospace;">[ IDLE ]</div></div>
            <div id="cmd-pane" class="pane" style="flex:1;"><div id="terminal-out" class="cmd-text">>_ READY</div></div>
        </div>
        <div id="right-stack" style="display:flex; flex-direction:column; width:30%;">
            <div id="ai-output" class="pane" style="flex:1;"><div id="ai-chat" class="ai-text-area"></div></div>
            <div id="ai-input" class="pane" style="flex:1;"><textarea id="user-prompt" class="user-input-area" placeholder="INPUT COMMAND..."></textarea></div>
        </div>
        <div class="fixed-right-strip" id="side-strip"></div>
    </div>

    <div class="fixed-footer">
        <div style="flex:1; display:flex; align-items:center; color:#00ff00; font-size:10px; padding-left:10px;">ONLINE</div>
        <div style="width:130px; background:#e1e1e1; color:#000; text-align:center; cursor:pointer; line-height:60px; font-weight:bold;" onclick="toggleAISet(true)">AI-SET ▲</div>
    </div>
</div>

<script>
    Split(['#left-stack', '#right-stack'], { sizes: [70, 30], gutterSize: 4 });
    for(let i=0; i<100; i++) document.getElementById('side-strip').innerHTML += '<div class="btn-cell"></div>';
    function toggleAISet(show) { document.getElementById('ai-modular-setup').style.display = show ? 'flex' : 'none'; }

    function saveData() {
        localStorage.setItem('gemini_api_key', document.getElementById('api-field-input').value);
        document.getElementById('terminal-out').innerHTML += "\\n> CONFIG_SAVED";
        toggleAISet(false);
    }

    async function callGemini(promptText) {
        const apiKey = localStorage.getItem('gemini_api_key');
        const model = document.getElementById('version-select').value;
        const chatWindow = document.getElementById('ai-chat');
        const terminal = document.getElementById('terminal-out');
        if (!apiKey) { chatWindow.innerHTML += "<br>[ERROR]: NO KEY"; return; }

        try {
            terminal.innerHTML += "\\n> CALLING " + model;
            const resp = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ contents: [{ parts: [{ text: promptText }] }] })
            });
            const data = await resp.json();
            if (data.error) throw new Error(data.error.message);
            chatWindow.innerHTML += `<br><br><span style="color:#00ff00">[${model}]:</span> ` + data.candidates[0].content.parts[0].text;
            terminal.innerHTML += "\\n> 200 OK";
            chatWindow.scrollTop = chatWindow.scrollHeight;
        } catch (err) {
            chatWindow.innerHTML += `<br><span style="color:red">[ERR]: ${err.message}</span>`;
        }
    }

    document.getElementById('user-prompt').addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            const text = this.value.trim();
            if(text) {
                document.getElementById('ai-chat').innerHTML += "<br><br><span style='color:#800080'>[USER]:</span> " + text;
                callGemini(text);
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
