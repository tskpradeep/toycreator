import streamlit as st
import streamlit.components.v1 as components

# 1. Page Configuration
st.set_page_config(layout="wide", page_title="CAD Design Portal")

# 2. Strict CSS to kill Streamlit's internal scrolling and padding
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {
            padding: 0rem !important;
            max-width: 100% !important;
            height: 100vh !important;
            overflow: hidden !important;
        }
        iframe {
            display: block;
        }
    </style>
""", unsafe_allow_html=True)

# 3. The Refined Application Logic
cad_app_html = """
<script src="https://cdnjs.cloudflare.com/ajax/libs/split.js/1.6.0/split.min.js"></script>
<style>
    /* Force absolute zero scroll on the browser level */
    html, body { 
        margin: 0; 
        padding: 0; 
        height: 100vh; 
        width: 100vw; 
        overflow: hidden !important; 
        background-color: white; 
        font-family: 'Segoe UI', sans-serif;
    }
    
    .master-container { 
        display: flex; 
        flex-direction: column; 
        height: 100vh; 
        width: 100vw; 
    }

    .window-title-bar {
        background: #2c3e50;
        color: white;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 10px;
        flex-shrink: 0;
    }

    /* Layout Sections */
    .flex-row { display: flex; flex-direction: row; width: 100%; overflow: hidden; }
    .flex-col { display: flex; flex-direction: column; height: 100%; overflow: hidden; }
    
    .pane { 
        background: white; 
        border: 1px solid black; 
        display: flex; 
        align-items: center; 
        justify-content: center; 
        overflow: hidden; 
        padding: 5px; 
    }
    
    /* Gutter Styling (The Draggable Lines) */
    .gutter { background-color: #eee; flex-shrink: 0; }
    .gutter.gutter-horizontal { cursor: col-resize; background-color: red; width: 4px !important; }
    .gutter.gutter-vertical { cursor: row-resize; background-color: green; height: 4px !important; }

    /* Fixed Sections */
    .fixed-right-strip { 
        width: 40px; 
        border-left: 2px solid black; 
        display: flex; 
        flex-direction: column; 
        padding: 2px; 
        align-items: center; 
        flex-shrink: 0; /* Ensures it never resizes */
        background: white;
    }

    .fixed-footer { 
        height: 70px; 
        display: flex; 
        flex-direction: row; 
        border-top: 2px solid black; 
        background: white; 
        flex-shrink: 0; 
    }

    /* Content Text */
    .text-main { color: darkred; font-size: 1.5vw; font-weight: bold; text-align: center; border: none !important; }
    .text-ai { color: green; font-weight: bold; border: none !important; }
    
    /* UI Elements */
    .footer-grid { display: grid; grid-template-columns: repeat(6, 1fr); gap: 2px; padding: 5px; width: 140px; }
    .small-box { width: 16px; height: 16px; border: 1px solid black; background: #eee; margin-bottom: 2px; flex-shrink: 0; }

    #dynamic-zone { flex-grow: 1; min-height: 0; }
</style>

<div class="master-container">
    <div class="window-title-bar">
        <div style="font-size: 12px;">CAD DESIGNER PRO - FIXED LAYOUT</div>
        <div style="font-size: 14px;"><span>−</span><span style="margin:0 10px;">❐</span><span>×</span></div>
    </div>

    <div id="dynamic-zone" class="flex-row">
        <!-- THE MOVABLE WORKSPACE -->
        <div id="split-container" class="flex-row" style="flex-grow: 1;">
            <!-- LEFT PILLAR -->
            <div id="left-side-stack" class="flex-col">
                <div id="cad-pane" class="pane text-main">
                    visual displays dynamic between coding and screen/CAD designs
                </div>
                <div id="cmd-pane" class="pane" style="justify-content: flex-start; align-items: flex-start; border-top: 2px solid black;">
                    <code style="color: darkred; font-weight: bold; font-size: 12px;">command prompt for system programming for project >_</code>
                </div>
            </div>

            <!-- RIGHT PILLAR (AI ONLY) -->
            <div id="ai-column" class="flex-col">
                <div id="ai-output" class="pane text-ai">AI TEXT REPLYING WINDOW</div>
                <div id="ai-input" class="pane" style="color: purple; font-weight: bold;">USER PROMPTING</div>
            </div>
        </div>

        <!-- FIXED SIDEBAR (Outside the Split) -->
        <div class="fixed-right-strip" id="side-strip"></div>
    </div>

    <!-- FIXED FOOTER -->
    <div class="fixed-footer">
        <div style="flex: 1.5; border-right: 1px solid black; display: flex; align-items: center; justify-content: center; color: green; font-size: 12px;">small indicators any</div>
        <div style="flex: 4; border-right: 1px solid black; display: flex; align-items: center; justify-content: center; color: blue; font-size: 12px; padding: 0 10px;">buttons for controlling we will decide buttons as and when we</div>
        <div id="footer-grid" class="footer-grid"></div>
    </div>
</div>

<script>
    // Split ONLY the workspace, leaving the Right Sidebar alone
    Split(['#left-side-stack', '#ai-column'], {
        sizes: [72, 28],
        gutterSize: 4,
        cursor: 'col-resize',
    });

    Split(['#cad-pane', '#cmd-pane'], {
        direction: 'vertical',
        sizes: [78, 22],
        gutterSize: 4,
    });

    Split(['#ai-output', '#ai-input'], {
        direction: 'vertical',
        sizes: [50, 50],
        gutterSize: 4,
    });

    // Populate Buttons
    const side = document.getElementById('side-strip');
    for(let i=0; i<25; i++) side.innerHTML += '<div class="small-box"></div>';
    const foot = document.getElementById('footer-grid');
    for(let i=0; i<12; i++) foot.innerHTML += '<div class="small-box"></div>';
</script>
"""

# Using 100vh height for the component
components.html(cad_app_html, height=1000)
