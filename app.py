import streamlit as st
import streamlit.components.v1 as components

# 1. Page Configuration
st.set_page_config(layout="wide", page_title="Architect AI Workbench")

# 2. UI Reset
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

# 3. Native UI Application
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
        border: 2px solid #d3d3d3; box-sizing: border-box;
    }

    .window-title-bar {
        background: #1a1a1a; color: #888; height: 30px;
        flex-shrink: 0; display: flex; align-items: center; 
        justify-content: space-between; padding: 0 10px; font-size: 12px;
        border-bottom: 1px solid #333;
    }

    #dynamic-zone { display: flex; flex-direction: row; flex: 1; min-height: 0; width: 100%; }

    .fixed-right-strip { 
        width: 65px; border-left: 1px solid #333; 
        display: grid; grid-template-columns: 1fr 1fr;
        grid-auto-rows: min-content; gap: 2px;
        padding: 5px; background: #000; 
        overflow-y: scroll; 
    }

    .btn-cell {
        aspect-ratio: 1 / 1; width: 20px; height: 20px;
        background: #e1e1e1; color: #000;
        border: 1px solid #707070;
        cursor: pointer; display: flex; align-items: center; justify-content: center;
        box-sizing: border-box; flex-shrink: 0; font-size: 8px; font-weight: bold;
    }

    .pane { background: #000 !important; border: 1px solid #333 !important; overflow: hidden; display: flex; align-items: center; justify-content: center; box-sizing: border-box; position: relative;}
    .gutter { background-color: #444 !important; }

    /* Text & Visual Area Styles */
    .text-display { width: 100%; height: 100%; padding: 10px; overflow-y: auto; font-family: 'Consolas', monospace; font-size: 13px; color: #008000; white-space: pre-wrap; }
    .cmd-display { width: 100%; height: 100%; padding: 10px; overflow-y: auto; font-family: 'Consolas', monospace; font-size: 12px; color: #0f0; background: #000; }
    .input-area { width: 100%; height: 100%; background: transparent; border: none; color: #800080; padding: 10px; font-family: 'Consolas', monospace; font-size: 13px; outline: none; resize: none; }

    /* Visual Monitor Styling */
    #visual-monitor { width: 100%; height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center; background: #050505; }
    .circuit-block { border: 2px solid #fff; padding: 10px; margin: 10px; min-width: 80px; text-align: center; font-size: 12px; font-family: 'Consolas'; }
    .wire { width: 2px; height: 30px; background: #0f0; }

    .fixed-footer { height: 64px; display: flex; flex-direction: row; border-top: 2px solid #333; background: #000; flex-shrink: 0; align-items: flex-end; padding: 0px 4px 2px 4px; }
</style>

<div class="master-container">
    <div class="window-title-bar">
        <div>ARCHITECT AI - SYSTEM DESIGNER</div>
        <div><span>−</span><span style="margin:0 10px;">❐</span><span>×</span></div>
    </div>

    <div id="dynamic-zone">
        <div id="split-container" style="display:flex; flex:1; width:100%;">
            <div id="left-stack" style="display:flex; flex-direction:column; width:70%;">
                <div id="cad-pane" class="pane">
                    <div id="visual-monitor">
                        <div style="color: #444; font-size: 14px;">VISUAL MONITOR IDLE</div>
                    </div>
                </div>
                <div id="cmd-pane" class="pane">
                    <div id="terminal-out" class="cmd-display">>_ System Kernel Loaded...</div>
                </div>
            </div>
            <div id="right-stack" style="display:flex; flex-direction:column; width:30%;">
                <div id="ai-output" class="pane">
                    <div id="ai-text-box" class="text-display">Architect AI Ready...</div>
                </div>
                <div id="ai-input" class="pane">
                    <textarea id="user-prompt" class="input-area" placeholder="Type 'draw circuit' to test Visual Monitor..."></textarea>
                </div>
            </div>
        </div>
        <div class="fixed-right-strip" id="side-strip"></div>
    </div>

    <div class="fixed-footer">
        <!-- Audio Mic Placeholder -->
        <div style="width: 40px; height: 40px; background: #222; border-radius: 50%; display:flex; align-items:center; justify-content:center; cursor:pointer; margin: 10px;">
            <span style="color: #ff0000; font-size: 18px;">●</span>
        </div>
        <div id="foot-palette" style="display: grid; grid-template-columns: repeat(6, 20px); gap: 1px; margin-bottom: 4px;"></div>
        <div style="flex:1;"></div>
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
                
                if(text.toLowerCase().includes("draw circuit")) {
                    aiOutput.innerHTML += "\\n[ARCHITECT]: Designing Switch-Bulb logic...\\n1. Battery Source (9V)\\n2. Toggle Switch\\n3. Incandescent Load";
                    
                    // Logic to update the Visual Monitor
                    monitor.innerHTML = `
                        <div class="circuit-block">[ BATTERY ]</div>
                        <div class="wire"></div>
                        <div class="circuit-block" style="border-style: dashed;">( SWITCH )</div>
                        <div class="wire"></div>
                        <div class="circuit-block" style="border-color: yellow; color: yellow;">{ BULB }</div>
                    `;

                    terminal.innerHTML += "\\n> GEN_NETLIST: V1 N001 0 9V";
                    terminal.innerHTML += "\\n> GEN_NETLIST: S1 N001 N002";
                    terminal.innerHTML += "\\n> GEN_NETLIST: L1 N002 0";
                    terminal.scrollTop = terminal.scrollHeight;
                } else {
                    aiOutput.innerHTML += "\\n[ARCHITECT]: Listening for design commands.";
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
