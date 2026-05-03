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

# 3. Native UI Application with Modular AI Window
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

    /* MODULAR AI WINDOW - GREEN VIBE */
    #ai-modular-window {
        position: absolute; top: 15%; left: 20%; width: 60%; height: 60%;
        background: #000; border: 2px solid #0f0; z-index: 10000;
        display: none; flex-direction: column; box-shadow: 0 0 30px rgba(0,255,0,0.2);
    }
    .modal-header { background: #0a1a0a; border-bottom: 1px solid #0f0; padding: 10px; display: flex; justify-content: space-between; color: #0f0; font-family: monospace; font-size: 12px; }
    .modal-body { display: flex; flex: 1; overflow: hidden; }
    .modal-sidebar { width: 35%; border-right: 1px solid #0f0; padding: 10px; background: #050505; }
    .modal-content { width: 65%; padding: 20px; color: #0f0; font-family: monospace; display: flex; flex-direction: column; gap: 15px; }
    
    .ai-item { padding: 8px; border: 1px solid #050; margin-bottom: 5px; cursor: pointer; font-size: 11px; }
    .ai-item.active { background: #0f0; color: #000; font-weight: bold; }
    .api-input { background: #000; border: 1px solid #0f0; color: #0f0; padding: 8px; width: 100%; outline: none; }

    /* DASHBOARD ELEMENTS */
    .window-title-bar { background: #1a1a1a; color: #888; height: 30px; display: flex; align-items: center; justify-content: space-between; padding: 0 10px; font-size: 12px; border-bottom: 1px solid #333; }
    #dynamic-zone { display: flex; flex: 1; min-height: 0; width: 100%; }
    .pane { background: #000 !important; border: 1px solid #333 !important; overflow: hidden; display: flex; align-items: center; justify-content: center; box-sizing: border-box; }
    .gutter { background-color: #444 !important; }

    /* FOOTER & BUTTONS */
    .fixed-footer { height: 64px; display: flex; border-top: 2px solid #333; background: #000; padding: 0 4px; align-items: flex-end; }
    .btn-classic { background: #e1e1e1; color: #000; border: 2px solid; border-color: #fff #707070 #707070 #fff; padding: 4px 10px; cursor: pointer; font-size: 11px; margin-right: 5px; margin-bottom: 5px;}
    .btn-classic:active { border-color: #707070 #fff #fff #707070; background: #bebebe; }
</style>

<div class="master-container">
    <!-- MODULAR AI WINDOW -->
    <div id="ai-modular-window">
        <div class="modal-header">
            <span>[ SYSTEM AI CORE CONFIG ]</span>
            <span onclick="toggleAI(false)" style="cursor:pointer">[ CLOSE ]</span>
        </div>
        <div class="modal-body">
            <div class="modal-sidebar">
                <div class="ai-item active" onclick="selectModel(this, 'Gemini 3.0 Pro')">GEMINI 3.0 PRO</div>
                <div class="ai-item" onclick="selectModel(this, 'Gemini 3.0 Flash')">GEMINI 3.0 FLASH</div>
                <div class="ai-item" onclick="selectModel(this, 'Gemini 2.0 Pro')">GEMINI 2.0 PRO</div>
            </div>
            <div class="modal-content">
                <label>ACTIVE ENGINE: <span id="active-model-name">Gemini 3.0 Pro</span></label>
                <input type="password" class="api-input" placeholder="PASTE API KEY HERE...">
                <a href="https://aistudio.google.com/app/apikey" target="_blank" style="color:#0f0; font-size:10px;">GET FREE KEY ↗</a>
                <button class="btn-classic" style="margin-top:auto; background:#0f0; border:none;" onclick="toggleAI(false)">SAVE CONFIG</button>
            </div>
        </div>
    </div>

    <div class="window-title-bar">
        <div>CAD DESIGNER PRO - INDUSTRIAL V1</div>
        <div><span>−</span><span style="margin:0 10px;">❐</span><span>×</span></div>
    </div>

    <div id="dynamic-zone">
        <div id="split-container" style="display:flex; flex:1;">
            <div id="left-stack" style="display:flex; flex-direction:column; width:70%;">
                <div id="cad-pane" class="pane">CAD VIEWPORT</div>
                <div id="cmd-pane" class="pane">SYSTEM CONSOLE</div>
            </div>
            <div id="right-stack" style="display:flex; flex-direction:column; width:30%;">
                <div id="ai-output" class="pane">AI REPLY</div>
                <div id="ai-input" class="pane">USER PROMPT</div>
            </div>
        </div>
    </div>

    <div class="fixed-footer">
        <button class="btn-classic" onclick="toggleAI(true)">AI SETTINGS</button>
        <button class="btn-classic">BOM GEN</button>
        <button class="btn-classic">EXPORT</button>
    </div>
</div>

<script>
    Split(['#left-stack', '#right-stack'], { sizes: [70, 30], gutterSize: 6 });
    Split(['#cad-pane', '#cmd-pane'], { direction: 'vertical', sizes: [80, 20], gutterSize: 6 });

    function toggleAI(show) {
        document.getElementById('ai-modular-window').style.display = show ? 'flex' : 'none';
    }

    function selectModel(el, name) {
        document.querySelectorAll('.ai-item').forEach(i => i.classList.remove('active'));
        el.classList.add('active');
        document.getElementById('active-model-name').innerText = name;
    }
</script>
"""

components.html(cad_app_html, height=0)
st.components.v1.html(
    f"""<script>
        window.parent.document.querySelector('iframe').style.height = '95vh';
    </script>""",
    height=0
)
