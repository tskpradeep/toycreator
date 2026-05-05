import streamlit as st
import streamlit.components.v1 as components

# 1. Page Configuration
st.set_page_config(layout="wide", page_title="CAD Designer Pro")

# 2. UI Reset (Minimalist/High Contrast)
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stApp { background-color: #000 !important; overflow: hidden !important; }
        .block-container { padding: 0rem !important; max-width: 100% !important; height: 100vh !important; }
    </style>
""", unsafe_allow_html=True)

# 3. Integrated Workbench UI
cad_app_html = """
<script src="https://cdnjs.cloudflare.com/ajax/libs/split.js/1.6.0/split.min.js"></script>
<style>
    html, body { margin: 0; padding: 0; height: 100%; width: 100%; overflow: hidden; background-color: #000; font-family: 'Segoe UI', sans-serif; color: white; }
    .master-container { display: flex; flex-direction: column; height: 100vh; width: 100vw; border: 2px solid #d3d3d3; box-sizing: border-box; position: relative; }
    
    /* MODULAR AI-SET WINDOW */
    #ai-modular-setup {
        position: absolute; top: 10%; left: 15%; width: 70%; height: 75%;
        background: #000; border: 2px solid #00ff00; z-index: 9999;
        display: none; flex-direction: column; box-shadow: 0 0 50px rgba(0,255,0,0.3);
    }
    .ai-setup-header { background: #0a1a0a; border-bottom: 1px solid #00ff00; padding: 10px; display: flex; justify-content: space-between; color: #00ff00; font-family: monospace; font-weight: bold; }
    .ai-setup-body { display: flex; flex: 1; overflow: hidden; }
    .ai-setup-sidebar { width: 30%; border-right: 1px solid #00ff00; padding: 10px; background: #050505; }
    .ai-setup-content { width: 70%; padding: 25px; color: #00ff00; font-family: monospace; display: flex; flex-direction: column; gap: 20px; }
    
    .ai-tool-item { padding: 12px; border: 1px solid #004400; margin-bottom: 8px; cursor: pointer; font-size: 11px; }
    .ai-tool-item.active { background: #00ff00; color: #000; font-weight: bold; }
    .ai-select { background: #000; border: 1px solid #00ff00; color: #00ff00; padding: 10px; width: 100%; cursor: pointer; font-family: monospace; }
    .ai-input { background: #000; border: 1px solid #00ff00; color: #00ff00; padding: 10px; width: 100%; box-sizing: border-box; }

    /* DASHBOARD ELEMENTS */
    .window-title-bar { background: #1a1a1a; height: 30px; display: flex; align-items: center; justify-content: space-between; padding: 0 10px; font-size: 12px; border-bottom: 1px solid #333; }
    #dynamic-zone { display: flex; flex: 1; min-height: 0; width: 100%; }
    .pane { background: #000; border: 1px solid #333; overflow: hidden; display: flex; align-items: center; justify-content: center; }
    .fixed-footer { height: 64px; display: flex; border-top: 2px solid #333; background: #000; align-items: flex-end; padding: 2px 4px; }
    .dropup { position: relative; width: 100%; height: 20px; background: #e1e1e1; color: #000; border: 1px solid #707070; display: flex; align-items: center; justify-content: space-between; padding: 0 5px; cursor: pointer; font-size: 9px; }
    .dropup.tall { height: 62px; }
</style>

<div class="master-container">
    <div id="ai-modular-setup">
        <div class="ai-setup-header"><span>[ SYSTEM AI-SET : LIVE TOOL CONFIG ]</span><span onclick="toggleAISet(false)" style="cursor:pointer;">[ X ]</span></div>
        <div class="ai-setup-body">
            <div class="ai-setup-sidebar">
                <div class="ai-tool-item active">GOOGLE GEMINI</div>
                <div class="ai-tool-item">LUVIA AI</div>
                <div class="ai-tool-item">FLUX.AI</div>
            </div>
            <div class="ai-setup-content">
                <label>GEMINI VERSION (LIVE MAY 2026):</label>
                <select class="ai-select" id="version-select">
                    <option value="gemini-3-flash">Gemini 3 Flash (Frontier/Fast)</option>
                    <option value="gemini-3.1-flash-lite">Gemini 3.1 Flash-Lite (High Volume)</option>
                    <option value="gemini-2.5-pro">Gemini 2.5 Pro (Deep Reasoning)</option>
                    <option value="gemini-2.5-flash">Gemini 2.5 Flash (Balanced)</option>
                    <option value="gemini-2.5-flash-lite">Gemini 2.5 Flash-Lite (Speed/Budget)</option>
                </select>
                <label>API KEY:</label>
                <input type="password" class="ai-input" placeholder="PASTE KEY HERE...">
                <button style="width: 100px; height: 30px; background:#00ff00; border:none; cursor:pointer;" onclick="toggleAISet(false)">SAVE</button>
            </div>
        </div>
    </div>

    <div class="window-title-bar"><div>CAD DESIGNER PRO</div></div>
    <div id="dynamic-zone">
        <div id="left-stack" style="width:70%;">
            <div id="cad-pane" class="pane" style="height:80%; color:#b22222; font-weight:bold;">SYSTEM CANVAS</div>
            <div id="cmd-pane" class="pane" style="height:20%; color:#0f0; font-family:monospace; font-size:11px; justify-content:flex-start; padding:10px;">>_ READY</div>
        </div>
        <div id="right-stack" style="width:30%;">
            <div id="ai-output" class="pane" style="height:50%; color:#008000; font-family:monospace; padding:10px; align-items:flex-start;">AI OUTPUT</div>
            <div id="ai-input" class="pane" style="height:50%;"><textarea style="width:100%; height:100%; background:transparent; border:none; color:#800080; padding:10px; font-family:monospace; outline:none;" placeholder="PROMPT..."></textarea></div>
        </div>
    </div>

    <div class="fixed-footer">
        <div style="flex:1; padding-left:10px; font-size:11px; color:#008000;">STABLE 2026.05</div>
        <div class="dropup tall" style="width:130px;" onclick="toggleAISet(true)"><span>AI-SET</span><span>▲</span></div>
    </div>
</div>

<script>
    Split(['#left-stack', '#right-stack'], { sizes: [70, 30], gutterSize: 4 });
    function toggleAISet(show) { document.getElementById('ai-modular-setup').style.display = show ? 'flex' : 'none'; }
</script>
"""

components.html(cad_app_html, height=0)
st.components.v1.html("""<script>window.parent.document.querySelector('iframe').style.height = '94vh';</script>""", height=0)
