import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# The unified layout with Split.js
final_layout_html = """
<script src="https://cdnjs.cloudflare.com/ajax/libs/split.js/1.6.0/split.min.js"></script>
<style>
    body { margin: 0; background-color: white; font-family: sans-serif; height: 100vh; width: 100vw; overflow: hidden; }
    
    /* Main wrapper to remove all outer black borders */
    .master-container { display: flex; flex-direction: column; height: 100vh; width: 100vw; }

    /* Layout Containers */
    .flex-row { display: flex; flex-direction: row; width: 100%; height: 100%; }
    .flex-col { display: flex; flex-direction: column; width: 100%; height: 100%; }
    
    /* Panes */
    .pane { background: white; border: 1px solid black; box-sizing: border-box; 
            display: flex; align-items: center; justify-content: center; overflow: hidden; padding: 10px; }
    
    /* Slimmed down Gutters (The Lines) */
    .gutter { background-color: #eee; background-repeat: no-repeat; background-position: center; }
    .gutter.gutter-horizontal { cursor: col-resize; background-color: red; width: 6px !important; }
    .gutter.gutter-vertical { cursor: row-resize; background-color: green; height: 6px !important; }

    /* Content Text Styles */
    .text-main { color: darkred; font-size: 1.8vw; font-weight: bold; text-align: center; border: none !important; }
    .text-ai { color: green; font-weight: bold; border: none !important; }
    .text-prompt { color: purple; font-weight: bold; border: none !important; }
    
    /* The Fixed Bottom Section (Below the imaginary brown line) */
    .fixed-footer { height: 80px; display: flex; flex-direction: row; border-top: 2px solid black; background: white; }
    .footer-item { border-right: 2px solid black; display: flex; align-items: center; justify-content: center; padding: 5px; }

    /* Button Grids */
    .sidebar-btns { width: 45px; border-left: 2px solid black; display: flex; flex-direction: column; padding: 4px; background: white; }
    .footer-grid { display: grid; grid-template-columns: repeat(6, 1fr); gap: 2px; padding: 5px; width: 160px; }
    .small-box { width: 18px; height: 18px; border: 1px solid black; background: #f0f0f0; margin-bottom: 3px; }
</style>

<div class="master-container">
    <!-- DYNAMIC AREA (Above the brown line) -->
    <div id="dynamic-zone" class="flex-row">
        
        <!-- LEFT SIDE: CAD + Command Prompt (Unified by the Red Line) -->
        <div id="left-side-stack" class="flex-col">
            <div id="cad-pane" class="pane text-main" style="border: 1px solid #ccc;">
                visual displays dynamic between coding and screen/CAD designs
            </div>
            <div id="cmd-pane" class="pane" style="justify-content: flex-start; align-items: flex-start; border-top: 2px solid black;">
                <code style="color: darkred; font-weight: bold;">command prompt for system programming for project >_</code>
            </div>
        </div>

        <!-- RIGHT SIDE: AI + Right Button Strip -->
        <div id="right-side-stack" class="flex-row">
            <div id="ai-column" class="flex-col">
                <div id="ai-output" class="pane text-ai">AI TEXT REPLYING WINDOW</div>
                <div id="ai-input" class="pane text-prompt">USER PROMPTING</div>
            </div>
            <div class="sidebar-btns" id="side-strip"></div>
        </div>
    </div>

    <!-- FIXED FOOTER (The base indicators and buttons) -->
    <div class="fixed-footer">
        <div class="footer-item" style="flex: 1.5; color: green; font-size: 0.9vw;">small indicators any</div>
        <div class="footer-item" style="flex: 4; color: blue; font-size: 0.9vw; border-right: 2px solid black;">
            buttons for controlling we will decide buttons as and when we
        </div>
        <div id="footer-grid" class="footer-grid"></div>
    </div>
</div>

<script>
    // 1. MAIN VERTICAL SPLIT (The Red Line)
    // This moves the Left Stack (CAD+CMD) and Right Stack (AI+Btns) together
    Split(['#left-side-stack', '#right-side-stack'], {
        sizes: [70, 30],
        gutterSize: 6,
        cursor: 'col-resize',
    });

    // 2. CAD vs COMMAND PROMPT SPLIT (Lower Green Line)
    // Moves ONLY between CAD and CMD windows
    Split(['#cad-pane', '#cmd-pane'], {
        direction: 'vertical',
        sizes: [80, 20],
        gutterSize: 6,
    });

    // 3. AI TOP vs AI BOTTOM SPLIT (Upper Green Line)
    Split(['#ai-output', '#ai-input'], {
        direction: 'vertical',
        sizes: [50, 50],
        gutterSize: 6,
    });

    // Generate Buttons
    const side = document.getElementById('side-strip');
    for(let i=0; i<18; i++) side.innerHTML += '<div class="small-box"></div>';
    
    const foot = document.getElementById('footer-grid');
    for(let i=0; i<12; i++) foot.innerHTML += '<div class="small-box"></div>';
</script>
"""

components.html(final_layout_html, height=900, scrolling=False)
