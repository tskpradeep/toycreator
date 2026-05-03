import streamlit as st
import streamlit.components.v1 as components

# 1. Page Configuration
st.set_page_config(layout="wide", page_title="Hardware Architect Pro")

# 2. UI Reset
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stApp { background-color: #000 !important; overflow: hidden !important; }
        .block-container { padding: 0rem !important; max-width: 100% !important; height: 100vh !important; overflow: hidden !important; }
    </style>
""", unsafe_allow_html=True)

# 3. Native UI Application
cad_app_html = """
<script src="https://cdnjs.cloudflare.com/ajax/libs/split.js/1.6.0/split.min.js"></script>
<style>
    html, body { margin: 0; padding: 0; height: 100%; width: 100%; overflow: hidden !important; background-color: #000; font-family: 'Segoe UI', sans-serif; color: white; }
    .master-container { display: flex; flex-direction: column; height: 100vh; width: 100vw; background: #000; border: 2px solid #d3d3d3; box-sizing: border-box; }
    .window-title-bar { background: #1a1a1a; color: #888; height: 30px; flex-shrink: 0; display: flex; align-items: center; justify-content: space-between; padding: 0 10px; font-size: 12px; border-bottom: 1px solid #333; }
    #dynamic-zone { display: flex; flex-direction: row; flex: 1; min-height: 0; width: 100%; }
    .pane { background: #000 !important; border: 1px solid #333 !important; overflow: hidden; display: flex; align-items: center; justify-content: center; box-sizing: border-box; position: relative; }
    .text-display { width: 100%; height: 100%; padding: 10px; overflow-y: auto; font-family: 'Consolas', monospace; font-size: 13px; color: #008000; white-space: pre-wrap; }
    .cmd-display { width: 100%; height: 100%; padding: 10px; overflow-y: auto; font-family: 'Consolas', monospace; font-size: 12px; color: #0f0; background: #000; }
    .input-area { width: 100%; height: 100%; background: transparent; border: none; color: #800080; padding: 10px; font-family: 'Consolas', monospace; font-size: 13px; outline: none; resize: none; }
    
    /* SVG Monitor Container */
    #visual-monitor { width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; background: #050505; }
    
    .fixed-footer { height: 64px; display: flex; flex-direction: row; border-top: 2px solid #333; background: #000; flex-shrink: 0; align-items: center; padding: 0px 10px; }
    .mic-dot { width: 12px; height: 12px; background: #ff0000; border-radius: 50%; box-shadow: 0 0 10px #f00; margin-right: 15px; }
</style>

<div class="master-container">
    <div class="window-title-bar">
        <div>SYSTEM ARCHITECT - TECH BUNDLE ENGINE</div>
        <div><span>−</span><span>❐</span><span>×</span></div>
    </div>
    <div id="dynamic-zone">
        <div id="split-container" style="display:flex; flex:1; width:100%;">
            <div id="left-stack" style="display:flex; flex-direction:column; width:70%;">
                <div id="cad-pane" class="pane">
                    <div id="visual-monitor">
                        <div style="color: #444; font-size: 12px; text-align: center;">WAITING FOR ARCHITECTURAL INPUT...<br>[READY FOR SPLIT-CORE OR PROCESSOR LOGIC]</div>
                    </div>
                </div>
                <div id="cmd-pane" class="pane">
                    <div id="terminal-out" class="cmd-display">>_ BASEMENT_OS LOADED. WAITING FOR COMPILER INSTRUCTIONS.</div>
                </div>
            </div>
            <div id="right-stack" style="display:flex; flex-direction:column; width:30%;">
                <div id="ai-output" class="pane">
                    <div id="ai-text-box" class="text-display">Architect AI Ready...</div>
                </div>
                <div id="ai-input" class="pane">
                    <textarea id="user-prompt" class="input-area" placeholder="e.g. 'high level architecture of a split core power supply'"></textarea>
                </div>
            </div>
        </div>
    </div>
    <div class="fixed-footer">
        <div class="mic-dot"></div>
        <div style="color: #00ff00; font-size: 10px; font-family: monospace;">STACK: Gemini-Pro | Flux.ai | KiCad</div>
        <div style="flex:1;"></div>
        <div style="color: #888; font-size: 11px;">MODE: TECH BUNDLE GENERATOR</div>
    </div>
</div>

<script>
    Split(['#left-stack', '#right-stack'], { sizes: [70, 30], gutterSize: 4 });
    Split(['#cad-pane', '#cmd-pane'], { direction: 'vertical', sizes: [80, 20], gutterSize: 4 });
    Split(['#ai-output', '#ai-input'], { direction: 'vertical', sizes: [50, 50], gutterSize: 4 });

    const promptInput = document.getElementById('user-prompt');
    const aiOutput = document.getElementById('ai-text-box');
    const terminal = document.getElementById('terminal-out');
    const monitor = document.getElementById('visual-monitor');

    promptInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            const text = promptInput.value.trim();
            if(text !== "") {
                aiOutput.innerHTML += "\\n\\n[USER]: " + text;
                const query = text.toLowerCase();

                if(query.includes("power supply") || query.includes("split core")) {
                    aiOutput.innerHTML += "\\n[ARCHITECT]: Mapping High-Current Split-Core Topology...\\n- Calculating Isolation Stages\\n- Defining Flux.ai Schematic requirements\\n- Formatting ODB++ Export parameters.";
                    
                    // PRO SVG Drawing
                    monitor.innerHTML = `
                        <svg width="400" height="200" viewBox="0 0 400 200">
                            <rect x="10" y="70" width="80" height="60" fill="none" stroke="white" stroke-width="2"/>
                            <text x="20" y="105" fill="white" font-size="10">AC INPUT</text>
                            <line x1="90" y1="100" x2="130" y2="100" stroke="#0f0" stroke-width="2" />
                            <circle cx="160" cy="100" r="30" fill="none" stroke="#0f0" stroke-width="2" stroke-dasharray="4"/>
                            <text x="140" y="105" fill="#0f0" font-size="9">SPLIT CORE</text>
                            <line x1="190" y1="100" x2="230" y2="100" stroke="#0f0" stroke-width="2" />
                            <rect x="230" y="70" width="80" height="60" fill="none" stroke="white" stroke-width="2"/>
                            <text x="240" y="105" fill="white" font-size="10">REGULATOR</text>
                            <line x1="310" y1="100" x2="350" y2="100" stroke="#0f0" stroke-width="2" />
                            <text x="355" y="105" fill="#0f0" font-size="10">DC OUT</text>
                        </svg>
                    `;

                    terminal.innerHTML += "\\n\\n> BUNDLE_GEN: Creating Flux.ai project link...";
                    terminal.innerHTML += "\\n> BOM: Selected High-Saturation Split Core Transformer.";
                    terminal.innerHTML += "\\n> CAD: Calculating STEP file clearances for Enclosure.";
                    terminal.scrollTop = terminal.scrollHeight;
                } else {
                    aiOutput.innerHTML += "\\n[ARCHITECT]: Analyzing request for Tech Bundle compatibility...";
                }

                promptInput.value = ""; 
                aiOutput.scrollTop = aiOutput.scrollHeight;
            }
        }
    });
</script>
"""

components.html(cad_app_html, height=0)
st.components.v1.html(
    f"""<script>
        window.parent.document.querySelector('iframe').style.height = '94vh';
    </script>""",
    height=0
)
