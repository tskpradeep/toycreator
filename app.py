import streamlit as st
import streamlit.components.v1 as components

# 1. Page Configuration
st.set_page_config(layout="wide", page_title="CAD Design Portal")

# 2. Ultra-Strict CSS to force everything into the visible area
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        /* Force the Streamlit container to be exactly 100% of the screen */
        .main {
            overflow: hidden !important;
        }
        .block-container {
            padding: 0rem !important;
            max-width: 100% !important;
            height: 100vh !important;
            overflow: hidden !important;
            display: flex;
            flex-direction: column;
        }
        /* Remove extra spacing Streamlit adds at the top */
        .stApp {
            height: 100vh !important;
            overflow: hidden !important;
        }
    </style>
""", unsafe_allow_html=True)

# 3. The Layout Logic
cad_app_html = """
<script src="https://cdnjs.cloudflare.com/ajax/libs/split.js/1.6.0/split.min.js"></script>
<style>
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
        border: 1px solid #333; /* Visual frame */
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

    /* THE DYNAMIC ZONE: 
       We subtract the Title bar (30px) and Footer (70px) from the total 100vh 
    */
    #dynamic-zone { 
        display: flex;
        flex-direction: row;
        height: calc(100vh - 100px); 
        width: 100%;
        overflow: hidden;
        min-height: 0;
    }

    .flex-row { display: flex; flex-direction: row; height: 100%; overflow: hidden; }
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
    
    /* Gutter Styling */
    .gutter { background-color: #eee; flex-shrink: 0; }
    .gutter.gutter-horizontal { cursor: col-resize; background-color: red; width: 4px !important; }
    .gutter.gutter-vertical { cursor: row-resize; background-color: green; height: 4px !important; }

    /* Fixed Sidebar */
    .fixed-right-strip { 
        width: 40px; 
        border-left: 2px solid black; 
        display: flex; 
        flex-direction: column; 
        padding: 2px; 
        align-items: center; 
        flex-shrink: 0;
        background: white;
    }

    /* Fixed Footer (The Floor) */
    .fixed-footer { 
        height: 70px; 
        display: flex; 
        flex-direction: row; 
        border-top: 2px solid black; 
        background: white; 
        flex-shrink: 0; /* Important: prevents footer from disappearing */
    }

    .text-main { color: darkred; font-size: 1.5vw; font-weight: bold; text-align: center; border: none !important; }
    .footer-grid { display: grid; grid-template-columns: repeat(6, 1fr); gap: 2px; padding: 5px; width: 140px; }
    .small-box { width: 16px; height: 16px; border: 1px solid black; background: #eee; margin-bottom: 2px; flex-shrink: 0; }
</style>

<div class="master-container">
    <div class="window-title-bar">
        <div style="font-size: 12px;">CAD DESIGNER PRO - LOCKED VIEW</div>
        <div style="font-size: 14px;"><span>−</span><span style="margin:0 10px;">❐</span><span>×</span></div>
    </div>

    <div id="dynamic-zone">
        <div id="split-container" class="flex-row" style="flex-grow: 1;">
            <div id="left-side-stack" class="flex-col">
                <div id="cad-pane" class="pane text-main">
                    visual displays dynamic between coding and screen/CAD designs
                </div>
                <div id="cmd-pane" class="pane" style="justify-content: flex-start; align-items: flex-start; border-top: 2px solid black;">
                    <code style="color: darkred; font-weight: bold; font-size: 12px;">command prompt for system programming for project >_</code>
                </div>
            </div>

            <div id="ai-column" class="flex-col">
                <div id="ai-output" class="pane" style="color: green; font-weight: bold;">AI TEXT REPLYING WINDOW</div>
                <div id="ai-input" class="pane" style="color: purple; font-weight: bold;">USER PROMPTING</div>
            </div>
        </div>
        <div class="fixed-right-strip" id="side-strip"></div>
    </div>

    <div class="fixed-footer">
        <div style="flex: 1.5; border-right: 1px solid black; display: flex; align-items: center; justify-content: center; color: green; font-size: 11px;">small indicators any</div>
        <div style="flex: 4; border-right: 1px solid black; display: flex; align-items: center; justify-content: center; color: blue; font-size: 11px; padding: 0 10px;">buttons for controlling we will decide buttons as and when we</div>
        <div id="footer-grid" class="footer-grid"></div>
    </div>
</div>

<script>
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

    const side = document.getElementById('side-strip');
    for(let i=0; i<25; i++) side.innerHTML += '<div class="small-box"></div>';
    const foot = document.getElementById('footer-grid');
    for(let i=0; i<12; i++) foot.innerHTML += '<div class="small-box"></div>';
</script>
"""

# Streamlit Component Call
components.html(cad_app_html, height=1000)
