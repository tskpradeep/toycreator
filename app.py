import streamlit as st
import streamlit.components.v1 as components

# 1. Page Configuration
st.set_page_config(layout="wide", page_title="CAD Design Portal")

# 2. CSS to clean up the Streamlit interface
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

# 3. The Application Logic
cad_app_html = """
<script src="https://cdnjs.cloudflare.com/ajax/libs/split.js/1.6.0/split.min.js"></script>
<style>
    html, body { 
        margin: 0; padding: 0; height: 100%; width: 100%; 
        overflow: hidden !important; background-color: #000; 
        font-family: 'Segoe UI', sans-serif;
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
        overflow: hidden; padding: 5px; 
    }

    .gutter { background-color: #222; flex-shrink: 0; }
    .gutter.gutter-horizontal { cursor: col-resize; background-color: #444 !important; width: 4px !important; }
    .gutter.gutter-vertical { cursor: row-resize; background-color: #444 !important; height: 4px !important; }

    /* YELLOW AREAS: Clickable Button Logic */
    .btn-cell {
        width: 18px; height: 18px; border: 1px solid #444; 
        background: #111; flex-shrink: 0; cursor: pointer;
        display: flex; align-items: center; justify-content: center;
        transition: background 0.2s;
    }
    .btn-cell:hover { background: #333; border-color: #888; }
    .btn-cell:active { background: #555; }

    .fixed-right-strip { 
        width: 60px; border-left: 1px solid #333; 
        display: grid; grid-template-columns: 1fr 1fr;
        grid-auto-rows: min-content; gap: 4px;
        padding: 5px; background: #000;
    }

    /* RED AREAS: Drop-up Menu Logic */
    .dropup { position: relative; display: inline-block; width: 100%; height: 100%; }
    .dropup-content {
        display: none; position: absolute; bottom: 100%; left: 0;
        background-color: #1a1a1a; min-width: 120px;
        border: 1px solid #444; z-index: 10;
    }
    .dropup-content a {
        color: #888; padding: 8px 12px; text-decoration: none;
        display: block; font-size: 10px; border-bottom: 1px solid #333;
    }
    .dropup-content a:hover { background-color: #333; color: white; }
    .dropup:hover .dropup-content { display: block; }

    .fixed-footer { 
        height: 75px; display: flex; flex-direction: row; 
        border-top: 1px solid #333; background: #000; flex-shrink: 0; 
    }

    .footer-item { border-right: 1px solid #333; display: flex; align-items: center; justify-content: center; padding: 2px; font-size: 11px; }
    
    .footer-btn-grid {
        display: grid; grid-template-columns: repeat(6, 1fr); 
        gap: 2px; padding: 2px;
    }

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
                    <code style="color: #00FF00; font-family: monospace;">>_</code>
                </div>
            </div>
            <div id="ai-column" class="flex-col">
                <div id="ai-output" class="pane" style="color: #008000; font-weight: bold;">AI TEXT REPLYING WINDOW</div>
                <div id="ai-input" class="pane" style="color: #800080; font-weight: bold;">USER PROMPTING</div>
            </div>
        </div>
        <div class="fixed-right-strip" id="side-strip">
            <!-- Densely packed yellow-area buttons -->
        </div>
    </div>

    <div class="fixed-footer">
        <div class="footer-item" style="flex: 1.5; color: #008000;">small indicators</div>
        <div class="footer-item" style="flex: 3; color: #0000ff;">buttons for controlling...</div>
        
        <!-- RED AREA (Left Drop-up) -->
        <div class="footer-item" style="flex: 1.5;">
            <div class="dropup">
                <div style="color: #666; font-size: 10px;">SELECTION A ▲</div>
                <div class="dropup-content">
                    <a>Option 1</a><a>Option 2</a><a>Option 3</a>
                </div>
            </div>
        </div>

        <!-- YELLOW AREA (Small Footer Buttons) -->
        <div class="footer-item" style="flex: 1.5;">
            <div id="footer-btn-grid" class="footer-btn-grid"></div>
        </div>

        <!-- RED AREA (Right Drop-up) -->
        <div class="footer-item" style="flex: 1; border-right: none;">
            <div class="dropup">
                <div style="color: #666; font-size: 10px;">SELECTION B ▲</div>
                <div class="dropup-content">
                    <a>Setting 1</a><a>Setting 2</a>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
    Split(['#left-side-stack', '#ai-column'], { sizes: [70, 30], gutterSize: 4 });
    Split(['#cad-pane', '#cmd-pane'], { direction: 'vertical', sizes: [80, 20], gutterSize: 4 });
    Split(['#ai-output', '#ai-input'], { direction: 'vertical', sizes: [50, 50], gutterSize: 4 });

    // Fill Sidebar Buttons (Yellow Area)
    const side = document.getElementById('side-strip');
    for(let i=0; i<40; i++) {
        side.innerHTML += '<div class="btn-cell" onclick="console.log(\'Btn \'+'+i+')"></div>';
    }
    
    // Fill Footer Grid Buttons (Yellow Area)
    const footGrid = document.getElementById('footer-btn-grid');
    for(let i=0; i<12; i++) {
        footGrid.innerHTML += '<div class="btn-cell" onclick="console.log(\'Foot \'+'+i+')"></div>';
    }
</script>
"""

# Re-anchor for visibility
components.html(cad_app_html, height=0)
st.components.v1.html(
    f"""<script>
        window.parent.document.querySelector('iframe').style.height = '94vh';
    </script>""",
    height=0
)
