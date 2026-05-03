import streamlit as st
import streamlit.components.v1 as components

# 1. Force the Streamlit page to wide mode
st.set_page_config(layout="wide", page_title="CAD Design Portal")

# 2. Corrected CSS block to hide Streamlit elements
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        /* This removes the extra padding around the app */
        .block-container {
            padding: 0rem !important;
            max-width: 100% !important;
        }
        /* This prevents the browser from showing any scrollbars on the main page */
        html, body {
            overflow: hidden;
        }
    </style>
""", unsafe_allow_html=True)

# 3. The Application Logic
cad_app_html = """
<script src="https://cdnjs.cloudflare.com/ajax/libs/split.js/1.6.0/split.min.js"></script>
<style>
    /* Force the internal window to be exactly the size of the browser */
    html, body { 
        margin: 0; 
        padding: 0; 
        height: 100vh; 
        width: 100vw; 
        overflow: hidden; 
        background-color: white; 
        font-family: 'Segoe UI', sans-serif;
    }
    
    .master-container { 
        display: flex; 
        flex-direction: column; 
        height: 100vh; 
        width: 100vw; 
    }

    /* Top Window Bar */
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
    .window-controls span { margin-left: 10px; cursor: pointer; }

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
    .gutter { background-color: #eee; }
    .gutter.gutter-horizontal { cursor: col-resize; background-color: red; width: 4px !important; }
    .gutter.gutter-vertical { cursor: row-resize; background-color: green; height: 4px !important; }

    /* Text Formatting */
    .text-main { color: darkred; font-size: 1.5vw; font-weight: bold; text-align: center; border: none !important; }
    .text-ai { color: green; font-weight: bold; border: none !important; font-size: 14px; }
    .text-prompt { color: purple; font-weight: bold; border: none !important; font-size: 14px; }
    
    /* Fixed Bottom Base */
    .fixed-footer { 
        height: 70px; 
        display: flex; 
        flex-direction: row; 
        border-top: 2px solid black; 
        background: white; 
        flex-shrink: 0; 
    }
    .footer-item { border-right: 1px solid black; display: flex; align-items: center; justify-content: center; padding: 5px; font-size: 12px; }

    /* Button Columns */
    .sidebar-btns { width: 40px; border-left: 2px solid black; display: flex; flex-direction: column; padding: 2px; align-items: center; }
    .footer-grid { display: grid; grid-template-columns: repeat(6, 1fr); gap: 2px; padding: 5px; width: 140px; }
    .small-box { width: 16px; height: 16px; border: 1px solid black; background: #eee; margin-bottom: 2px; flex-shrink: 0; }

    #dynamic-zone { flex-grow: 1; }
</style>

<div class="master-container">
    <div class="window-title-bar">
        <div style="font-size: 12px;">CAD DESIGNER PRO - LANDSCAPE MODE</div>
        <div class="window-controls"><span>−</span><span>❐</span><span>×</span></div>
    </div>

    <div id="dynamic-zone" class="flex-row">
        <div id="left-side-stack" class="flex-col">
            <div id="cad-pane" class="pane text-main">
                visual displays dynamic between coding and screen/CAD designs
            </div>
            <div id="cmd-pane" class="pane" style="justify-content: flex-start; align-items: flex-start; border-top: 2px solid black;">
                <code style="color: darkred; font-weight: bold; font-size: 12px;">command prompt for system programming for project >_</code>
            </div>
        </div>

        <div id="right-side-stack" class="flex-row">
            <div id="ai-column" class="flex-col">
                <div id="ai-output" class="pane text-ai">AI TEXT REPLYING WINDOW</div>
                <div id="ai-input" class="pane text-prompt">USER PROMPTING</div>
            </div>
            <div class="sidebar-btns" id="side-strip"></div>
        </div>
    </div>

    <div class="fixed-footer">
        <div class="footer-item" style="flex: 1.5; color: green;">small indicators any</div>
        <div class="footer-item" style="flex: 4; color: blue;">buttons for controlling we will decide buttons as and when we</div>
        <div id="footer-grid" class="footer-grid"></div>
    </div>
</div>

<script>
    Split(['#left-side-stack', '#right-side-stack'], {
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

    const side = document.getElementById('side-strip');
    for(let i=0; i<25; i++) side.innerHTML += '<div class="small-box"></div>';
    const foot = document.getElementById('footer-grid');
    for(let i=0; i<12; i++) foot.innerHTML += '<div class="small-box"></div>';
</script>
"""

# Render with 100vh height
components.html(cad_app_html, height=1000)
