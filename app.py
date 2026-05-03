import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# This code uses Split.js to enable real mouse dragging for the red and green lines
draggable_html = """
<script src="https://cdnjs.cloudflare.com/ajax/libs/split.js/1.6.0/split.min.js"></script>
<style>
    body { margin: 0; background-color: white; font-family: sans-serif; height: 100vh; overflow: hidden; }
    
    /* Layout Containers */
    .flex-row { display: flex; flex-direction: row; height: 100%; width: 100%; }
    .flex-col { display: flex; flex-direction: column; height: 100%; width: 100%; }
    
    /* Panes */
    .pane { background: white; border: 2px solid black; box-sizing: border-box; 
            display: flex; align-items: center; justify-content: center; overflow: hidden; padding: 10px; }
    
    /* Gutter (The Draggable Lines) */
    .gutter { background-color: #eee; background-repeat: no-repeat; background-position: center; }
    .gutter.gutter-horizontal { cursor: col-resize; background-color: red; width: 10px !important; }
    .gutter.gutter-vertical { cursor: row-resize; background-color: green; height: 10px !important; }

    /* Content Styles */
    .text-main { color: darkred; font-size: 2vw; font-weight: bold; text-align: center; }
    .text-ai { color: green; font-weight: bold; }
    .text-prompt { color: purple; font-weight: bold; }
    
    /* Button Grids */
    .sidebar-btns { width: 50px; border-left: 2px solid black; display: flex; flex-direction: column; padding: 5px; background: white; }
    .footer-btns { display: grid; grid-template-columns: repeat(6, 1fr); gap: 2px; padding: 5px; }
    .small-box { width: 20px; height: 20px; border: 1px solid black; background: #f0f0f0; margin-bottom: 4px; }
</style>

<div class="flex-col" id="vertical-stack">
    <!-- TOP SECTION -->
    <div id="top-section" class="flex-row">
        <div id="cad-pane" class="pane text-main">
            visual displays dynamic between coding and screen/CAD designs
        </div>
        <div id="ai-sidebar" class="flex-col">
            <div id="ai-top" class="pane text-ai">AI TEXT REPLYING WINDOW</div>
            <div id="ai-bottom" class="pane text-prompt">USER PROMPTING</div>
        </div>
        <div class="sidebar-btns" id="side-strip"></div>
    </div>

    <!-- BOTTOM SECTION -->
    <div id="bottom-section" class="flex-col" style="background: white; border-top: 2px solid black;">
        <div style="padding: 10px; color: darkred; font-family: monospace;">command prompt for system programming for project >_</div>
        <div class="flex-row" style="height: 60px;">
            <div class="pane" style="flex: 1; color: green;">small indicators any</div>
            <div class="pane" style="flex: 3; color: blue;">buttons for controlling we will decide buttons as and when we</div>
            <div id="footer-grid" class="footer-btns"></div>
        </div>
    </div>
</div>

<script>
    // 1. Initialize Horizontal Split (The Red Line)
    Split(['#cad-pane', '#ai-sidebar'], {
        sizes: [70, 30],
        minSize: 100,
        gutterSize: 10,
        cursor: 'col-resize',
    });

    // 2. Initialize Vertical Split inside AI Sidebar (Upper Green Line)
    Split(['#ai-top', '#ai-bottom'], {
        direction: 'vertical',
        sizes: [50, 50],
        gutterSize: 10,
    });

    // 3. Initialize Main Vertical Split (Lower Green Line)
    Split(['#top-section', '#bottom-section'], {
        direction: 'vertical',
        sizes: [75, 25],
        gutterSize: 10,
    });

    // Generate Buttons
    const side = document.getElementById('side-strip');
    for(let i=0; i<15; i++) side.innerHTML += '<div class="small-box"></div>';
    
    const foot = document.getElementById('footer-grid');
    for(let i=0; i<12; i++) foot.innerHTML += '<div class="small-box"></div>';
</script>
"""

# Increase height to 900 to ensure it fills the page
components.html(draggable_html, height=900)
