import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="Architect AI - Full GUI")

st.markdown("""
    <style>
        #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
        .stApp { background-color: #000 !important; overflow: hidden !important; }
        .block-container { padding: 0rem !important; max-width: 100% !important; height: 100vh !important; }
    </style>
""", unsafe_allow_html=True)

cad_app_html = """
<script src="https://cdnjs.cloudflare.com/ajax/libs/split.js/1.6.0/split.min.js"></script>
<style>
    html, body { margin: 0; padding: 0; height: 100%; width: 100%; overflow: hidden; background: #000; font-family: 'Segoe UI', sans-serif; color: white; }
    .master-container { display: flex; flex-direction: column; height: 100vh; width: 100vw; border: 2px solid #d3d3d3; box-sizing: border-box; }
    
    .window-title-bar { background: #1a1a1a; color: #888; height: 30px; display: flex; align-items: center; justify-content: space-between; padding: 0 10px; font-size: 12px; border-bottom: 1px solid #333; }

    #dynamic-zone { display: flex; flex-direction: row; flex: 1; min-height: 0; }

    /* PANES */
    .pane { background: #000; border: 1px solid #333; overflow: hidden; display: flex; align-items: center; justify-content: center; position: relative; }
    .gutter { background-color: #444 !important; }

    /* RIGHT SIDE STRIP (The buttons you missed!) */
    .fixed-right-strip { 
        width: 65px; border-left: 1px solid #333; 
        display: grid; grid-template-columns: 1fr 1fr;
        grid-auto-rows: min-content; gap: 4px;
        padding: 5px; background: #0b0b0b; overflow-y: auto; 
    }
    .btn-cell { 
        aspect-ratio: 1/1; width: 22px; height: 22px; 
        background: #e1e1e1; color: #000; border: 1px solid #777;
        font-size: 8px; font-weight: bold; display: flex; align-items: center; justify-content: center; cursor: pointer;
    }

    /* TEXT DISPLAYS */
    .text-display { width: 100%; height: 100%; padding: 10px; overflow-y: auto; font-family: 'Consolas', monospace; font-size: 13px; color: #008000; }
    .cmd-display { width: 100%; height: 100%; padding: 10px; overflow-y: auto; font-family: 'Consolas', monospace; font-size: 12px; color: #0f0; background: #000; }
    .input-area { width: 100%; height: 100%; background: transparent; border: none; color: #800080; padding: 10px; font-family: 'Consolas', monospace; outline: none; resize: none; }

    /* FOOTER */
    .fixed-footer { height: 60px; display: flex; align-items: center; border-top: 2px solid #333; background: #000; padding: 0 10px; }
    .mic-btn { width: 35px; height: 35px; background: #222; border: 1px solid #444; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; margin-right: 15px; box-shadow: 0 0 5px #f00; }
    .foot-palette { display: grid; grid-template-columns: repeat(8, 18px); gap: 2px; }
</style>

<div class="master-container">
    <div class="window-title-bar">
        <div>SYSTEM ARCHITECT - V2.0 PRO </div>
        <div><span>−</span><span style="margin:0 10px;">❐</span><span>×</span></div>
    </div>

    <div id="dynamic-zone">
        <div id="split-container" style="display:flex; flex:1;">
            <div id="left-stack" style="display:flex; flex-direction:column; width:70%;">
                <div id="cad-pane" class="pane">
                    <div id="visual-monitor" style="color:#444;">[ VISUAL MONITOR ACTIVE ]</div>
                </div>
                <div id="cmd-pane" class="pane">
                    <div id="terminal-out" class="cmd-display">>_ System Core Linked. Waiting for command...</div>
                </div>
            </div>
            <div id="right-stack" style="display:flex; flex-direction:column; width:30%;">
                <div id="ai-output" class="pane">
                    <div id="ai-text-box" class="text-display">Architect Ready...</div>
                </div>
                <div id="ai-input" class="pane">
                    <textarea id="user-prompt" class="input-area" placeholder="Describe your architecture..."></textarea>
                </div>
            </div>
        </div>
        
        <!-- RESTORED RIGHT STRIP -->
        <div class="fixed-right-strip" id="side-strip">
            <!-- JS will populate these -->
        </div>
    </div>

    <div class="fixed-footer">
        <div class="mic-btn"><div style="width:10px; height:10px; background:red; border-radius:50%;"></div></div>
        <div class="foot-palette" id="foot-palette"></div>
        <div style="flex:1;"></div>
        <div style="font-size: 10px; color: #666; font-family: monospace; margin-right: 20px;">TECH BUNDLE: READY</div>
        <div style="color: #0f0; font-size: 11px;">ONLINE</div>
    </div>
</div>

<script>
    // 1. Split logic
    Split(['#left-stack', '#right-stack'], { sizes: [70, 30], gutterSize: 4 });
    Split(['#cad-pane', '#cmd-pane'], { direction: 'vertical', sizes: [80, 20], gutterSize: 4 });
    Split(['#ai-output', '#ai-input'], { direction: 'vertical', sizes: [50, 50], gutterSize: 4 });

    // 2. Populate Buttons (Restore GUI)
    const strip = document.getElementById('side-strip');
    for(let i=0; i<40; i++) {
        const btn = document.createElement('div');
        btn.className = 'btn-cell';
        btn.innerText = i+1;
        strip.appendChild(btn);
    }

    const palette = document.getElementById('foot-palette');
    for(let i=0; i<16; i++) {
        const pbtn = document.createElement('div');
        pbtn.className = 'btn-cell';
        pbtn.style.background = i % 2 === 0 ? '#333' : '#666';
        palette.appendChild(pbtn);
    }

    // 3. Command Logic
    const promptInput = document.getElementById('user-prompt');
    const aiOutput = document.getElementById('ai-text-box');
    const terminal = document.getElementById('terminal-out');
    const monitor = document.getElementById('visual-monitor');

    promptInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            const text = promptInput.value.trim();
            if(text) {
                aiOutput.innerHTML += "\\n\\n[USER]: " + text;
                const query = text.toLowerCase();
                
                if(query.includes("power supply") || query.includes("split core")) {
                    monitor.innerHTML = `
                        <svg width="300" height="150">
                            <rect x="10" y="50" width="60" height="50" stroke="white" fill="none" />
                            <circle cx="150" cy="75" r="30" stroke="#0f0" fill="none" stroke-dasharray="5"/>
                            <rect x="230" y="50" width="60" height="50" stroke="white" fill="none" />
                            <path d="M70 75 L120 75 M180 75 L230 75" stroke="#0f0" />
                        </svg>`;
                    terminal.innerHTML += "\\n> ARCH: Split-Core Logic Mapped.";
                } else if(query.includes("led")) {
                    monitor.innerHTML = '<div style="border:2px solid #0f0; padding:20px;">[BATT] -- [SW] -- [RES] -- {LED}</div>';
                    terminal.innerHTML += "\\n> ARCH: LED Circuit Initiated.";
                }

                promptInput.value = "";
                aiOutput.scrollTop = aiOutput.scrollHeight;
                terminal.scrollTop = terminal.scrollHeight;
            }
        }
    });
</script>
"""

components.html(cad_app_html, height=0)
st.components.v1.html(f"<script>window.parent.document.querySelector('iframe').style.height = '94vh';</script>", height=0)
