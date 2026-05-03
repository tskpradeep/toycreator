import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai

# --- 1. CONFIG & MODEL SETUP ---
st.set_page_config(layout="wide", page_title="CAD Designer Pro")

# Set up your Gemini API Key here or via Streamlit Secrets
API_KEY = "YOUR_GEMINI_API_KEY" 
if API_KEY != "YOUR_GEMINI_API_KEY":
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None

# --- 2. UI RESET (STYLING) ---
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

# --- 3. NATIVE UI APPLICATION (HTML/JS) ---
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
        position: relative;
    }
    /* --- SYSTEM AI-SET MODULAR WINDOW --- */
    #ai-modular-setup {
        position: absolute; top: 10%; left: 15%; width: 70%; height: 75%;
        background: #000; border: 2px solid #00ff00; z-index: 9999;
        display: none; flex-direction: column; box-shadow: 0 0 50px rgba(0,255,0,0.3);
    }
    .ai-setup-header { background: #0a1a0a; border-bottom: 1px solid #00ff00; padding: 10px; display: flex; justify-content: space-between; color: #00ff00; font-family: monospace; font-weight: bold; }
    .ai-setup-body { display: flex; flex: 1; overflow: hidden; }
    .ai-setup-sidebar { width: 30%; border-right: 1px solid #00ff00; padding: 10px; background: #050505; overflow-y: auto; }
    .ai-setup-content { width: 70%; padding: 25px; color: #00ff00; font-family: monospace; display: flex; flex-direction: column; gap: 20px; }
    .ai-tool-item { padding: 12px; border: 1px solid #004400; margin-bottom: 8px; cursor: pointer; font-size: 12px; transition: 0.2s; }
    .ai-tool-item:hover { border-color: #00ff00; background: #0a2a0a; }
    .ai-tool-item.active { background: #00ff00; color: #000; font-weight: bold; }
    .ai-select, .ai-input { background: #000; border: 1px solid #00ff00; color: #00ff00; padding: 10px; width: 100%; outline: none; font-family: monospace; }

    /* --- DASHBOARD PADS --- */
    .window-title-bar { background: #1a1a1a; color: #888; height: 30px; display: flex; align-items: center; justify-content: space-between; padding: 0 10px; font-size: 12px; border-bottom: 1px solid #333; }
    #dynamic-zone { display: flex; flex-direction: row; flex: 1; min-height: 0; width: 100%; }
    .pane { background: #000 !important; border: 1px solid #333 !important; overflow: hidden; display: flex; align-items: center; justify-content: center; box-sizing: border-box; }
    .gutter { background-color: #444 !important; }
    .fixed-footer { height: 64px; display: flex; border-top: 2px solid #333; background: #000; align-items: flex-end; padding: 0 4px 2px 4px; }
    .ai-text-area { width: 100%; height: 100%; padding: 10px; color: #008000; font-family: 'Consolas', monospace; font-size: 13px; overflow-y: auto; }
    .user-input-area { width: 100%; height: 100%; background: transparent; border: none; color: #800080; padding: 10px; font-family: 'Consolas', monospace; outline: none; resize: none; font-weight: bold; }
    .cmd-text { width: 100%; height: 100%; color: #0f0; font-family: monospace; font-size: 11px; padding: 5px; overflow-y: auto; }
    .btn-cell { width: 20px; height: 20px; background: #e1e1e1; border: 2px solid; border-color: #fff #707070 #707070 #fff; cursor: pointer; flex-shrink: 0; }
</style>

<div class="master-container">
    <div id="ai-modular-setup">
        <div class="ai-setup-header"><span>[ SYSTEM AI-SET ]</span><span onclick="toggleAISet(false)" style="cursor:pointer;">[ X ]</span></div>
        <div class="ai-setup-body">
            <div class="ai-setup-sidebar">
                <div class="ai-tool-item active">LUVIA AI</div>
                <div class="ai-tool-item">FLUX.AI</div>
            </div>
            <div class="ai-setup-content">
                <div style="font-size: 20px; color:#fff;">TOOL: GEMINI (CORE)</div>
                <input type="password" class="ai-input" placeholder="API KEY ACTIVE...">
                <button class="btn-cell" style="width: 100px; height: 30px; background:#00ff00;" onclick="toggleAISet(false)">SAVE</button>
            </div>
        </div>
    </div>

    <div class="window-title-bar"><div>CAD DESIGNER PRO</div></div>

    <div id="dynamic-zone">
        <div id="split-container" style="display:flex; flex:1; width:100%;">
            <div id="left-stack" style="display:flex; flex-direction:column; width:70%;">
                <div id="cad-pane" class="pane"><div style="color:#b22222; font-weight:bold;">VISUAL MONITOR</div></div>
                <div id="cmd-pane" class="pane"><div id="terminal-out" class="cmd-text">>_ SYSTEM READY</div></div>
            </div>
            <div id="right-stack" style="display:flex; flex-direction:column; width:30%;">
                <div id="ai-output" class="pane"><div id="ai-chat" class="ai-text-area">GEMINI STANDBY...</div></div>
                <div id="ai-input" class="pane"><textarea id="user-prompt" class="user-input-area" placeholder="ASK GEMINI..."></textarea></div>
            </div>
        </div>
    </div>

    <div class="fixed-footer">
        <div style="flex:1; color:#008000; font-size:11px; padding-left:10px;">SYSTEM: ONLINE</div>
        <div class="dropup tall" style="background:#e1e1e1; width:100px; height:60px; display:flex; align-items:center; justify-content:center; cursor:pointer;" onclick="toggleAISet(true)">
            <span style="color:#000; font-size:10px; font-weight:bold;">AI-SET</span>
        </div>
    </div>
</div>

<script>
    Split(['#left-stack', '#right-stack'], { sizes: [70, 30], gutterSize: 4 });
    Split(['#cad-pane', '#cmd-pane'], { direction: 'vertical', sizes: [80, 20], gutterSize: 4 });
    Split(['#ai-output', '#ai-input'], { direction: 'vertical', sizes: [70, 30], gutterSize: 4 });

    function toggleAISet(show) { document.getElementById('ai-modular-setup').style.display = show ? 'flex' : 'none'; }

    const promptInput = document.getElementById('user-prompt');
    const chatWindow = document.getElementById('ai-chat');
    const terminal = document.getElementById('terminal-out');

    promptInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            const text = promptInput.value.trim();
            if(text !== "") {
                chatWindow.innerHTML += "<br><br><span style='color:#800080'>[USER]:</span> " + text;
                terminal.innerHTML += "\\n> SENDING TO GEMINI...";
                
                // SEND TO STREAMLIT BACKEND
                const btn = window.parent.document.createElement('button');
                btn.innerText = text;
                btn.style.display = 'none';
                btn.onclick = () => {}; 
                // We use a custom event to notify Streamlit
                window.parent.postMessage({type: 'streamlit:setComponentValue', value: text}, '*');
                
                promptInput.value = "";
            }
        }
    });

    // Receive from Streamlit
    window.addEventListener('message', function(e) {
        if(e.data.type === 'GEMINI_REPLY') {
            chatWindow.innerHTML += "<br><br><span style='color:#00ff00'>[GEMINI]:</span> " + e.data.content;
            terminal.innerHTML += "\\n> DONE.";
            chatWindow.scrollTop = chatWindow.scrollHeight;
        }
    });
</script>
"""

# --- 4. BACKEND BRIDGE ---
# This component captures the user input from the JS "postMessage"
user_input = components.html(cad_app_html, height=0)

# Set the iframe height for the main UI
components.html(
    f"""<script>
        window.parent.document.querySelector('iframe').style.height = '94vh';
    </script>""",
    height=0
)

# Gemini Logic Loop
if user_input:
    if model:
        try:
            response = model.generate_content(user_input)
            ai_text = response.text.replace("'", "\\'") # Escape for JS
            
            # Send reply back to the HTML chat window
            components.html(f"""
                <script>
                window.parent.postMessage({{
                    type: 'GEMINI_REPLY',
                    content: '{ai_text}'
                }}, '*');
                </script>
            """, height=0)
        except Exception as e:
            st.error(f"Gemini Error: {e}")
    else:
        st.warning("Please configure your Gemini API Key in the script.")
