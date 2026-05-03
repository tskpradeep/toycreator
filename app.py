import streamlit as st
import streamlit.components.v1 as components

# Set page to wide to use the whole screen
st.set_page_config(layout="wide")

# This is the Raw Layout matching image_0d35a5.png
# It uses "Flexbox" which is the professional way to make windows resizable
custom_html = """
<style>
    body { margin: 0; background-color: #111; color: white; font-family: sans-serif; overflow: hidden; }
    .container { display: flex; flex-direction: column; height: 95vh; width: 100vw; border: 5px solid #333; }
    
    /* Top Section */
    .top-section { display: flex; flex: 7; min-height: 0; }
    
    .visual-display { flex: 6; border: 3px solid black; background: white; color: darkred; 
                       display: flex; align-items: center; justify-content: center; 
                       font-size: 2vw; font-weight: bold; text-align: center; margin: 5px; }
                       
    .red-line { width: 10px; background: red; cursor: col-resize; }
    
    .ai-sidebar { flex: 3; display: flex; flex-direction: column; }
    .ai-window { flex: 1; border: 3px solid black; background: white; color: green; 
                 display: flex; align-items: center; justify-content: center; margin: 5px; font-weight: bold; }
    
    .green-line { height: 10px; background: green; cursor: row-resize; }
    
    .button-strip { width: 60px; border-left: 3px solid black; display: flex; flex-wrap: wrap; padding: 5px; align-content: flex-start; }
    .small-box { width: 25px; height: 25px; border: 1px solid black; margin: 2px; background: #eee; }

    /* Bottom Section */
    .bottom-section { flex: 3; display: flex; flex-direction: column; border-top: 10px solid green; background: #000; padding: 10px; }
    .command-prompt { flex: 1; color: darkred; font-family: monospace; margin-bottom: 10px; }
    .footer-row { display: flex; height: 60px; }
    .indicator { flex: 1; border: 2px solid black; color: green; background: white; padding: 5px; margin-right: 5px; }
    .controls { flex: 3; border: 2px solid black; color: blue; background: white; padding: 5px; margin-right: 5px; }
    .footer-btns { flex: 1; display: flex; flex-wrap: wrap; }
</style>

<div class="container">
    <div class="top-section">
        <div class="visual-display">visual displays dynamic between coding and screen/CAD designs</div>
        <div class="red-line"></div>
        <div class="ai-sidebar">
            <div class="ai-window">AI TEXT REPLYING WINDOW</div>
            <div class="green-line"></div>
            <div class="ai-window" style="color: purple;">USER PROMPTING</div>
        </div>
        <div class="button-strip" id="side-btns"></div>
    </div>
    
    <div class="bottom-section">
        <div class="command-prompt">command prompt for system programming for project >_</div>
        <div class="footer-row">
            <div class="indicator">small indicators any</div>
            <div class="controls">buttons for controlling we will decide buttons as and when we</div>
            <div class="footer-btns" id="foot-btns"></div>
        </div>
    </div>
</div>

<script>
    // Generate the small button boxes automatically
    const sideBtns = document.getElementById('side-btns');
    for(let i=0; i<18; i++) {
        let div = document.createElement('div');
        div.className = 'small-box';
        sideBtns.appendChild(div);
    }
    
    const footBtns = document.getElementById('foot-btns');
    for(let i=0; i<12; i++) {
        let div = document.createElement('div');
        div.className = 'small-box';
        footBtns.appendChild(div);
    }
</script>
"""

# Render the HTML inside Streamlit
components.html(custom_html, height=800, scrolling=False)
