import streamlit as st
import streamlit.components.v1 as components

# 1. Page Configuration
st.set_page_config(layout="wide", page_title="ToyCreator Workbench")

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

# 3. Complete Restored Workbench + AI-SET Match
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

    /* --- SYSTEM AI-SET WINDOW (EXACT MATCH image_e3e7f9.png) --- */
    #ai-modular-setup {
        position: absolute; top: 5%; left: 5%; width: 90%; height: 85%;
        background: #000; border: 2px solid #00ff00; z-index: 9999;
        display: none; flex-direction: column;
    }
    .ai-setup-header { 
        border-bottom: 1px solid #00ff00; padding: 10px; 
        display: flex; justify-content: space-between; align-items: center;
        color: #00ff00; font-family: monospace;
    }
    .ai-setup-body { display: flex; flex: 1; overflow: hidden; }
    .ai-setup-sidebar { width: 300px; border-right: 1px solid #00ff00; padding: 15px; }
    .ai-setup-content { flex: 1; padding: 30px; color: #00ff00; font-family: monospace; display: flex; flex-direction: column; gap: 20px; }
    
    .ai-tool-item { padding: 12px; border: 1px solid #333; margin-bottom: 8px; cursor: pointer; color: #00ff00; font-weight: bold; }
    .ai-tool-item.active { background: #00ff00; color: #000; border-color: #00ff00; }
    
    .field-box { border: 1px solid #00ff00; padding: 12px; background: transparent; color: #00ff00; margin-bottom: 15px; }
    .ai-input-field { border: 1px solid #00ff00; padding: 12px; background: transparent; color: #00ff00; width: 100%; outline: none; box-sizing: border-box; }

    .btn-save { background: #000; border: 1px solid #00ff00; color: #00ff00; padding: 2px 15px; cursor: pointer; font-family: monospace; margin-right: 10px;}
    .btn-close { background: #000; border: 1px solid #fff; color: #fff; padding: 2px 10px; cursor: pointer; font-family: monospace; }

    /* --- DASHBOARD ELEMENTS (RESTORED) --- */
    .window-title-bar { background: #1a1a1a; color: #888; height: 30px; display: flex; align-items: center; justify-content: space-between; padding: 0 10px; font-size: 12px; border-bottom: 1px solid #333; }
    #dynamic-zone { display: flex; flex-direction: row; flex: 1; min-height: 0; width: 100%; }
    
    /* Side Strip */
    .fixed-right-strip { width: 65px; border-left: 1px solid #333; display: grid; grid-template-columns: 1fr 1fr; grid-auto-rows: min-content; gap: 2px; padding: 5px; background: #000; overflow-y: auto; }
    .btn-cell { aspect-ratio: 1 / 1; width: 22px; height: 22px; background: #e1e1e1; border-top: 2px solid #fff; border-left: 2px solid #fff; border-right: 2px solid #707070; border-bottom: 2px solid #707070; cursor: pointer; }

    /* Panes */
    .pane { background: #000; border: 1px solid #333; overflow: hidden; display: flex; }
    .gutter { background-color: #444 !important; }
    
    /* Footer */
    .fixed-footer { height: 64px; display: flex; flex-direction: row; border-top: 2px solid #333; background: #000; align-items: flex-end; padding: 0 4px 2px 4px; }
    .footer-palette-grid { display: grid; grid-template-columns: repeat(6, 22px); gap: 1px; margin: 0 10px; }
    .dropup { position: relative; width: 130px; height: 20px; background: #e1e1e1; color: #000; border: 1px solid #707070; display: flex; align-items: center; justify-content: space-between; padding: 0 5px; cursor: pointer; font-size: 10px; margin-bottom: 1px;}
    .dropup.tall { height: 62px; }
</style>

<div class="master-container">
    <!-- MODULAR WINDOW -->
    <div id="ai-modular-setup">
        <div class="ai-setup-header">
            <span>[ SYSTEM AI-SET : TOOL CONFIGURATION ]</span>
            <div>
                <button class="btn-save" onclick="saveData()">SAVE</button>
                <button class="btn-close" onclick="toggleAISet(false)">[ X ]</button>
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
                <div style="font-size: 24px; font-weight: bold; margin-bottom: 10px;">TOOL: Google Gemini</div>
                <label class="field-label">AVAILABLE VERSIONS:</label>
                <div class="field-box">Gemini 3 Flash (PhD reasoning/Speed)</div>
                <label class="field-label">CORE FUNCTION:</label>
                <div class="field-box">Multi-modal Reasoning</div>
                <label class="field-label">API KEY / LOCAL PATH:</label>
                <input type="password" id="api-field" class="ai-input-field" placeholder="ENTER ACCESS KEY OR PATH...">
            </div>
        </div>
    </div>

    <div class="window-title-bar">
        <div>TOYCREATOR WORKBENCH</div>
        <div><span>−</span><span style="margin:0 10px;">❐</span><span>×</span></div>
    </div>

    <div id="dynamic-zone">
        <div id="split-container" style="display:flex; flex:1; width:100%;">
            <div id="left-stack" style="display:flex; flex-direction:column;">
                <div id="cad-pane" class="pane" style="flex: 0.8; justify-content: center; align-items: center; color: #b22222; font-weight: bold; font-size: 20px;">
                    <div id="visual-monitor">VISUAL AREA</div>
                </div>
                <div id="cmd-pane" class="pane" style="flex: 0.2; background: #000; color: #0f0; padding: 10px; font-family: monospace; font-size: 12px;">
                    <div id="terminal-out">>_ SYSTEM READY</div>
                </div>
            </div>
            <div id="right-stack" style="display:flex; flex-direction:column;">
                <div id="ai-output" class="pane" style="flex: 0.6; padding: 10px; color: #008000; font-family: monospace;">AI OUTPUT AREA</div>
                <div id="ai-input" class="pane" style="flex: 0.4;">
                    <textarea style="width:100%; height:100%; background:transparent; border:none; color:#800080; padding:10px; outline:none; font-family:monospace; font-weight:bold;" placeholder="TYPE HERE..."></textarea>
                </div>
            </div>
        </div>
        <div class="fixed-right-strip" id="side-strip"></div>
    </div>

    <div class="fixed-footer">
        <div style="flex:1; color:#008000; font-size:11px; padding-left:10px;">READY</div>
        <div id="foot-palette" class="footer-palette-grid"></div>
        <div style="display:flex; flex-direction:column;">
            <div class="dropup"><span>File</span><span>▲</span></div>
            <div class="dropup"><span>Tools</span><span>▲</span></div>
            <div class="dropup"><span>View</span><span>▲</span></div>
        </div>
        <div class="dropup tall" style="margin-left:5px;" onclick="toggleAISet(true)">
            <span style="font-weight:bold;">AI-SET</span><span>▲</span>
        </div>
    </div>
</div>

<script>
    Split(['#left-stack', '#right-stack'], { sizes: [70, 30], gutterSize: 4 });
    
    for(let i=0; i<60; i++) document.getElementById('side-strip').innerHTML += '<div class="btn-cell"></div>';
    for(let i=0; i<18; i++) document.getElementById('foot-palette').innerHTML += '<div class="btn-cell"></div>';

    function toggleAISet(show) { document.getElementById('ai-modular-setup').style.display = show ? 'flex' : 'none'; }
    
    function saveData() {
        const val = document.getElementById('api-field').value;
        localStorage.setItem('gemini_key', val);
        document.getElementById('terminal-out').innerHTML += "<br>> SETTINGS PERSISTED FOR GOOGLE GEMINI";
        toggleAISet(false);
    }
</script>
"""

components.html(cad_app_html, height=0)
st.components.v1.html(f"<script>window.parent.document.querySelector('iframe').style.height = '95vh';</script>", height=0)
