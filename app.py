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
        .block-container { padding: 0rem !important; max-width: 100% !important; height: 100vh !important; overflow: hidden !important; }
    </style>
""", unsafe_allow_html=True)

# 3. Native UI Application
cad_app_html = """
<script src="https://cdnjs.cloudflare.com/ajax/libs/split.js/1.6.0/split.min.js"></script>
<style>
    html, body { margin: 0; padding: 0; height: 100%; width: 100%; overflow: hidden !important; background-color: #000; font-family: 'Segoe UI', sans-serif; color: white; }
    .master-container { display: flex; flex-direction: column; height: 100vh; width: 100vw; background: #000; border: 2px solid #d3d3d3; box-sizing: border-box; position: relative; }
    #ai-modular-setup { position: absolute; top: 10%; left: 15%; width: 70%; height: 75%; background: #000; border: 2px solid #00ff00; z-index: 9999; display: none; flex-direction: column; }
    .ai-setup-header { background: #0a1a0a; border-bottom: 1px solid #00ff00; padding: 10px; display: flex; justify-content: space-between; color: #00ff00; font-family: monospace; }
    .ai-setup-body { display: flex; flex: 1; overflow: hidden; }
    .ai-setup-sidebar { width: 30%; border-right: 1px solid #00ff00; padding: 10px; background: #050505; }
    .ai-setup-content { width: 70%; padding: 25px; color: #00ff00; font-family: monospace; display: flex; flex-direction: column; gap: 20px; }
    .ai-tool-item { padding: 12px; border: 1px solid #004400; margin-bottom: 8px; cursor: pointer; font-size: 12px; }
    .ai-tool-item.active { background: #00ff00; color: #000; font-weight: bold; }
    .ai-select, .ai-input { background: #000; border: 1px solid #00ff00; color: #00ff00; padding: 10px; width: 100%; outline: none; font-family: monospace; }
    .title-action-btn { padding: 2px 12px; font-size: 10px; cursor: pointer; border: 1px solid #00ff00; background: #000; color: #00ff00; }
    .window-title-bar { background: #1a1a1a; color: #888; height: 30px; display: flex; align-items: center; justify-content: space-between; padding: 0 10px; font-size: 12px; border-bottom: 1px solid #333; }
    #dynamic-zone { display: flex; flex-direction: row; flex: 1; min-height: 0; width: 100%; }
    .fixed-right-strip { width: 65px; border-left: 1px solid #333; display: grid; grid-template-columns: 1fr 1fr; grid-auto-rows: min-content; gap: 2px; padding: 5px; background: #000; overflow-y: scroll; }
    .btn-cell { aspect-ratio: 1 / 1; width: 20px; height: 20px; background: #e1e1e1; border: 2px solid #707070; box-sizing: border-box; }
    .pane { background: #000; border: 1px solid #333; overflow: hidden; display: flex; box-sizing: border-box; }
    .fixed-footer { height: 64px; display: flex; border-top: 2px solid #333; background: #000; align-items: flex-end; padding: 0 4px 2px 4px; }
    .footer-palette-grid { display: grid; grid-template-columns: repeat(6, 20px); gap: 1px; margin-left: 8px; }
    .dropup { width: 130px; height: 20px; background: #e1e1e1; color: #000; border: 1px solid #707070; padding: 0 5px; cursor: pointer; font-size: 9px; }
    .ai-text-area { width: 100%; height: 100%; padding: 10px; color: #00ff00; font-family: monospace; overflow-y: auto; text-align: left; }
    .user-input-area { width: 100%; height: 100%; background: transparent; border: none; color: #800080; padding: 10px; font-family: monospace; outline: none; resize: none; font-weight: bold; }
    .cmd-text { width: 100%; height: 100%; color: #0f0; font-family: monospace; font-size: 11px; padding: 5px; overflow-y: auto; text-align: left; }
</style>

<div class="master-container">
    <div id="ai-modular-setup">
        <div class="ai-setup-header">
            <span>[ SYSTEM AI-SET : TOOL CONFIGURATION ]</span>
            <div><button class="title-action-btn" onclick="saveData()">SAVE</button> <button class="title-action-btn" onclick="toggleAISet(false)">[X]</button></div>
        </div>
        <div class="ai-setup-body">
            <div class="ai-setup-sidebar"><div class="ai-tool-item active">GOOGLE GEMINI</div></div>
            <div class="ai-setup-content">
                <label>VERSION:</label><select class="ai-select" id="version-select"><option>Gemini 3 Flash</option></select>
                <label>API KEY:</label><input type="password" id="api-field-input" class="ai-input" placeholder="PASTE KEY...">
            </div>
        </div>
    </div>

    <div class="window-title-bar"><div>CAD DESIGNER PRO</div></div>
    <div id="dynamic-zone">
        <div id="left-stack" style="width:70%; display:flex; flex-direction:column;">
            <div id="cad-pane" class="pane" style="height:80%; display:block; padding:20px;">[ VISUAL MONITOR ]</div>
            <div id="cmd-pane" class="pane" style="height:20%;"><div id="terminal-out" class="cmd-text">>_ SYSTEM READY</div></div>
        </div>
        <div id="right-stack" style="width:30%; display:flex; flex-direction:column;">
            <div id="ai-output" class="pane" style="height:50%;"><div id="ai-chat" class="ai-text-area">AI TEXT REPLYING WINDOW</div></div>
            <div id="ai-input" class="pane" style="height:50%;"><textarea id="user-prompt" class="user-input-area" placeholder="TYPE HERE..."></textarea></div>
        </div>
        <div class="fixed-right-strip" id="side-strip"></div>
    </div>
    <div class="fixed-footer">
        <div id="foot-palette" class="footer-palette-grid"></div>
        <div class="dropup" style="height:62px;" onclick="toggleAISet(true)">AI-SET ▲</div>
    </div>
</div>

<script>
    Split(['#left-stack', '#right-stack'], { sizes: [70, 30], gutterSize: 4 });
    Split(['#cad-pane', '#cmd-pane'], { direction: 'vertical', sizes: [80, 20], gutterSize: 4 });
    Split(['#ai-output', '#ai-input'], { direction: 'vertical', sizes: [50, 50], gutterSize: 4 });
    for(let i=0; i<100; i++) document.getElementById('side-strip').innerHTML += '<div class="btn-cell"></div>';
    function toggleAISet(s) { document.getElementById('ai-modular-setup').style.display = s ? 'flex' : 'none'; }
    function saveData() { 
        localStorage.setItem('gemini_api_key', document.getElementById('api-field-input').value);
        document.getElementById('terminal-out').innerHTML += "\\n> GOOGLE GEMINI: CONFIGURATION SAVED";
        toggleAISet(false); 
    }
    document.getElementById('user-prompt').addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            const t = this.value;
            document.getElementById('ai-chat').innerHTML += "<div style='color:#800080; margin-top:10px;'>[USER]: " + t + "</div>";
            document.getElementById('terminal-out').innerHTML += "\\n> GEMINI DISPATCH: " + t.toUpperCase();
            this.value = "";
            setTimeout(() => {
                document.getElementById('ai-chat').innerHTML += "<div style='color:#00ff00'>[GEMINI]: Designing architecture for: " + t + "...</div>";
                document.getElementById('cad-pane').innerHTML = "[ BLOCK DIAGRAM GENERATING ]";
            }, 500);
        }
    });
</script>
"""
components.html(cad_app_html, height=0)
st.components.v1.html("""<script>window.parent.document.querySelector('iframe').style.height = '94vh';</script>""", height=0)
