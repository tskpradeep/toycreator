import streamlit as st
import streamlit.components.v1 as components

# 1. Page Configuration
st.set_page_config(layout="wide", page_title="CAD Design Portal")

# 2. CSS to clean up the Streamlit interface and prevent outer scrolling
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stApp { overflow: hidden !important; }
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
        overflow: hidden !important; background-color: #333; 
        font-family: 'Segoe UI', sans-serif;
    }
    
    .master-container { 
        display: flex; flex-direction: column; 
        height: 100vh; width: 100vw; background: white;
    }

    .window-title-bar {
        background: #2c3e50; color: white; height: 30px;
        flex-shrink: 0; display: flex; align-items: center; 
        justify-content: space-between; padding: 0 10px; font-size: 12px;
    }

    /* Resizable Workspace */
    #dynamic-zone { 
        display: flex; flex-direction: row; flex: 1; 
        min-height: 0; width: 100%;
    }

    .flex-row { display: flex; flex-direction: row; height: 100%; width: 100%; overflow: hidden; }
    .flex-col { display: flex; flex-direction: column; height: 100%; width: 100%; overflow: hidden; }
    
    .pane { 
        background: white; border: 1px solid black; 
        display: flex; align-items: center; justify-content: center; 
        overflow: hidden; padding: 5px; 
    }

    /* COMMAND PROMPT: Solid Black and Blank as requested */
    #cmd-pane {
        background-color: black !important;
        color: white;
        justify-content: flex-start;
        align-items: flex-start;
        padding: 10px;
    }
    
    /* Gutters */
    .gutter { background-color: #eee; flex-shrink: 0; }
    .gutter.gutter-horizontal { cursor: col-resize; background-color: red; width: 4px !important; }
    .gutter.gutter-vertical { cursor: row-resize; background-color: green; height: 4px !important; }

    /* YELLOW REQUEST: 2-Column Button Strip */
    .fixed-right-strip { 
        width: 60px; /* Widened for 2 columns */
        border-left: 2px solid black; 
        display: grid;
        grid-template-columns: 1fr 1fr;
        grid-auto-rows: min-content;
        gap: 4px;
        padding: 5px; 
        background: white;
        overflow-y: auto;
    }

    /* BLUE REQUEST: Footer Layout */
    .fixed-footer { 
        height: 75px; display: flex; flex-direction: row; 
        border-top: 2px solid black; background: white; flex-shrink: 0; 
    }

    .footer-item { border-right: 1px solid black; display: flex; align-items: center; justify-content: center; padding: 5px; font-size: 11px; }
    
    /* Small Button Boxes */
    .small-box { width: 18px; height: 18px; border: 1px solid black; background: #eee; flex-shrink: 0; }
    
    /* Grid for moved buttons in footer */
    .footer-btn-grid {
        display: grid; grid-template-columns: repeat(6, 1fr); 
        gap: 2px; padding: 5px; align-items: center;
    }

    .text-main { color: darkred; font-size: 1.4vw; font-weight: bold; text-align: center; border: none !important; }
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
                <div id="cmd-pane" class="pane">
                    <code style="color: #00FF00; font-family: monospace;">>_</code>
                </div>
            </div>
            <div id="ai-column" class="flex-col">
                <div id="ai-output" class="pane" style="color: green; font-weight: bold;">AI TEXT REPLYING WINDOW</div>
                <div id="ai-input" class="pane" style="color: purple; font-weight: bold;">USER PROMPTING</div>
            </div>
        </div>
        <!-- Right Sidebar with 2 columns -->
        <div class="fixed-right-strip" id="side-strip"></div>
    </div>

    <!-- RESTRUCTURED FOOTER per Blue marking -->
    <div class="fixed-footer">
        <div class="footer-item" style="flex: 1.5; color: green;">small indicators</div>
        <div class="footer-item" style="flex: 3; color: blue;">buttons for controlling...</div>
        <div class="footer-item" style="flex: 1.5;" id="moved-btns-grid" class="footer-btn-grid">
            <!-- Buttons moved here from far right -->
        </div>
        <div class="footer-item" style="flex: 1; border-right: none;"></div> <!-- Empty corner -->
    </div>
</div>

<script>
    Split(['#left-side-stack', '#ai-column'], { sizes: [70, 30], gutterSize: 4 });
    Split(['#cad-pane', '#cmd-pane'], { direction: 'vertical', sizes: [80, 20], gutterSize: 4 });
    Split(['#ai-output', '#ai-input'], { direction: 'vertical', sizes: [50, 50], gutterSize: 4 });

    // Populate Side Strip (2 columns)
    const side = document.getElementById('side-strip');
    for(let i=0; i<30; i++) side.innerHTML += '<div class="small-box"></div>';
    
    // Populate Footer Grid (Blue Request)
    const foot = document.getElementById('moved-btns-grid');
    for(let i=0; i<12; i++) foot.innerHTML += '<div class="small-box"></div>';
</script>
"""

# Force height to 90% of user's screen to ensure footer visibility
components.html(cad_app_html, height=0)
st.components.v1.html(
    f"""<script>
        window.parent.document.querySelector('iframe').style.height = '92vh';
    </script>""",
    height=0
)
