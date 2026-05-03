import streamlit as st
import streamlit.components.v1 as components

# 1. Page Configuration
st.set_page_config(layout="wide", page_title="CAD Design Portal")

# 2. Reset Streamlit's default padding
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

# 3. The Refined App Code
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
        border: 2px solid #d3d3d3; 
        box-sizing: border-box;
    }

    .window-title-bar {
        background: #1a1a1a; color: #888; height: 30px;
        flex-shrink: 0; display: flex; align-items: center; 
        justify-content: space-between; padding: 0 10px; font-size: 12px;
        border-bottom: 1px solid #333;
    }

    #dynamic-zone { 
        display: flex; flex-direction: row; flex: 1; 
        min-height: 0; width: 100%;
    }

    .flex-row { display: flex; flex-direction: row; height: 100%; width: 100%; overflow: hidden; }
    .flex-col { display: flex; flex-direction: column; height: 100%; width: 100%; overflow: hidden; }
    
    .pane { 
        background: #000 !important; 
        border: 1px solid #333 !important; 
        display: flex; align-items: center; justify-content: center; 
        overflow: hidden; padding: 5px; box-sizing: border-box;
    }

    .gutter { background-color: #222; flex-shrink: 0; }
    .gutter.gutter-horizontal { cursor: col-resize; background-color: #444 !important; width: 4px !important; }
    .gutter.gutter-vertical { cursor: row-resize; background-color: #444 !important; height: 4px !important; }

    /* NATIVE BUTTON STYLE - SQUARED & SIZED */
    .btn-cell {
        aspect-ratio: 1 / 1;
        width: 100%; /* Fill width of grid column */
        background: #e1e1e1;
        color: #000;
        border-top: 2px solid #fff;
        border-left: 2px solid #fff;
        border-right: 2px solid #707070;
        border-bottom: 2px solid #707070;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        box-sizing: border-box;
    }
    .btn-cell:active { 
        border-top: 2px solid #707070;
        border-left: 2px solid #707070;
        border-right: 2px solid #fff;
        border-bottom: 2px solid #fff;
        background: #bebebe;
    }

    /* Side Strip Layout */
    .fixed-right-strip { 
        width: 65px; border-left: 1px solid #333; 
        display: grid; grid-template-columns: 1fr 1fr;
        grid-auto-rows: min-content; gap: 4px;
        padding: 5px; background: #000; overflow-y: auto;
    }

    /* Footer Button Grid - Maximize buttons */
    .footer-btn-grid { 
        display: grid; 
        grid-template-columns: repeat(8, 1fr); /* More columns for more buttons */
        gap: 2px; 
        width: 100%;
    }

    /* NATIVE DROP-UP STYLE - CLICK TRIGGERED */
    .dropup { 
        position: relative; width: 90%; height: 26px; 
        background: #e1e1e1; color: #000;
        border: 1px solid #707070; 
        display: flex; align-items: center; justify-content: space-between;
        padding: 0 5px; cursor: pointer; font-size: 10px;
    }
    .dropup-content {
        display: none; position: absolute; bottom: 105%; left: -1px;
        background-color: #f0f0f0; min-width: 130px; 
        border: 1px solid #707070; box-shadow: 2px -2px 5px rgba(0,0,0,0.5);
        z-index: 1000;
    }
    .dropup.show .dropup-content { display: block; }
    .dropup-content a { color: #000; padding: 8px 10px; text-decoration: none; display: block; border-bottom: 1px solid #ccc; }
    .dropup-content a:hover { background: #0078d7; color: white; }

    .fixed-footer { 
        height: 80px; display: flex; flex-direction: row; 
        border-top: 2px solid #333; background: #000; flex-shrink: 0; 
    }

    .footer-item { border-right: 1px solid #333; display: flex; align-items: center; justify-content: center; padding: 4px; font-size: 11px; }

    .text-main { color: #b22222; font-size: 1.4vw; font-weight: bold; text-align: center; border: none !important; }
</style>

<div class="master-container">
    <div class="window-title-bar">
        <div>CAD DESIGNER PRO</div>
        <div><span>−</span><span style="margin:0 10px;">❐</span><span>×</span></div>
    </div>

    <div id="dynamic-zone">
        <div id="split-container" class="flex-row" style="flex-grow: 1;">
            <div id="left-side-stack" class="flex-col">
                <div id="cad-pane" class="pane text-main">visual displays dynamic between coding and screen/CAD designs</div>
                <div id="cmd-pane" class="pane" style="justify-content: flex-start; align-items: flex-start;">
                    <code style="color: #00FF00; font-family: monospace; padding: 5px;">>_</code>
                </div>
            </div>
            <div id="ai-column" class="flex-col">
                <div id="ai-output" class="pane" style="color: #008000; font-weight: bold;">AI TEXT REPLYING WINDOW</div>
                <div id="ai-input" class="pane" style="color: #800080; font-weight: bold;">USER PROMPTING</div>
            </div>
        </div>
        <div class="fixed-right-strip" id="side-strip"></div>
    </div>

    <div class="fixed-footer">
        <div class="footer-item" style="flex: 1.5; color: #008000;">small indicators</div>
        <div class="footer-item" style="flex: 2.5; color: #0000ff;">buttons for controlling...</div>
        
        <div class="footer-item" style="flex: 1.5;">
            <div class="dropup" onclick="toggleDropup(event, 'drop1')" id="drop1">
                <span>Selection A</span>
                <span style="font-size: 8px;">▲</span>
                <div class="dropup-content">
                    <a>Excel Mode</a>
                    <a>PowerShell View</a>
                    <a>Tcl Console</a>
                </div>
            </div>
        </div>

        <div class="footer-item" style="flex: 2.5;">
            <div id="foot-grid" class="footer-btn-grid"></div>
        </div>

        <div class="footer-item" style="flex: 1.5; border-right: none;">
            <div class="dropup" onclick="toggleDropup(event, 'drop2')" id="drop2">
                <span>Selection B</span>
                <span style="font-size: 8px;">▲</span>
                <div class="dropup-content">
                    <a>System Settings</a>
                    <a>Export Design</a>
                    <a>Help Manual</a>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
    Split(['#left-side-stack', '#ai-column'], { sizes: [70, 30], gutterSize: 4 });
    Split(['#cad-pane', '#cmd-pane'], { direction: 'vertical', sizes: [80, 20], gutterSize: 4 });
    Split(['#ai-output', '#ai-input'], { direction: 'vertical', sizes: [50, 50], gutterSize: 4 });

    const side = document.getElementById('side-strip');
    for(let i=0; i<44; i++) side.innerHTML += '<div class="btn-cell"></div>';
    
    const foot = document.getElementById('foot-grid');
    for(let i=0; i<24; i++) foot.innerHTML += '<div class="btn-cell"></div>';

    // Toggle Dropup on Click
    function toggleDropup(event, id) {
        event.stopPropagation();
        const el = document.getElementById(id);
        const wasOpen = el.classList.contains('show');
        
        // Close all others first
        document.querySelectorAll('.dropup').forEach(d => d.classList.remove('show'));
        
        if (!wasOpen) el.classList.add('show');
    }

    // Close menus if user clicks anywhere else
    window.onclick = function() {
        document.querySelectorAll('.dropup').forEach(d => d.classList.remove('show'));
    };
</script>
"""

# Maintain fixed screen height
components.html(cad_app_html, height=0)
st.components.v1.html(
    f"""<script>
        window.parent.document.querySelector('iframe').style.height = '94vh';
    </script>""",
    height=0
)
