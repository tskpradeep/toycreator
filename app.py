import streamlit as st
import streamlit.components.v1 as components

# 1. Page Configuration
st.set_page_config(layout="wide", page_title="CAD Design Portal")

# 2. Reset Streamlit interface
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

# 3. The Stabilized "Native-Feel" App
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

    /* Side Strip with Native Scrollbar */
    .fixed-right-strip { 
        width: 60px; border-left: 1px solid #333; 
        display: grid; grid-template-columns: 1fr 1fr;
        grid-auto-rows: min-content; gap: 2px;
        padding: 4px; background: #000; 
        overflow-y: scroll; /* Native scrollbar enabled */
    }

    /* Beveled Native Button */
    .btn-cell {
        aspect-ratio: 1 / 1; width: 100%;
        background: #e1e1e1; color: #000;
        border-top: 2px solid #fff; border-left: 2px solid #fff;
        border-right: 2px solid #707070; border-bottom: 2px solid #707070;
        cursor: pointer; display: flex; align-items: center; justify-content: center;
        box-sizing: border-box;
    }
    .btn-cell:active { 
        border-top: 2px solid #707070; border-left: 2px solid #707070;
        border-right: 2px solid #fff; border-bottom: 2px solid #fff;
        background: #bebebe;
    }

    /* Panes & Gutters */
    .pane { background: #000 !important; border: 1px solid #333 !important; overflow: hidden; display: flex; align-items: center; justify-content: center; box-sizing: border-box; }
    .gutter { background-color: #444 !important; }

    /* Footer Layout */
    .fixed-footer { 
        height: 80px; display: flex; flex-direction: row; 
        border-top: 2px solid #333; background: #000; flex-shrink: 0; 
    }
    .footer-item { border-right: 1px solid #333; display: flex; align-items: center; justify-content: center; padding: 2px; }

    /* Drop-up Styling */
    .dropup { 
        position: relative; width: 95%; height: 24px; 
        background: #e1e1e1; color: #000; border: 1px solid #707070; 
        display: flex; align-items: center; justify-content: space-between;
        padding: 0 5px; cursor: pointer; font-size: 10px;
    }
    .dropup-content {
        display: none; position: absolute; bottom: 100%; left: -1px;
        background-color: #f0f0f0; min-width: 140px; 
        border: 1px solid #707070; z-index: 1000;
    }
    .dropup.active .dropup-content { display: block; }
    .dropup-content a { color: #000; padding: 6px; text-decoration: none; display: block; border-bottom: 1px solid #ccc; }

    /* Specific palette grid for the footer */
    .footer-palette { 
        display: grid; grid-template-columns: repeat(8, 20px); gap: 2px; 
    }

    .text-main { color: #b22222; font-size: 1.4vw; font-weight: bold; text-align: center; }
</style>

<div class="master-container">
    <div class="window-title-bar">
        <div>CAD DESIGNER PRO</div>
        <div><span>−</span><span style="margin:0 10px;">❐</span><span>×</span></div>
    </div>

    <div id="dynamic-zone">
        <div id="split-container" style="display:flex; flex:1; width:100%;">
            <div id="left-side-stack" style="display:flex; flex-direction:column; width:70%;">
                <div id="cad-pane" class="pane text-main">visual displays dynamic between coding and screen/CAD designs</div>
                <div id="cmd-pane" class="pane" style="justify-content: flex-start; align-items: flex-start; color:#0f0; font-family:monospace;">>_</div>
            </div>
            <div id="ai-column" style="display:flex; flex-direction:column; width:30%;">
                <div id="ai-output" class="pane" style="color:#008000; font-weight:bold;">AI TEXT REPLYING WINDOW</div>
                <div id="ai-input" class="pane" style="color:#800080; font-weight:bold;">USER PROMPTING</div>
            </div>
        </div>
        <div class="fixed-right-strip" id="side-strip"></div>
    </div>

    <div class="fixed-footer">
        <div class="footer-item" style="flex: 1; color:#008000; font-size:10px;">small indicators</div>
        <div class="footer-item" style="flex: 2; color:#0000ff; font-size:10px;">buttons for controlling...</div>
        
        <div class="footer-item" style="flex: 1.5; flex-direction:column; gap:2px;">
            <div class="dropup" onclick="toggleMenu(this)"><span>Selection A</span><span>▲</span><div class="dropup-content"><a>Tool 1</a><a>Tool 2</a></div></div>
            <div class="dropup" onclick="toggleMenu(this)"><span>Selection A</span><span>▲</span><div class="dropup-content"><a>Data 1</a><a>Data 2</a></div></div>
        </div>

        <div class="footer-item" style="flex: 2;">
            <div id="foot-palette" class="footer-palette"></div>
        </div>

        <div class="footer-item" style="flex: 1.2; border-right:none;">
            <div class="dropup" onclick="toggleMenu(this)"><span>Selection B</span><span>▲</span><div class="dropup-content"><a>Settings</a><a>Export</a></div></div>
        </div>
    </div>
</div>

<script>
    Split(['#left-side-stack', '#ai-column'], { sizes: [70, 30], gutterSize: 4 });
    Split(['#cad-pane', '#cmd-pane'], { direction: 'vertical', sizes: [80, 20], gutterSize: 4 });
    Split(['#ai-output', '#ai-input'], { direction: 'vertical', sizes: [50, 50], gutterSize: 4 });

    // Sidebar: Fill with many buttons to trigger scroll
    const side = document.getElementById('side-strip');
    for(let i=0; i<80; i++) side.innerHTML += '<div class="btn-cell"></div>';
    
    // Footer: Palette grid
    const palette = document.getElementById('foot-palette');
    for(let i=0; i<24; i++) palette.innerHTML += '<div class="btn-cell"></div>';

    function toggleMenu(el) {
        const isActive = el.classList.contains('active');
        document.querySelectorAll('.dropup').forEach(d => d.classList.remove('active'));
        if(!isActive) el.classList.add('active');
    }

    window.onclick = function(event) {
        if (!event.target.closest('.dropup')) {
            document.querySelectorAll('.dropup').forEach(d => d.classList.remove('active'));
        }
    };
</script>
"""

components.html(cad_app_html, height=0)
st.components.v1.html(
    f"""<script>
        window.parent.document.querySelector('iframe').style.height = '94vh';
    </script>""",
    height=0
)
