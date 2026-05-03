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

    .pane { background: #000 !important; border: 1px solid #333 !important; overflow: hidden; display: flex; align-items: center; justify-content: center; box-sizing: border-box; position: relative;}
    .gutter { background-color: #444 !important; }

    /* Text & Visual Area Styles */
    .text-display { width: 100%; height: 100%; padding: 10px; overflow-y: auto; font-family: 'Consolas', monospace; font-size: 13px; color: #008000; white-space: pre-wrap; }
    .cmd-display { width: 100%; height: 100%; padding: 10px; overflow-y: auto; font-family: 'Consolas', monospace; font-size: 12px; color: #0f0; background: #000; }
    .input-area { width: 100%; height: 100%; background: transparent; border: none; color: #800080; padding: 10px; font-family: 'Consolas', monospace; font-size: 13px; outline: none; resize: none; }

    /* Visual Monitor Styling */
    #visual-monitor { width: 100%; height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center; background: #050505; }
    .circuit-block { border: 2px solid #fff; padding: 10px; margin: 5px; min-width: 100px; text-align: center; font-size: 12px; font-family: 'Consolas'; background: #111; }
    .wire { width: 2px; height: 20px; background: #0f0; }

    .fixed-footer { height: 64px; display: flex; flex-direction: row; border-top: 2px solid #333; background: #000; flex-shrink: 0; align-items: center; padding: 0px 10px; }
    
    /* Audio Indicator */
    .mic-dot { width: 12px; height: 12px; background: #ff0000; border-radius: 50%; box-shadow: 0 0 10px #f00; margin-right: 15px; }
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
                    <textarea id="user-prompt" class="input-area" placeholder="Ask for an LED circuit diagram..."></textarea>
                </div>
            </div>
        </div>
    </div>

    <div class="fixed-footer">
        <div class="mic-dot"></div>
        <div style="color: #666; font-size: 10px; font-family: monospace;">AUDIO CHANNEL: STANDBY</div>
        <div style="flex:1;"></div>
        <div style="color: #008000; font-size: 11px;">SYSTEM STATUS: ONLINE</div>
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
                
                // ARCHITECT BRAIN: Smart Detection
                const query = text.toLowerCase();
                if(query.includes("led") || query.includes("circuit") || query.includes("diagram")) {
                    
                    aiOutput.innerHTML += "\\n[ARCHITECT]: Logic recognized. Generating Block Diagram for LED Control System...\\n- Integrating 3.3V Source\\n- Adding Series Current-Limiting Resistor (220Ω)\\n- Mapping GPIO Switch Link.";
                    
                    // Render Visual
                    monitor.innerHTML = `
                        <div style="color:#0f0; font-size:10px; margin-bottom:10px;">TOP-LEVEL ARCHITECTURE</div>
                        <div class="circuit-block">[ BATTERY 3.3V ]</div>
                        <div class="wire"></div>
                        <div class="circuit-block" style="border-style: dashed;">( PUSH BUTTON )</div>
                        <div class="wire"></div>
                        <div class="circuit-block">[ RESISTOR 220 Ohm ]</div>
                        <div class="wire"></div>
                        <div class="circuit-block" style="border-color: #0f0; color: #0f0;">{ GREEN LED }</div>
                    `;

                    // Generate Technical Data in Command Pane
                    terminal.innerHTML += "\\n\\n> Initializing LED_Project_v1...";
                    terminal.innerHTML += "\\n> NET: BATT_POS to SW_IN";
                    terminal.innerHTML += "\\n> NET: SW_OUT to R1_IN";
                    terminal.innerHTML += "\\n> NET: R1_OUT to LED_ANODE";
                    terminal.innerHTML += "\\n> NET: LED_CATHODE to BATT_NEG (GND)";
                    terminal.innerHTML += "\\n> CALCULATING: If Vcc=3.3V, Vf=2.0V, I=5.9mA. Logic Safe.";
                    terminal.scrollTop = terminal.scrollHeight;
                } else {
                    aiOutput.innerHTML += "\\n[ARCHITECT]: Please provide a design specific or architectural requirement.";
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
