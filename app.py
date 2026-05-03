import streamlit as st
import streamlit.components.v1 as components

# 1. Page Configuration
st.set_page_config(layout="wide", page_title="CAD Designer Pro")

# 2. Force CSS for Classic Style
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stApp { background-color: #000 !important; }
        .block-container { padding: 0rem !important; max-width: 100% !important; height: 100vh !important; }
    </style>
""", unsafe_allow_html=True)

# 3. Main Application Component
cad_app_html = """
<script src="https://cdnjs.cloudflare.com/ajax/libs/split.js/1.6.0/split.min.js"></script>
<style>
    html, body { 
        margin: 0; padding: 0; height: 100%; width: 100%; 
        overflow: hidden; background-color: #000; 
        font-family: 'Segoe UI', Tahoma, sans-serif; color: #fff;
    }
    
    .master-container { 
        display: flex; flex-direction: column; 
        height: 100vh; width: 100vw; background: #000;
        position: relative;
    }

    /* PANE STYLING */
    .pane { background: #000; border: 1px solid #333; overflow: hidden; display: flex; align-items: center; justify-content: center; }
    
    /* DULL MOVING WALLS (GUTTERS) */
    .gutter.gutter-horizontal { background-color: #331a1a !important; cursor: col-resize; } /* Dull Red */
    .gutter.gutter-vertical { background-color: #1a331a !important; cursor: row-resize; }   /* Dull Green */

    /* AI SETTING MODAL - GREEN VIBE */
    #ai-modal {
        position: absolute; top: 15%; left: 20%; width: 60%; height: 60%;
        background: #000; border: 2px solid #0f0; z-index: 9999;
        display: none; flex-direction: column; box-shadow: 0 0 30px rgba(0,255,0,0.3);
    }
    .modal-header { background: #0a1a0a; border-bottom: 1px solid #0f0; padding: 12px; display: flex; justify-content: space-between; color: #0f0; font-family: monospace; font-weight: bold; }
    .modal-body { display: flex; flex: 1; overflow: hidden; }
    .modal-sidebar { width: 35%; border-right: 1px solid #0f0; padding: 10px; background: #050505; overflow-y: auto; }
    .modal-content { width: 65%; padding: 20px; color: #0f0; font-family: monospace; display: flex; flex-direction: column; gap: 15px; background: #000; }
    
    .ai-item { padding: 10px; border: 1px solid #050; margin-bottom: 8px; cursor: pointer; font-size: 11px; color: #0f0; transition: 0.2s; }
    .ai-item:hover { background: #002200; border-color: #0f0; }
    .ai-item.active { background: #0f0; color: #000; font-weight: bold; }

    .api-link { color: #0f0; text-decoration: underline; font-size: 10px; cursor: pointer; margin-top: 5px; display: block; }
    .input-box { background: #000; border: 1px solid #0f0; color: #0f0; padding: 10px; width: 100%; box-sizing: border-box; outline: none; font-family: monospace; }
    .input-box:focus { box-shadow: 0 0 10px rgba(0,255,0,0.2); }

    /* FOOTER & BUTTONS - CLASIC DASHBOARD */
    .footer { height: 50px; background: #111; border-top: 1px solid #333; display: flex; align-items: center; padding: 0 15px; flex-shrink: 0; }
    .btn-classic { background: #222; border: 1px solid #444; color: #ccc; padding: 6px 18px; cursor: pointer; font-size: 12px; margin-right: 10px; outline: none; }
    .btn-classic:hover { background: #333; border-color: #666; }
    .btn-classic:active { background: #111; }
</style>

<div class="master-container">
    <!-- AI MODAL -->
    <div id="ai-modal">
        <div class="modal-header">
            <span>[ SYSTEM AI CORE CONFIGURATION ]</span>
            <span onclick="closeAI()" style="cursor:pointer; color: #fff;">[ CLOSE X ]</span>
        </div>
        <div class="modal-body">
            <div class="modal-sidebar" id="model-list">
                <div class="ai-item active" onclick="setAI(this, 'Gemini 3.0 Pro')">GEMINI 3.0 PRO (STABLE)</div>
                <div class="ai-item" onclick="setAI(this, 'Gemini 3.0 Flash')">GEMINI 3.0 FLASH</div>
                <div class="ai-item" onclick="setAI(this, 'Gemini 2.0 Pro')">GEMINI 2.0 PRO</div>
                <div class="ai-item" onclick="window.open('https://ai.google.dev/models/gemini', '_blank')" style="border-style: dashed; opacity: 0.6; margin-top: 20px;">MODEL REGISTRY ↗</div>
            </div>
            <div class="modal-content">
                <div>
                    <label style="font-size: 10px; opacity: 0.7;">ACTIVE DISPATCHER:</label>
                    <div id="current-model-display" style="font-size: 20px; color: #fff; margin-top: 5px;">Gemini 3.0 Pro</div>
                </div>
                
                <div style="margin-top: 10px;">
                    <label style="font-size: 10px; opacity: 0.7;">API AUTHORIZATION KEY:</label>
                    <input type="password" class="input-box" placeholder="ENTER GOOGLE API KEY...">
                    <a href="https://aistudio.google.com/app/apikey" target="_blank" class="api-link">ACQUIRE KEY FROM GOOGLE AI STUDIO ↗</a>
                </div>

                <div style="margin-top: 10px;">
                    <label style="font-size: 10px; opacity: 0.7;">TECHNICAL DOMAIN:</label>
                    <select class="input-box" style="appearance: none;">
                        <option>Industrial Automation</option>
                        <option>Hardware Architect</option>
                        <option>Consumer Electronics</option>
                    </select>
                </div>
                
                <div style="margin-top: auto; display: flex; gap: 10px;">
                    <button class="btn-classic" style="border-color: #0f0; color: #0f0; background: transparent;" onclick="closeAI()">INITIALIZE CORE</button>
                    <button class="btn-classic" onclick="closeAI()">CANCEL</button>
                </div>
            </div>
        </div>
    </div>

    <!-- MAIN DASHBOARD -->
    <div id="main-layout" style="flex: 1; display: flex; flex-direction: column;">
        <div id="top-split" style="display: flex; flex: 0.8;">
            <div id="cad-view" class="pane">CAD VIEWPORT</div>
            <div id="data-view" class="pane">ENGINE DATA</div>
        </div>
        <div id="bottom-split" class="pane">SYSTEM CONSOLE</div>
    </div>

    <div class="footer">
        <button class="btn-classic" onclick="openAI()">AI SETTINGS</button>
        <button class="btn-classic">HARDWARE</button>
        <button class="btn-classic">LOGS</button>
        <button class="btn-classic">EXPORT</button>
        <div style="margin-left: auto; color: #444; font-size: 10px; font-family: monospace;">SYS_CORE_V4 | 2026.05.04</div>
    </div>
</div>

<script>
    // Initialize Split.js
    Split(['#cad-view', '#data-view'], { 
        sizes: [70, 30], 
        gutterSize: 8,
        minSize: 100
    });
    
    Split(['#top-split', '#bottom-split'], { 
        direction: 'vertical', 
        sizes: [75, 25], 
        gutterSize: 8,
        minSize: 50
    });

    function openAI() { document.getElementById('ai-modal').style.display = 'flex'; }
    function closeAI() { document.getElementById('ai-modal').style.display = 'none'; }

    function setAI(el, name) {
        document.querySelectorAll('.ai-item').forEach(i => i.classList.remove('active'));
        el.classList.add('active');
        document.getElementById('current-model-display').innerText = name;
    }
</script>
"""

# Render component
components.html(cad_app_html, height=0)
st.components.v1.html(
    f"""<script>
        const iframe = window.parent.document.querySelector('iframe');
        iframe.style.height = '98vh';
        iframe.style.width = '100%';
    </script>""",
    height=0
)
