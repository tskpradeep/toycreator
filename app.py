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
    .tool-note { font-size: 11px; color: #008800; border-left: 2px solid #00ff00; padding-left: 10px; margin-top: 5px; }

    .title-action-btn { 
        padding: 2px 12px; font-size: 10px; cursor: pointer; 
        border: 1px solid #00ff00; background: #000; color: #00ff00;
        font-family: monospace; text-transform: uppercase;
    }
    .title-action-btn:hover { background: #00ff00; color: #000; }
    .title-action-btn.close { border-color: #fff; color: #fff; }

    .window-title-bar { background: #1a1a1a; color: #888; height: 30px; flex-shrink: 0; display: flex; align-items: center; justify-content: space-between; padding: 0 10px; font-size: 12px; border-bottom: 1px solid #333; }
    #dynamic-zone { display: flex; flex-direction: row; flex: 1; min-height: 0; width: 100%; }
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
    .dropup-content a { color: #000; padding: 6px; text-decoration: none; display: block; border-bottom: 1px solid #ccc; font-size: 10px; }
    .text-main { color: #b22222; font-size: 1.4vw; font-weight: bold; text-align: center; width:100%; height:100%; overflow:auto; display:flex; flex-direction:column; align-items:center; justify-content:center;}
    .ai-text-area { width: 100%; height: 100%; padding: 10px; color: #00ff00; font-family: 'Consolas', monospace; font-size: 13px; overflow-y: auto; text-align: left; }
    .user-input-area { width: 100%; height: 100%; background: transparent; border: none; color: #800080; padding: 10px; font-family: 'Consolas', monospace; outline: none; resize: none; font-weight: bold; }
    .cmd-text { width: 100%; height: 100%; color: #0f0; font-family: monospace; font-size: 11px; padding: 5px; overflow-y: auto; white-space: pre-wrap; }
</style>

<div class="master-container">

<div id="ai-modular-setup">
<div class="ai-setup-header">
<span>[ SYSTEM AI-SET : TOOL CONFIGURATION ]</span>
<div class="ai-header-controls">
<button class="title-action-btn" onclick="saveData()">SAVE</button>
<button class="title-action-btn close" onclick="toggleAISet(false)">[ X ]</button>
</div>
</div>

<div class="ai-setup-body">
<div class="ai-setup-sidebar">
<div class="ai-tool-item active">GOOGLE GEMINI</div>
</div>

<div class="ai-setup-content">
<div style="font-size:20px;color:#fff;">TOOL: Google Gemini</div>

<label>API URL:</label>
<input id="url-input" class="ai-input" value="https://generativelanguage.googleapis.com/v1beta/models/">

<label>MODEL:</label>
<select class="ai-select" id="version-select">
<option value="gemini-2.5-flash">gemini-2.5-flash</option>
<option value="gemini-2.5-pro">gemini-2.5-pro</option>
<option value="gemini-2.5-flash-lite">gemini-2.5-flash-lite</option>
</select>

<label>API KEY:</label>
<input type="password" id="api-field-input" class="ai-input">
</div>
</div>
</div>

<div class="window-title-bar">
<div>CAD DESIGNER PRO</div>
<div>×</div>
</div>

<div id="dynamic-zone">
<div id="split-container" style="display:flex; flex:1; width:100%;">
<div id="left-stack" style="display:flex; flex-direction:column; width:70%;">
<div id="cad-pane" class="pane text-main">LEFT AREA</div>
<div id="cmd-pane" class="pane"><div id="terminal-out" class="cmd-text">>_ SYSTEM INITIALIZED</div></div>
</div>

<div id="right-stack" style="display:flex; flex-direction:column; width:30%;">
<div id="ai-output" class="pane"><div id="ai-chat" class="ai-text-area">AI TEXT REPLYING WINDOW</div></div>
<div id="ai-input" class="pane"><textarea id="user-prompt" class="user-input-area" placeholder="TYPE HERE..."></textarea></div>
</div>
</div>
<div class="fixed-right-strip" id="side-strip"></div>
</div>

<div class="fixed-footer">
<div class="footer-left-content">READY</div>
<div class="selection-b-container">
<div class="dropup tall" onclick="toggleAISet(true)"><span>AI-SET</span></div>
</div>
</div>

</div>

<script>
Split(['#left-stack', '#right-stack'], { sizes: [70, 30], gutterSize: 4 });
Split(['#ai-output', '#ai-input'], { direction: 'vertical', sizes: [50, 50], gutterSize: 4 });

function toggleAISet(show){
document.getElementById('ai-modular-setup').style.display = show ? 'flex':'none';
}

function saveData(){
localStorage.setItem('gemini_api_key',document.getElementById('api-field-input').value);
localStorage.setItem('gemini_model',document.getElementById('version-select').value);
localStorage.setItem('gemini_url',document.getElementById('url-input').value);
toggleAISet(false);
}

async function callGemini(promptText){
const apiKey = localStorage.getItem('gemini_api_key');
const model = localStorage.getItem('gemini_model') || 'gemini-2.5-flash';
const apiUrl = localStorage.getItem('gemini_url') || 'https://generativelanguage.googleapis.com/v1beta/models/';
const chatWindow = document.getElementById('ai-chat');

const url = `${apiUrl}${model}:generateContent?key=${apiKey}`;

const data = {
contents:[{parts:[{text:promptText}]}]
};

try{
const response = await fetch(url,{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify(data)
});

const result = await response.json();

if(result.candidates){
const reply = result.candidates[0].content.parts[0].text;
chatWindow.innerHTML += "<br><br><span style='color:#800080'>[USER]:</span> "+promptText;
chatWindow.innerHTML += "<br><span style='color:#00ff00'>[AI]:</span> "+reply;
chatWindow.scrollTop = chatWindow.scrollHeight;
}else{
chatWindow.innerHTML += "<br><span style='color:red'>API ERROR</span>";
}
}catch(e){
chatWindow.innerHTML += "<br><span style='color:red'>CONNECTION FAILED</span>";
}
}

document.getElementById("user-prompt").addEventListener("keydown",function(e){
if(e.key==="Enter" && !e.shiftKey){
e.preventDefault();
const text=this.value.trim();
if(text!==""){
callGemini(text);
this.value="";
}
}
});
</script>
"""

components.html(cad_app_html, height=0)

st.components.v1.html(
"""
<script>
window.parent.document.querySelector('iframe').style.height='94vh';
</script>
""",
height=0
)
