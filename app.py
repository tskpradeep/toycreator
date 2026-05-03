import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="CAD Design Portal")

# The layout now includes a simulated OS-style Title Bar
cad_app_html = """
<script src="https://cdnjs.cloudflare.com/ajax/libs/split.js/1.6.0/split.min.js"></script>
<style>
    /* Reset and Dynamic Sizing */
    * { box-sizing: border-box; }
    body { 
        margin: 0; 
        background-color: #f0f0f0; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
        height: 100vh; 
        width: 100vw; 
        overflow: hidden; 
        display: flex;
        flex-direction: column;
    }
    
    /* 1. TOP WINDOW BAR (Minimize, Maximize, Close) */
    .window-title-bar {
        background: #2c3e50;
        color: white;
        height: 35px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 10px;
        user-select: none;
        border-bottom: 1px solid #1a252f;
    }
    .window-title { font-size: 14px; font-weight: 600; }
    .window-controls { display: flex; gap: 15px; }
    .control-btn { cursor: pointer; font-size: 16px; width: 20px; text-align: center; }
    .control-btn:hover { color: #bdc3c7; }
    .close-btn:hover { color: #e74c3c; }

    /* 2. MAIN APP CONTAINER */
    .master-container { 
        display: flex; 
        flex-direction: column; 
        flex-grow: 1; 
        height: calc(100vh - 35px); 
        width: 100vw; 
        background: white;
    }

    .flex-row { display: flex; flex-direction: row; width: 100%; height: 100%; }
    .flex-col { display: flex; flex-direction: column; width: 100%; height: 100%; }
    
    /* Panes */
    .pane { background: white; border: 1px solid black; display: flex; align-items: center; justify-content: center; overflow: hidden; padding: 10px; }
    
    /* Slimmed Dividers */
    .gutter { background-color: #f8f9fa; background-repeat: no-repeat; background-position: center; }
    .gutter.gutter-horizontal { cursor: col-resize; background-color: red; width: 5px !important; }
    .gutter.gutter-vertical { cursor: row-resize; background-color: green; height: 5px !important; }

    /* Content Text */
    .text-main { color: darkred; font-size: 1.8vw; font-weight: bold; text-align: center; border: none !important; }
    .text-ai { color: green; font-weight: bold; border: none !important; }
    .text-prompt { color: purple; font-weight: bold; border: none !important; }
    
    /* Fixed Bottom Base */
    .fixed-footer { height: 75px; display: flex; flex-direction: row; border-top: 2px solid black; background: white; }
    .footer-item { border-right: 1px solid black; display: flex; align-items: center; justify-content: center; padding: 5px; }

    /* Buttons */
    .sidebar-btns { width: 45px; border-left: 2px solid black; display: flex; flex-direction: column; padding: 4px; background: white; }
    .footer-grid { display: grid; grid-template-columns: repeat(6, 1fr); gap: 2px; padding: 5px; width: 150px; }
    .small-box { width: 18px; height: 18px; border: 1px solid black; background: #f0f0f0; margin-bottom: 3px; }
</style>

<!-- WINDOW TITLE BAR -->
<div class="window-title-bar">
    <div class="window-title">CAD Tool Portal - Professional Edition</div>
    <div class="window-controls">
        <span class="control-btn">−</span>
        <span class="control-btn">❐</span>
        <span class="control-btn close-btn">×</span>
    </div>
</div>

<!-- MAIN DASHBOARD -->
<div class="master-container">
    <div id="dynamic-zone" class="flex-row">
        
        <!-- LEFT PILLAR -->
        <div id="left-side-stack" class="flex-col">
            <div id="cad-pane" class="pane text-main">
                visual displays dynamic between coding and screen/CAD designs
            </div>
            <div id="cmd-pane" class="pane" style="justify-content: flex-start; align-items: flex-start; border-top: 2px solid black;">
                <code style="color: darkred; font-weight: bold;">command prompt for system programming for project >_</code>
            </div>
        </div>

        <!-- RIGHT PILLAR -->
        <div id="right-side-stack" class="flex-row">
            <div id="ai-column" class="flex-col">
                <div id="ai-output" class="pane text-ai">AI TEXT REPLYING WINDOW</div>
                <div id="ai-input" class="pane text-prompt">USER PROMPTING</div>
            </div>
            <div class="sidebar-btns" id="side-strip"></div>
        </div>
    </div>

    <!-- BOTTOM FIXED BASE -->
    <div class="fixed-footer">
        <div class="footer-item" style="flex: 1.5; color: green; font-size: 13px;">small indicators any</div>
        <div class="footer-item" style="flex: 4; color: blue; font-size: 13px;">
            buttons for controlling we will decide buttons as and when we
        </div>
        <div id="footer-grid" class="footer-grid"></div>
    </div>
</div>

<script>
    // Maintain the 1:1 Dynamic Logic
    Split(['#left-side-stack', '#right-side-stack'], {
        sizes: [70, 30],
        gutterSize: 5,
        cursor: 'col-resize',
    });

    Split(['#cad-pane', '#cmd-pane'], {
        direction: 'vertical',
        sizes: [75, 25],
        gutterSize: 5,
    });

    Split(['#ai-output', '#ai-input'], {
        direction: 'vertical',
        sizes: [50, 50],
        gutterSize: 5,
    });

    const side = document.getElementById('side-strip');
    for(let i=0; i<18; i++) side.innerHTML += '<div class="small-box"></div>';
    const foot = document.getElementById('footer-grid');
    for(let i=0; i<12; i++) foot.innerHTML += '<div class="small-box"></div>';
</script>
"""

# Render with height set to occupy 100% of the Streamlit container
components.html(cad_app_html, height=1000, scrolling=False)
