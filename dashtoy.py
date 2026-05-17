import streamlit as st
import streamlit.components.v1 as components
import json
import os

st.set_page_config(layout="wide", page_title="CAD Designer Pro")

st.markdown("""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
.stApp { background:#000 !important; overflow:hidden !important; }
.block-container{
padding:0rem !important;
max-width:100% !important;
height:100vh !important;
overflow:hidden !important;
}
</style>
""", unsafe_allow_html=True)

# Cloud persistence handler: reads common configuration matrix
def load_cloud_config():
    if os.path.exists("comutoy.json"):
        try:
            with open("comutoy.json", "r") as f:
                return json.load(f)
        except:
            pass
    return {
        "gemini_api_key": "",
        "gemini_model": "gemini-2.5-flash",
        "gemini_url": "https://generativelanguage.googleapis.com/v1beta/models/"
    }

cfg = load_cloud_config()

# Read values into safe Python variables to avoid JavaScript collision errors
api_key_val = cfg.get('gemini_api_key', '')
model_val = cfg.get('gemini_model', 'gemini-2.5-flash')
url_val = cfg.get('gemini_url', 'https://generativelanguage.googleapis.com/v1beta/models/')

cad_app_html = """
<script src="https://cdnjs.cloudflare.com/ajax/libs/split.js/1.6.0/split.min.js"></script>

<style>
html, body {
margin:0; padding:0; height:100%; width:100%;
overflow:hidden !important; background:#000;
font-family:'Segoe UI',Tahoma,sans-serif; color:white;
}

.master-container{
display:flex; flex-direction:column;
height:100vh; width:100vw; background:#000;
border:2px solid #d3d3d3; box-sizing:border-box;
position:relative;
}

#ai-modular-setup{
position:absolute; top:10%; left:15%; width:70%; height:75%;
background:#000; border:2px solid #00ff00; z-index:9999;
display:none; flex-direction:column;
box-shadow:0 0 50px rgba(0,255,0,0.3);
}

.ai-setup-header{
background:#0a1a0a; border-bottom:1px solid #00ff00;
padding:10px; display:flex; justify-content:space-between;
color:#00ff00; font-family:monospace; font-weight:bold;
align-items:center;
}

.ai-header-controls{display:flex; gap:10px; align-items:center;}
.ai-setup-body{display:flex; flex:1; overflow:hidden;}
.ai-setup-sidebar{
width:30%; border-right:1px solid #00ff00;
padding:10px; background:#050505; overflow-y:auto;
}

.ai-setup-content{
width:70%; padding:25px; color:#00ff00;
font-family:monospace; display:flex;
flex-direction:column; gap:20px;
overflow-y:auto;
}

.ai-tool-item{
padding:12px; border:1px solid #004400;
margin-bottom:8px; cursor:pointer; font-size:12px;
transition:0.2s;
}
.ai-tool-item:hover{border-color:#00ff00; background:#0a2a0a;}
.ai-tool-item.active{background:#00ff00; color:#000; font-weight:bold;}

.ai-select{
background:#000; border:1px solid #00ff00; color:#00ff00;
padding:10px; width:100%; outline:none; cursor:pointer;
font-family:monospace; appearance:none;
}

.ai-input{
background:#000; border:1px solid #00ff00; color:#00ff00;
padding:10px; width:100%; outline:none; box-sizing:border-box;
}

.title-action-btn{
padding:2px 12px; font-size:10px; cursor:pointer;
border:1px solid #00ff00; background:#000; color:#00ff00;
font-family:monospace; text-transform:uppercase;
}
.title-action-btn:hover{background:#00ff00; color:#000;}
.title-action-btn.close{border-color:#fff; color:#fff;}

.window-title-bar{
background:#1a1a1a; color:#888; height:30px; flex-shrink:0;
display:flex; align-items:center; justify-content:space-between;
padding:0 10px; font-size:12px; border-bottom:1px solid #333;
}

#dynamic-zone{
display:flex; flex-direction:row; flex:1; min-height:0; width:100%;
}

.fixed-right-strip{
width:65px; border-left:1px solid #333;
display:grid; grid-template-columns:1fr 1fr;
grid-auto-rows:min-content; gap:2px; padding:5px;
background:#000; overflow-y:scroll;
}

.btn-cell{
aspect-ratio:1/1; width:20px; height:20px; background:#e1e1e1;
color:#000; border-top:2px solid #fff; border-left:2px solid #fff;
border-right:2px solid #707070; border-bottom:2px solid #707070;
cursor:pointer; display:flex; align-items:center;
justify-content:center; box-sizing:border-box; flex-shrink:0;
font-size:9px; font-weight:bold; font-family:sans-serif;
}

.btn-cell:active{
border-top:2px solid #707070; border-left:2px solid #707070;
border-right:2px solid #fff; border-bottom:2px solid #fff;
background:#bebebe;
}

.pane{
background:#000 !important; border:1px solid #333 !important;
overflow:hidden; display:flex; align-items:center;
justify-content:center; box-sizing:border-box;
}

.gutter{background:#444 !important;}

.fixed-footer{
height:64px; display:flex; flex-direction:row;
border-top:2px solid #333; background:#000;
flex-shrink:0; align-items:flex-end;
padding:0px 4px 2px 4px;
}

.footer-left-content{
flex:1; display:flex; height:100%;
align-items:center; padding-left:10px;
}

.selection-b-container{width:130px; height:62px; margin-left:5px;}
.selection-a-stack{
display:flex; flex-direction:column; gap:1px;
width:130px; margin-left:5px;
}

.footer-palette-grid{
display:grid; grid-template-columns:repeat(6,20px);
grid-template-rows:repeat(3,20px); gap:1px; margin-left:8px;
}

.dropup{
position:relative; width:100%; height:20px;
background:#e1e1e1; color:#000; border:1px solid #707070;
display:flex; align-items:center; justify-content:space-between;
padding:0 5px; cursor:pointer; font-size:9px;
box-sizing:border-box;
}

.dropup.tall{height:62px;}

.dropup-content{
display:none; position:absolute; bottom:100%; left:-1px;
background:#f0f0f0; min-width:140px;
border:1px solid #707070; z-index:1000;
}

.dropup.active .dropup-content{display:block;}

.dropup-content a{
color:#000; padding:6px; text-decoration:none;
display:block; border-bottom:1px solid #ccc; font-size:10px;
}

.text-main{
color:#b22222; font-size:1.4vw; font-weight:bold;
text-align:center; width:100%; height:100%;
overflow:auto; display:flex; flex-direction:column;
align-items:center; justify-content:center;
}

.ai-text-area{
width:100%; height:100%; padding:10px; color:#00ff00;
font-family:'Consolas',monospace; font-size:13px;
overflow-y:auto; text-align:left;
}

.user-input-area{
width:100%; height:100%; background:transparent;
border:none; color:#800080; padding:10px;
font-family:'Consolas',monospace; outline:none;
resize:none; font-weight:bold;
}

.cmd-text{
width:100%; height:100%; color:#0f0;
font-family:monospace; font-size:11px;
padding:5px; overflow-y:auto; white-space:pre-wrap;
}

/* --- REPO SUB-PANEL EMBEDDED HUD MATRIX STYLES --- */
.repo-overlay-panel {
width:100%; height:100%; background:#000; padding:20px;
box-sizing:border-box; display:flex; flex-direction:column;
font-family:monospace; color:#00ff00; text-align:left;
}
.repo-nav-row { display:flex; gap:10px; margin-bottom:15px; }
.repo-nav-btn {
flex:1; background:#000; color:#00ff00; border:2px solid #00ff00;
padding:10px; font-weight:bold; cursor:pointer; border-radius:4px;
font-family:monospace; text-align:center;
}
.repo-nav-btn:hover { background:#003300; }
.repo-inner-card {
flex:1; border:1px solid #333; background:#050505;
padding:15px; border-radius:4px; overflow-y:auto; margin-bottom:15px;
}
.repo-field-group { margin-bottom:12px; display:flex; flex-direction:column; gap:5px; }
.repo-field-label { font-size:11px; color:#888; text-transform:uppercase; }
.repo-select-input {
background:#000; border:1px solid #00ff00; color:#00ff00; padding:8px;
font-family:monospace; outline:none;
}
.repo-txt-input {
background:#000; border:1px solid #00ff00; color:#00ff00; padding:8px;
font-family:monospace; outline:none; box-sizing:border-box; width:100%;
}
.repo-check-row { display:flex; align-items:center; gap:10px; margin-bottom:8px; }
.repo-check-input { accent-color:#00ff00; cursor:pointer; }
.repo-footer-row { display:flex; justify-content:center; gap:20px; align-items:center; }
.repo-action-commit {
background:#00ff00; color:#000; border:none; padding:8px 20px;
font-weight:bold; cursor:pointer; font-family:monospace; border-radius:4px;
}
.repo-action-commit:hover { background:#00cc00; }
.repo-action-close {
background:#000; color:#fff; border:1px solid #fff; padding:8px 20px;
font-weight:bold; cursor:pointer; font-family:monospace; border-radius:4px;
}
.repo-action-close:hover { background:#222; }
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

<div class="ai-setup-sidebar" id="tool-list">
<div class="ai-tool-item active">GOOGLE GEMINI</div>
<div class="ai-tool-item">LUVIA AI</div>
<div class="ai-tool-item">FLUX.AI</div>
<div class="ai-tool-item">KICAD</div>
<div class="ai-tool-item">QUILTER</div>
<div class="ai-tool-item">NTOP / FUSION</div>
</div>

<div class="ai-setup-content">

<div style="font-size:20px;border-bottom:2px solid #004400;padding-bottom:5px;color:#fff;">
TOOL: <span id="tool-name">Google Gemini</span>
</div>

<div>
<label>AVAILABLE VERSIONS (DYNAMIC):</label>
<select class="ai-select" id="version-select">
<option value="gemini-2.5-flash">Gemini 2.5 Flash</option>
<option value="gemini-2.5-pro">Gemini 2.5 Pro</option>
<option value="gemini-2.5-flash-lite">Gemini 2.5 Flash-Lite</option>
</select>
</div>

<div>
<label>CORE FUNCTION (OUTPUT):</label>
<select class="ai-select">
<option>Multi-modal Reasoning</option>
<option>MPN Text / Sourcing only</option>
</select>
</div>

<div>
<label id="key-label">API KEY / LOCAL PATH:</label>
<input type="password" id="api-field-input" class="ai-input" placeholder="ENTER ACCESS KEY OR PATH...">
</div>

<div>
<label>API URL:</label>
<input type="text" id="url-input" class="ai-input" value="https://generativelanguage.googleapis.com/v1beta/models/">
</div>

</div>
</div>
</div>

<div class="window-title-bar">
<div>CAD DESIGNER PRO</div>
<div><span>−</span><span style="margin:0 10px;">❐</span><span>×</span></div>
</div>

<div id="dynamic-zone">

<div id="split-container" style="display:flex;flex:1;width:100%;">

<div id="left-stack" style="display:flex;flex-direction:column;width:70%;">
<div id="cad-pane" class="pane text-main">
<div id="visual-monitor" style="color:#444;font-size:12px;font-family:monospace;width:100%;height:100%;display:flex;align-items:center;justify-content:center;">
[ IDLE: AWAITING CIRCUIT REQUEST ]
</div>
</div>

<div id="cmd-pane" class="pane" style="justify-content:flex-start;align-items:flex-start;">
<div id="terminal-out" class="cmd-text">>_ SYSTEM INITIALIZED</div>
</div>
</div>

<div id="right-stack" style="display:flex;flex-direction:column;width:30%;">
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
<span style="color:#008000;font-size:11px;margin-right:20px;">READY</span>
<span style="color:#0000ff;font-size:11px;">SYSTEM STATUS: ONLINE</span>
</div>

<div id="foot-palette" class="footer-palette-grid"></div>

<div class="selection-a-stack">
<div class="dropup"><span>File</span><span>▲</span></div>
<div class="dropup"><span>Tools</span><span>▲</span></div>
<div class="dropup"><span>View</span><span>▲</span></div>
</div>

<div class="selection-b-container">
<div class="dropup tall" onclick="toggleAISet(true)">
<span>AI-SET</span><span>▲</span>
</div>
</div>
</div>

</div>

<script>
// Injection of cloud parameter variables safely passed down from Streamlit configuration definitions
const cloudApiKey = """ + f'"{api_key_val}"' + """ ;
const cloudModel = """ + f'"{model_val}"' + """ ;
const cloudUrl = """ + f'"{url_val}"' + """ ;

if(cloudApiKey) {
    localStorage.setItem('gemini_api_key', cloudApiKey);
    localStorage.setItem('gemini_model', cloudModel);
    localStorage.setItem('gemini_url', cloudUrl);
}

Split(['#left-stack','#right-stack'],{sizes:[70,30],gutterSize:4});
Split(['#cad-pane','#cmd-pane'],{direction:'vertical',sizes:[80,20],gutterSize:4});
Split(['#ai-output','#ai-input'],{direction:'vertical',sizes:[50,50],gutterSize:4});

// MODIFIED: Generates top 2 buttons uniquely and preserves the other 98 cells exactly
for(let i=0;i<100;i++){
    if(i === 0) {
        document.getElementById('side-strip').innerHTML += '<div class="btn-cell" id="btn-repo-trigger" onclick="toggleRepoSubPanel()">RP</div>';
    } else if(i === 1) {
        document.getElementById('side-strip').innerHTML += '<div class="btn-cell" id="btn-fs-trigger">FS</div>';
    } else {
        document.getElementById('side-strip').innerHTML += '<div class="btn-cell"></div>';
    }
}

for(let i=0;i<18;i++){
    document.getElementById('foot-palette').innerHTML += '<div class="btn-cell"></div>';
}

// Global active sub-panel tracking variable
let activeRepoTab = "storage";

function toggleRepoSubPanel() {
    const monitor = document.getElementById('visual-monitor');
    const terminal = document.getElementById('terminal-out');
    
    // Check if repo overlay panel is already rendered on screen
    const existingPanel = document.getElementById('repo-embedded-panel');
    
    if(existingPanel) {
        // Toggle view back to default idle state
        monitor.innerHTML = '<div id="visual-monitor" style="color:#444;font-size:12px;font-family:monospace;">[ IDLE: AWAITING CIRCUIT REQUEST ]</div>';
        terminal.innerHTML += "\\n> DEACTIVATED: REPO SET VIEW OVERLAY CLOSING";
    } else {
        // Inject clean structural HTML payload inside the central pane window canvas block
        monitor.innerHTML = `
            <div class="repo-overlay-panel" id="repo-embedded-panel">
                <div class="repo-nav-row">
                    <div class="repo-nav-btn" onclick="switchRepoTab('storage')">STORAGE</div>
                    <div class="repo-nav-btn" onclick="switchRepoTab('backup')">BACK UP</div>
                    <div class="repo-nav-btn" onclick="switchRepoTab('milestone')">MILESTONE</div>
                </div>
                <div class="repo-inner-card" id="repo-dynamic-content">
                    </div>
                <div class="repo-footer-row">
                    <button class="repo-action-commit" onclick="commitRepoConfig()">[ COMMIT CHANGES ]</button>
                    <button class="repo-action-close" onclick="toggleRepoSubPanel()">CLOSE</button>
                </div>
            </div>
        `;
        terminal.innerHTML += "\\n> INITIALIZED: REPO SET SUBSYSTEM DASHBOARD MOUNTED";
        switchRepoTab(activeRepoTab);
    }
}

function switchRepoTab(tabName) {
    activeRepoTab = tabName;
    const contentArea = document.getElementById('repo-dynamic-content');
    if(!contentArea) return;
    
    if(tabName === 'storage') {
        contentArea.innerHTML = `
            <div style="font-size:14px; color:#fff; margin-bottom:10px; font-weight:bold;">📁 PRIMARY STORAGE ROUTING DEFINITION</div>
            <div class="repo-field-group">
                <label class="repo-field-label">Cloud Target Platform Instance:</label>
                <select class="repo-select-input" id="repo-p-provider">
                    <option value="gdrive">Google Drive Workspace Mirror</option>
                    <option value="dropbox">Dropbox Sync Engine</option>
                    <option value="local">Isolated Local Hard-Path Matrix</option>
                </select>
            </div>
            <div class="repo-field-group">
                <label class="repo-field-label">Workspace Local Directory Target Road Map (D:/):</label>
                <input type="text" class="repo-txt-input" id="repo-l-path" value="D:/Project_Mothership/temp_workspace">
            </div>
            <div class="repo-field-group">
                <label class="repo-field-label">Cache Scratchpad Temporal Subfolder:</label>
                <input type="text" class="repo-txt-input" id="repo-c-path" value="D:/Project_Mothership/temp_workspace/cache">
            </div>
        `;
    } else if(tabName === 'backup') {
        contentArea.innerHTML = `
            <div style="font-size:14px; color:#fff; margin-bottom:10px; font-weight:bold;">🛡️ COLD SYNC & REDUNDANCY MATRICES</div>
            <div class="repo-field-group">
                <label class="repo-field-label">Redundant Cold Backup Target Vault:</label>
                <select class="repo-select-input" id="repo-b-provider">
                    <option value="dropbox">Dropbox Core System Repository</option>
                    <option value="gdrive">Google Drive Cloud Instance</option>
                    <option value="s3">AWS S3 Glacial Server Segment</option>
                </select>
            </div>
            <div class="repo-field-group">
                <label class="repo-field-label">Automated Mirror Interval Trigger Frequency (Hours):</label>
                <input type="range" min="1" max="24" value="6" style="width:100%; accent-color:#00ff00;" id="repo-sync-slider" oninput="document.getElementById('slider-val-read').innerText = this.value + ' Hours'">
                <span id="slider-val-read" style="font-size:11px; color:#00ff00;">6 Hours</span>
            </div>
        `;
    } else if(tabName === 'milestone') {
        contentArea.innerHTML = `
            <div style="font-size:14px; color:#fff; margin-bottom:10px; font-weight:bold;">🎯 FIXED WORKFLOW MATRIX TARGET GATES</div>
            <div class="repo-check-row"><input type="checkbox" class="repo-check-input" id="m1" checked><label>Milestone 1: Web Component Match API (Luvia AI Component API)</label></div>
            <div class="repo-check-row"><input type="checkbox" class="repo-check-input" id="m2" checked><label>Milestone 2: Netlist Capture Rules (Flux.ai Structural Schema Check)</label></div>
            <div class="repo-check-row"><input type="checkbox" class="repo-check-input" id="m3" checked><label>Milestone 3: Headless Wave Simulator Check (KiCad Local SPICE Engine)</label></div>
            <div class="repo-check-row"><input type="checkbox" class="repo-check-input" id="m4" checked><label>Milestone 4: Trace Georouting Compliance (Quilter CAM Engine Router)</label></div>
            <div class="repo-check-row"><input type="checkbox" class="repo-check-input" id="m5"><label>Milestone 5: 3D Physics Collision Check (nTop Structural Integrity)</label></div>
            <div style="margin-top:12px; font-size:11px; color:#888;">AUTOMATION INTERCEPT PATTERN SETTINGS:</div>
            <div class="repo-check-row" style="margin-top:5px;"><input type="radio" name="auto-rule" value="full" checked id="r-full"><label>Fully Automated Conference Pipeline Process</label></div>
            <div class="repo-check-row"><input type="radio" name="auto-rule" value="hitl" id="r-hitl"><label>Human Decision Checkpoint Verification Halt Mode</label></div>
        `;
    }
}

function commitRepoConfig() {
    const terminal = document.getElementById('terminal-out');
    const chatWindow = document.getElementById('ai-chat');
    
    // Scrape live values depending on which tab is open for safe persistence initialization
    if(document.getElementById('repo-p-provider')) {
        localStorage.setItem('repo_primary_provider', document.getElementById('repo-p-provider').value);
        localStorage.setItem('repo_local_path', document.getElementById('repo-l-path').value);
        localStorage.setItem('repo_cache_path', document.getElementById('repo-c-path').value);
    }
    
    terminal.innerHTML += "\\n> CONFIG_SAVE: WORKFLOW GUIDELINES ANCHORED INTO MEMORY MATRIX LAYER SUCCESSFULLY";
    chatWindow.innerHTML += "<br><span style='color:#00ff00'>[SYSTEM]:</span> REPO SET VARIABLES REGISTERED AND CACHED.";
    toggleRepoSubPanel();
}

function toggleAISet(show){
document.getElementById('ai-modular-setup').style.display = show ? 'flex':'none';
}

function saveData(){
const apiKey = document.getElementById('api-field-input').value;
const model = document.getElementById('version-select').value;
const apiUrl = document.getElementById('url-input').value;

localStorage.setItem('gemini_api_key', apiKey);
localStorage.setItem('gemini_model', model);
localStorage.setItem('gemini_url', apiUrl);

document.getElementById('ai-chat').innerHTML += "<br><br><span style='color:#00ff00'>[SYSTEM]:</span> CONFIG SAVED TEMPORARILY.";
document.getElementById('terminal-out').innerHTML += "\\n> CONFIG_SAVE: SUCCESS";
toggleAISet(false);
}

async function callGemini(promptText){

const apiKey = localStorage.getItem('gemini_api_key') || cloudApiKey;
const model = localStorage.getItem('gemini_model') || cloudModel || 'gemini-2.5-flash';
const apiUrl = localStorage.getItem('gemini_url') || cloudUrl || 'https://generativelanguage.googleapis.com/v1beta/models/';

const chatWindow = document.getElementById('ai-chat');
const terminal = document.getElementById('terminal-out');

if(!apiKey){
chatWindow.innerHTML += "<br><span style='color:red'>[ERROR]: NO API KEY FOUND. OPEN AI-SET.</span>";
return;
}

try{

terminal.innerHTML += "\\n> API_CALL: HANDSHAKE STARTED";

const response = await fetch(apiUrl + model + ":generateContent?key=" + apiKey, {
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({
contents:[{parts:[{text:promptText}]}]
})
});

const data = await response.json();

if(
data.candidates &&
data.candidates[0] &&
data.candidates[0].content &&
data.candidates[0].content.parts &&
data.candidates[0].content.parts[0]
){
const aiText = data.candidates[0].content.parts[0].text || "No text returned.";

chatWindow.innerHTML += "<br><span style='color:#00ff00'>[GEMINI]:</span> " + aiText;
terminal.innerHTML += "\\n> API_RESPONSE: SUCCESS_LOADED";
chatWindow.scrollTop = chatWindow.scrollHeight;

}else{
chatWindow.innerHTML += "<br><span style='color:red'>[API ERROR]: " + JSON.stringify(data) + "</span>";
terminal.innerHTML += "\\n> API_RESPONSE: UNKNOWN_FORMAT";
}

}catch(err){
chatWindow.innerHTML += "<br><span style='color:red'>[API ERROR]: CONNECTION FAILED.</span>";
terminal.innerHTML += "\\n> API_ERROR: CHECK KEY/MODEL";
}
}

const promptInput = document.getElementById('user-prompt');

promptInput.addEventListener('keydown',function(e){

if(e.key==='Enter' && !e.shiftKey){
e.preventDefault();

const text = promptInput.value.trim();

if(text !== ''){

document.getElementById('ai-chat').innerHTML += "<br><br><span style='color:#800080'>[USER]:</span> " + text;
document.getElementById('terminal-out').innerHTML += "\\n> DISPATCH: " + text.toUpperCase();

callGemini(text);

promptInput.value='';
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
