import streamlit as st
import streamlit.components.v1 as components

# 1. Page Configuration
st.set_page_config(layout="wide", page_title="CAD Designer Pro - AI SET")

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
    }

    .window-title-bar {
        background: #1a1a1a; color: #888; height: 30px;
        flex-shrink: 0; display: flex; align-items: center; 
        justify-content: space-between; padding: 0 10px; font-size: 12px;
        border-bottom: 1px solid #333;
    }

    #dynamic-zone { display: flex; flex-direction: row; flex: 1; min-height: 0; width: 100%; position: relative;}

    .fixed-right-strip { 
        width: 65px; border-left: 1px solid #333; 
        display: grid; grid-template-columns: 1fr 1fr;
        grid-auto-rows: min-content; gap: 2px;
        padding: 5px; background: #000; 
        overflow-y: scroll; 
    }

    .btn-cell {
        aspect-ratio: 1 / 1; width: 20px; height: 20px;
        background: #e1e1e1; color: #000;
        border-top: 2px solid #fff; border-left: 2px solid #fff;
        border-right: 2px solid #707070; border-bottom: 2px solid #707070;
        cursor: pointer; display: flex; align-items: center; justify-content: center;
        box-sizing: border-box; flex-shrink: 0;
    }

    /* CRIMSON VIOLET COMMAND CENTER */
    #ai-setup-overlay {
        position: absolute; top: 5%; left: 5%; width: 90%; height: 85%;
        background: #0a050a; border: 2px solid #8a2be2; z-index: 2000;
        display: none; flex-direction: column; padding: 15px;
        box-shadow: 0 0 30px #dc143c;
    }

    .setup-header { display:flex; justify-content:space-between; border-bottom:1px solid #8a2be2; padding-bottom:10px; margin-bottom:10px; font-family:monospace; }
    
    .setup-body { display: flex; flex: 1; gap: 10px; overflow: hidden; }
    
    .ai-list-pane { width: 30%; border-right: 1px solid #333; display: flex; flex-direction: column; gap: 5px; padding-right: 10px; }
    .ai-settings-pane { width: 70%; padding-left: 10px; display: flex; flex-direction: column; }

    .ai-item-btn { 
        background: #1a001a; border: 1px solid #dc143c; color: #fff; 
        padding: 8px; font-size: 11px; cursor: pointer; text-align: left;
        font-family: monospace;
    }
    .ai-item-btn:hover { background: #8a2be2; }
    .add-btn { background: #4b0082; color: #fff; border: 1px solid #fff; padding: 5px; cursor: pointer; margin-top: auto; font-family: monospace; }

    .setting-row { margin-bottom: 20px; font-family: monospace; }
    .setting-input { width: 100%; background: #000; border: 1px solid #8a2be2; color: #fff; padding: 8px; margin-top: 5px; }
    .setting-select { width: 100%; background: #000; border: 1px solid #dc143c; color: #fff; padding: 8px; margin-top: 5px; }

    .pane { background: #000 !important; border: 1px solid #333 !important; overflow: hidden; display: flex; align-items: center; justify-content: center; box-sizing: border-box; }
    
    .fixed-footer { 
        height: 64px; display: flex; flex-direction: row; 
        border-top: 2px solid #333; background: #000; flex-shrink: 0;
        align-items: flex-end; 
        padding: 0px 4px 2px 4px;
    }

    .selection-b-container { width: 130px; height: 62px; margin-left: 5px; }
    .dropup.tall { height: 62px; font-weight: bold; font-size: 14px; display: flex; align-items: center; justify-content: center; cursor: pointer;}
</style>

<div class="master-container">
    <!-- MODAL SETUP -->
    <div id="ai-setup-overlay">
        <div class="setup-header">
            <span style="color:#dc143c;">[ AI MULTI-DISPATCHER CONFIG ]</span>
            <span style="cursor:pointer; color:#8a2be2;" onclick="toggleAI()">[ X CLOSE ]</span>
        </div>
        <div class="setup-body">
            <div class="ai-list-pane" id="ai-list">
                <div class="ai-item-btn" onclick="showSet('GEMINI 1.5 PRO')">01. GEMINI 1.5 PRO</div>
                <div class="ai-item-btn" onclick="showSet('GROQ LLAMA-3')">02. GROQ LLAMA-3</div>
                <button class="add-btn">[ + ADD NEW AI MODULE ]</button>
            </div>
            <div class="ai-settings-pane" id="ai-settings">
                <div id="set-default" style="color:#444; font-family:monospace;">SELECT AN AI FROM THE LEFT TO CONFIGURE...</div>
                <div id="set-active" style="display:none;">
                    <h3 id="set-title" style="color:#8a2be2; font-family:monospace; margin-top:0;">CONFIGURATION</h3>
                    <div class="setting-row">
                        <label>ENTER API KEY:</label>
                        <input type="password" class="setting-input" placeholder="PX-XXXX-XXXX-XXXX">
                    </div>
                    <div class="setting-row">
                        <label>ASSIGN TECHNICAL TASK:</label>
                        <select class="setting-select">
                            <option>System Architecture (Hardware)</option>
                            <option>Firmware & Code Generation</option>
                            <option>BOM & Parts Analysis</option>
                            <option>Thermal & High-Current Physics</option>
                        </select>
                    </div>
                    <div style="color:#dc143c; font-size:10px; font-family:monospace;">
                        NOTE: When a prompt involves the assigned task, this AI will trigger automatically.
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="window-title-bar">
        <div>CAD DESIGNER PRO</div>
        <div><span>−</span><span style="margin:0 10px;">❐</span><span>×</span></div>
    </div>

    <div id="dynamic-zone">
        <div id="split-container" style="display:flex; flex:1; width:100%;">
            <div id="left-stack" style="display:flex; flex-direction:column; width:70%;">
                <div id="cad-pane" class="pane" style="color:#b22222; font-size:1.4vw; font-weight:bold;">Visual Monitor Standby</div>
                <div id="cmd-pane" class="pane" style="justify-content: flex-start; align-items: flex-start; color:#0f0; font-family:monospace; padding:5px;">>_ SYSTEM READY</div>
            </div>
            <div id="right-stack" style="display:flex; flex-direction:column; width:30%;">
                <div id="ai-output" class="pane" style="color:#008000; font-weight:bold; font-family:monospace; font-size:12px; padding:10px; align-items:flex-start;">AI DISPATCHER LOGS...</div>
                <div id="ai-input" class="pane"><textarea style="width:100%; height:100%; background:transparent; border:none; color:#800080; font-family:monospace; outline:none; padding:10px;" placeholder="PROMPT SYSTEM..."></textarea></div>
            </div>
        </div>
        <div class="fixed-right-strip" id="side-strip"></div>
    </div>

    <div class="fixed-footer">
        <div style="flex:1; display:flex; align-items:center; padding-left:10px;">
            <span style="color:#008000; font-size: 11px; margin-right: 20px;">CORE: STABLE</span>
            <span style="color:#0000ff; font-size: 11px;">MODE: MULTI-AI</span>
        </div>
        <div id="foot-palette" class="footer-palette-grid"></div>
        <div class="selection-a-stack" style="display: flex; flex-direction: column; gap: 1px; width: 130px; margin-left: 5px;">
            <div class="dropup" style="background:#e1e1e1; color:#000; height:20px; font-size:9px; padding:0 5px; border:1px solid #707070;">Selection A</div>
            <div class="dropup" style="background:#e1e1e1; color:#000; height:20px; font-size:9px; padding:0 5px; border:1px solid #707070;">Selection A</div>
            <div class="dropup" style="background:#e1e1e1; color:#000; height:20px; font-size:9px; padding:0 5px; border:1px solid #707070;">Selection A</div>
        </div>
        <div class="selection-b-container">
            <div class="dropup tall" style="background:#8a2be2; color:#fff; border:2px solid #dc143c;" onclick="toggleAI()">AI-SET</div>
        </div>
    </div>
</div>

<script>
    Split(['#left-stack', '#right-stack'], { sizes: [70, 30], gutterSize: 4 });
    Split(['#cad-pane', '#cmd-pane'], { direction: 'vertical', sizes: [80, 20], gutterSize: 4 });
    Split(['#ai-output', '#ai-input'], { direction: 'vertical', sizes: [50, 50], gutterSize: 4 });

    const side = document.getElementById('side-strip');
    for(let i=0; i<100; i++) side.innerHTML += '<div class="btn-cell"></div>';
    
    const palette = document.getElementById('foot-palette');
    for(let i=0; i<18; i++) palette.innerHTML += '<div class="btn-cell"></div>';

    function toggleAI() {
        const modal = document.getElementById('ai-setup-overlay');
        modal.style.display = modal.style.display === 'flex' ? 'none' : 'flex';
    }

    function showSet(aiName) {
        document.getElementById('set-default').style.display = 'none';
        document.getElementById('set-active').style.display = 'block';
        document.getElementById('set-title').innerText = 'CONFIG: ' + aiName;
    }
</script>
"""

components.html(cad_app_html, height=0)
st.components.v1.html(f"<script>window.parent.document.querySelector('iframe').style.height = '94vh';</script>", height=0)
