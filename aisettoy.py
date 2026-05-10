import streamlit as st
import streamlit.components.v1 as components
import json

st.set_page_config(layout="wide", page_title="AI-SET CONFIG")

# Streamlit styles to match the black background
st.markdown("<style>.stApp { background:#000 !important; }</style>", unsafe_allow_html=True)

# This component contains the EXACT HTML/CSS from your original "ai-modular-setup" div
aisettoy_html = """
<style>
html, body { margin:0; padding:0; height:100%; width:100%; background:#000; font-family:'Segoe UI',sans-serif; color:#00ff00; overflow:hidden; }
#ai-modular-setup { display:flex; flex-direction:column; height:100vh; width:100vw; background:#000; border:2px solid #00ff00; box-sizing:border-box; }
.ai-setup-header { background:#0a1a0a; border-bottom:1px solid #00ff00; padding:10px; display:flex; justify-content:space-between; color:#00ff00; font-family:monospace; font-weight:bold; align-items:center; }
.ai-setup-body { display:flex; flex:1; overflow:hidden; }
.ai-setup-sidebar { width:30%; border-right:1px solid #00ff00; padding:10px; background:#050505; overflow-y:auto; }
.ai-setup-content { width:70%; padding:25px; color:#00ff00; font-family:monospace; display:flex; flex-direction:column; gap:20px; overflow-y:auto; }
.ai-tool-item { padding:12px; border:1px solid #004400; margin-bottom:8px; cursor:pointer; font-size:12px; transition:0.2s; }
.ai-tool-item.active { background:#00ff00; color:#000; font-weight:bold; }
.ai-select, .ai-input { background:#000; border:1px solid #00ff00; color:#00ff00; padding:10px; width:100%; outline:none; font-family:monospace; box-sizing:border-box; }
.title-action-btn { padding:2px 12px; font-size:10px; cursor:pointer; border:1px solid #00ff00; background:#000; color:#00ff00; font-family:monospace; text-transform:uppercase; }
.title-action-btn:hover { background:#00ff00; color:#000; }
</style>

<div id="ai-modular-setup">
    <div class="ai-setup-header">
        <span>[ SYSTEM AI-SET : TOOL CONFIGURATION ]</span>
        <div class="ai-header-controls">
            <button class="title-action-btn" onclick="saveToJSON()">SAVE</button>
            <button class="title-action-btn" onclick="window.close()">[ X ]</button>
        </div>
    </div>
    <div class="ai-setup-body">
        <div class="ai-setup-sidebar">
            <div class="ai-tool-item active">GOOGLE GEMINI</div>
            <div class="ai-tool-item">LUVIA AI</div>
            <div class="ai-tool-item">FLUX.AI</div>
        </div>
        <div class="ai-setup-content">
            <div style="font-size:20px;border-bottom:2px solid #004400;padding-bottom:5px;color:#fff;">TOOL: <span id="tool-name">Google Gemini</span></div>
            <div>
                <label>AVAILABLE VERSIONS:</label>
                <select class="ai-select" id="version-select">
                    <option value="gemini-1.5-flash">Gemini 1.5 Flash</option>
                    <option value="gemini-1.5-pro">Gemini 1.5 Pro</option>
                </select>
            </div>
            <div>
                <label>API KEY / LOCAL PATH:</label>
                <input type="password" id="api-field-input" class="ai-input" placeholder="ENTER ACCESS KEY...">
            </div>
            <div>
                <label>API URL:</label>
                <input type="text" id="url-input" class="ai-input" value="https://generativelanguage.googleapis.com/v1beta/models/">
            </div>
        </div>
    </div>
</div>

<script>
function saveToJSON() {
    const data = {
        version: document.getElementById('version-select').value,
        api_key: document.getElementById('api-field-input').value,
        api_url: document.getElementById('url-input').value
    };
    
    // Send data back to Streamlit to save as comutoy.json
    window.parent.postMessage({
        type: 'streamlit:setComponentValue',
        value: data
    }, '*');
    
    alert("CONFIG SENT TO SYSTEM");
}
</script>
"""

# Logic to catch the message from the HTML and save it to the JSON file
res = components.html(aisettoy_html, height=600)

if res:
    with open("comutoy.json", "w") as f:
        json.dump(res, f, indent=4)
    st.success("comutoy.json updated.")
