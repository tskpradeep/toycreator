import streamlit as st
import streamlit.components.v1 as components
import json
import os

st.set_page_config(layout="wide", page_title="CAD AI-SET Suite")

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

def get_current_values():
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

current_cfg = get_current_values()

# Load current configuration values into safe python variables
p_key = current_cfg.get('gemini_api_key','')
p_model = current_cfg.get('gemini_model','gemini-2.5-flash')
p_url = current_cfg.get('gemini_url','https://generativelanguage.googleapis.com/v1beta/models/')

ai_set_html = """
<style>
html, body {
margin:0; padding:0; height:100%; width:100%;
overflow:hidden !important; background:#000;
font-family:'Segoe UI',Tahoma,sans-serif; color:white;
}
.master-container{
display:flex; flex-direction:column;
height:100vh; width:100vw; background:#000;
box-sizing:border-box; position:relative;
}
#ai-modular-setup{
width:100%; height:100%;
background:#000; border:2px solid #00ff00;
display:flex; flex-direction:column;
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
</style>

<div class="master-container">
<div id="ai-modular-setup">
<div class="ai-setup-header">
<span>[ SYSTEM AI-SET : TOOL CONFIGURATION ]</span>
<div class="ai-header-controls">
<button class="title-action-btn" onclick="emitData()">SAVE</button>
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
<input type="password" id="api-field-input" class="ai-input" placeholder="ENTER ACCESS KEY OR PATH..." value=" """ + p_key + """ ">
</div>
<div>
<label>API URL:</label>
<input type="text" id="url-input" class="ai-input" value=" """ + p_url + """ ">
</div>
</div>
</div>
</div>
</div>

<script>
document.getElementById('version-select').value = """ + f'"{p_model}"' + """ ;

function emitData() {
    const apiKey = document.getElementById('api-field-input').value.trim();
    const model = document.getElementById('version-select').value;
    const apiUrl = document.getElementById('url-input').value.trim();
    
    const packet = {
        gemini_api_key: apiKey,
        gemini_model: model,
        gemini_url: apiUrl
    };
    
    window.parent.postMessage({
        type: 'streamlit:setComponentValue',
        value: packet
    }, '*');
}
</script>
"""

response_data = components.html(ai_set_html, height=700)

if response_data:
    with open("comutoy.json", "w") as f:
        json.dump(response_data, f, indent=4)
    st.toast("Cloud matrix updated in comutoy.json!", icon="⚙️")
