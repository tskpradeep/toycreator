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

# 3. Native UI Application with AI-SET Logic
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
        box-sizing: border-box; flex-shrink: 0; font-size: 8px; font-weight: bold;
    }
    .btn-cell:active { 
        border-top: 2px solid #707070; border-left: 2px solid #707070;
        border-right: 2px solid #fff; border-bottom: 2px solid #fff;
        background: #bebebe;
    }

    .pane { background: #000 !important; border: 1px solid #333 !important; overflow: hidden; display: flex; align-items: center; justify-content: center; box-sizing: border-box; }
    
    /* MODAL SETUP WINDOW (Hidden by default) */
    #ai-setup-overlay {
        position: absolute; top: 10%; left: 10%; width: 50%; height: 70%;
        background: #111; border: 2px solid #0f0; z-index: 2000;
        display: none; flex-direction: column; padding: 20px;
        box-shadow: 0 0 20px #0f0;
    }

    .fixed-footer { 
        height: 64px; display: flex; flex-direction: row; 
        border-top: 2px solid #333; background: #000; flex-shrink: 0;
        align-items: flex-end; 
        padding: 0px 4px 2px 4px;
    }

    .footer-left-content { flex: 1; display: flex; height: 100%; align-items: center; padding-left: 10px;}
    .selection-b-container { width: 130px; height: 62px; margin-left: 5px; }
    .selection-a-stack { display: flex; flex-direction: column; gap: 1px; width: 130px; margin-left: 5px; }
    .footer-palette-grid { display: grid; grid-template-columns: repeat(6, 20px); grid-template-rows: repeat(3, 20px); gap: 1px; margin-left: 8px; }

    .dropup { 
        position: relative; width: 100%; height: 20px; 
        background: #e1e1e1; color: #000; border: 1px solid #707070; 
        display: flex; align-items: center; justify-content: space-between;
        padding: 0 5px; cursor: pointer; font-size: 9px; box-sizing: border-box;
    }
    .dropup.tall { height: 62px; font-weight: bold; font-size: 14px; text-align:center; display: flex; align-items: center; justify-content: center; }

    .text-main { color: #b22222; font-size: 1.4vw; font-weight: bold; text-align: center; }
</style>

<div class="master-container">
    <div id="ai-setup-overlay">
        <div style="display:flex; justify-content:space-between; border-bottom:1px solid #0f0; padding-bottom:5px; margin-bottom:15px;">
            <span style="color:#0f0; font-family:monospace;">[ AI COMMAND CENTER ]</span>
            <span style="cursor:pointer; color:red;" onclick="toggleAI()">[ CLOSE ]</span>
        </div>
        <div style="flex:1; overflow-y:auto; font-family:monospace; font-size:12px;">
            <div style="margin-bottom:15px; border:1px solid #444; padding:10px;">
                <span style="color:#fff;">AI SLOT 01: GEMINI 2.0 (Architect)</span><br>
                <span style="color:#888;">STATUS: <span style="color:#0f0;">ACTIVE</span></span><br>
                <input type="password" placeholder="ENTER API KEY" style="width:100%; background:#222; border:1px solid #0f0; color:#0f0; margin-top:5px;">
            </div>
            <div style="margin-bottom:15px; border:1px solid #444; padding:10px;">
                <span style="color:#fff;">AI SLOT 02: GROQ/LLAMA3 (Code)</span><br>
                <span style="color:#888;">STATUS: <span style="color:#777;">PENDING</span></span><br>
                <input type="password" placeholder="ENTER API KEY" style="width:100%; background:#222; border:1px solid #444; color:#0f0; margin-top:5px;">
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
                <div id="cad-pane" class="pane text-main">visual displays dynamic between coding and screen/CAD designs</div>
                <div id="cmd-pane" class="pane" style="justify-content: flex-start; align-items: flex-start; color:#0f0; font-family:monospace; padding:5px;">>_ AI ENGINE STANDBY...</div>
            </div>
            <div id="right-stack" style="display:flex; flex-direction:column; width:30%;">
                <div id="ai-output" class="pane" style="color:#008000; font-weight:bold; padding:10px; font-family:monospace; font-size:12px; align-items:flex-start;">AI TEXT REPLYING WINDOW</div>
                <div id="ai-input" class="pane" style="color:#800080; font-weight:bold;"><textarea style="width:100%; height:100%; background:transparent; border:none; color:#800080; font-family:monospace; outline:none; padding:10px;" placeholder="USER PROMPTING..."></textarea></div>
            </div>
        </div>
        <div class="fixed-right-strip" id="side-strip"></div>
    </div>

    <div class="fixed-footer">
        <div class="footer-left-content">
            <span style="color:#008000; font-size: 11px; margin-right: 20px;">NODE-01: READY</span>
            <span style="color:#0000ff; font-size: 11px;">SYSTEM STATUS: ONLINE</span>
        </div>

        <div id="foot-palette" class="footer-palette-grid"></div>

        <div class="selection-a-stack">
            <div class="dropup"><span>Selection A</span><span>▲</span></div>
            <div class="dropup"><span>Selection A</span><span>▲</span></div>
            <div class="dropup"><span>Selection A</span><span>▲</span></div>
        </div>

        <div class="selection-b-container">
            <div class="dropup tall" style="background:#0f0; color:#000; border:2px solid #fff;" onclick="toggleAI()">AI-SET</div>
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
</script>
"""

components.html(cad_app_html, height=0)
st.components.v1.html(
    f"""<script>
        window.parent.document.querySelector('iframe').style.height = '94vh';
    </script>""",
    height=0
)
