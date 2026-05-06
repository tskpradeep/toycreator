import streamlit as st
import streamlit.components.v1 as components

# 1. Page Configuration
st.set_page_config(layout="wide", page_title="CAD Designer Pro")

# 2. UI Reset & Styling
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

# 3. Full Integrated Application Code
cad_app_html = """
<!DOCTYPE html>
<html>
<head>
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

        #ai-modular-setup {
            position: absolute; top: 10%; left: 15%; width: 70%; height: 75%;
            background: #000; border: 2px solid #00ff00; z-index: 9999;
            display: none; flex-direction: column; box-shadow: 0 0 50px rgba(0,255,0,0.3);
        }
        .ai-setup-header { 
            background: #0a1a0a; border-bottom: 1px solid #00ff00; 
            padding: 10px; display: flex; justify-content: space-between; 
            color: #00ff00; font-family: monospace; font-weight: bold; 
            align-items: center;
        }
        .ai-header-controls { display: flex; gap: 10px; align-items: center; }
        .ai-setup-body { display: flex; flex: 1; overflow: hidden; }
        .ai-setup-sidebar { width: 30%; border-right: 1px solid #00ff00; padding: 10px; background: #050505; overflow-y: auto; }
        .ai-setup-content { width: 70%; padding: 25px; color: #00ff00; font-family: monospace; display: flex; flex-direction: column; gap: 20px; }
        
        .ai-tool-item { padding: 12px; border: 1px solid #004400; margin-bottom: 8px; cursor: pointer; font-size: 12px; transition: 0.2s; }
        .ai-tool-item:hover { border-color: #00ff00; background: #0a2a0a; }
        .ai-tool-item.active { background: #00ff00; color: #000; font-weight: bold; }
        
        .ai-select { background: #000; border: 1px solid #00ff00; color: #00ff00; padding: 10px; width: 100%; outline: none; cursor: pointer; font-family: monospace; appearance: none; }
        .ai-input { background: #000; border: 1px solid #00ff00; color: #00ff00; padding: 10px; width: 100%; outline: none; box-sizing: border-box; }

        .window-title-bar { background: #1a1a1a; color: #888; height: 30px; flex-shrink: 0; display: flex; align-items: center; justify-content: space-between; padding: 0 10px; font-size: 12px; border-bottom: 1px solid #333; }
        #dynamic-zone { display: flex; flex-direction: row; flex: 1; min-height: 0; width: 100%; }
        
        .fixed-right-strip { width: 65px; border-left: 1px solid #333; display: grid; grid-template-columns: 1fr 1fr; grid-auto-rows: min-content; gap: 2px; padding: 5px; background: #000; overflow-y: scroll; }
        .btn-cell { aspect-ratio: 1 / 1; width: 20px; height: 20px; background: #e1e1e1; color: #000; border-top: 2px solid #fff; border-left: 2px solid #fff; border-right: 2px solid #707070; border-bottom: 2px solid #707070; cursor: pointer; display: flex; align-items: center; justify-content: center; box-sizing: border-box; }
        
        .pane { background: #000 !important; border: 1px solid #333 !important; overflow: hidden; display: flex; align-items: center; justify-content: center; box-sizing: border-box; }
        .gutter { background-color: #444 !important; }
        
        .fixed-footer { height: 64px; display: flex; flex-direction: row; border-top: 2px solid #333; background: #000; flex-shrink: 0; align-items: flex-end; padding: 0px 4px 2px 4px; }
        .footer-left-content { flex: 1; display: flex; height: 100%; align-items: center; padding-left: 10px;}
        
        .ai-text-area { width: 100%; height: 100%; padding: 10px; color: #00ff00; font-family: 'Consolas', monospace; font-size: 13px; overflow-y: auto; text-align: left; box-sizing: border-box; }
        .user-input-area { width: 100%; height: 100%; background: transparent; border: none; color: #800080; padding: 10px; font-family: 'Consolas', monospace; outline: none; resize: none; font-weight: bold; box-sizing: border-box; }
        .cmd-text { width: 100%; height: 100%; color: #0f0; font-family: monospace; font-size: 11px; padding: 5px; overflow-y: auto; white-space: pre-wrap; box-sizing: border-box; }

        .dropup { position: relative; width: 130px; height: 20px; background: #e1e1e1; color: #000; border: 1px solid #707070; display: flex; align-items: center; justify-content: space-between; padding: 0 5px; cursor: pointer; font-size: 9px; box-sizing: border-box; }
        .dropup.tall { height: 62px; }
    </style>
</head>
<body>

<div class="master-container">
    <!-- AI CONFIGURATION MODAL -->
    <div id="ai-modular-setup">
        <div class="ai-setup-header">
            <span>[ SYSTEM AI-SET : TOOL CONFIGURATION ]</span>
            <div class="ai-header-controls">
                <button style="cursor:pointer;" onclick="saveData()">SAVE</button>
                <button style="cursor:pointer;" onclick="toggleAISet(false)">[ X ]</button>
            </div>
        </div>
        <div class="ai-setup-body">
            <div class="ai-setup-sidebar">
                <div class="ai-tool-item active">GOOGLE GEMINI</div>
            </div>
            <div class="ai-setup-content">
                <label>MODEL VERSION:</label>
                <select class="ai-select" id="version-select">
                    <option value="gemini-1.5-flash">Gemini 1.5 Flash (Fast)</option>
                    <option value="gemini-1.5-pro">Gemini 1.5 Pro (Logical)</option>
                </select>
                <label>API KEY:</label>
                <input type="password" id="api-field-input" class="ai-input" placeholder="Paste your Google API Key here...">
            </div>
        </div>
    </div>

    <div class="window-title-bar">
        <div>CAD DESIGNER PRO - V1.0</div>
    </div>

    <div id="dynamic-zone">
        <div id="split-container" style="display:flex; flex:1; width:100%;">
            <!-- Left Side: Visuals and Terminal -->
            <div id="left-stack" style="display:flex; flex-direction:column; width:70%;">
                <div id="cad-pane" class="pane" style="flex: 8;">
                    <div id="visual-monitor" style="color: #444; font-size: 12px; font-family: monospace;">[ MONITOR ACTIVE ]</div>
                </div>
                <div id="cmd-pane" class="pane" style="flex: 2;">
                    <div id="terminal-out" class="cmd-text">>_ SYSTEM READY</div>
                </div>
            </div>
            <!-- Right Side: AI Interaction -->
            <div id="right-stack" style="display:flex; flex-direction:column; width:30%;">
                <div id="ai-output" class="pane" style="flex: 1;">
                    <div id="ai-chat" class="ai-text-area">AI TEXT REPLYING WINDOW</div>
                </div>
                <div id="ai-input" class="pane" style="flex: 1;">
                    <textarea id="user-prompt" class="user-input-area" placeholder="TYPE MESSAGE AND PRESS ENTER..."></textarea>
                </div>
            </div>
        </div>
    </div>

    <!-- Footer -->
    <div class="fixed-footer">
        <div class="footer-left-content">
            <span style="color:#008000; font-size: 11px;">STATUS: ONLINE</span>
        </div>
        <div class="dropup tall" onclick="toggleAISet(true)">
            <span>AI-SET</span><span>▲</span>
        </div>
    </div>
</div>

<script>
    // 1. Initialize Split Panes
    Split(['#left-stack', '#right-stack'], { sizes: [70, 30], gutterSize: 4 });
    
    function toggleAISet(show) { 
        document.getElementById('ai-modular-setup').style.display = show ? 'flex' : 'none'; 
    }

    // 2. Data Persistence
    function saveData() {
        const key = document.getElementById('api-field-input').value.trim();
        const model = document.getElementById('version-select').value;
        if(key) {
            localStorage.setItem('gemini_api_key', key);
            document.getElementById('ai-chat').innerHTML += `<br><br><span style="color:#00ff00">[SYSTEM]: CONFIG SAVED. ACTIVE: ${model.toUpperCase()}</span>`;
            document.getElementById('terminal-out').innerHTML += `\\n> CONFIG_SAVE: SUCCESS`;
            toggleAISet(false);
        }
    }

    // 3. HTTP Request Implementation (Gemini API)
    async function callGemini(promptText) {
        const apiKey = localStorage.getItem('gemini_api_key');
        const model = document.getElementById('version-select').value;
        const chatWindow = document.getElementById('ai-chat');
        const terminal = document.getElementById('terminal-out');

        if (!apiKey) {
            chatWindow.innerHTML += "<br><span style='color:red'>[ERROR]: API KEY MISSING. OPEN AI-SET.</span>";
            return;
        }

        try {
            terminal.innerHTML += `\\n> API_POST: CALLING ${model}...`;
            
            // Explicit HTTP POST Request Node Logic
            const response = await fetch(`https://generativelanguage.googleapis.com/v1/models/${model}:generateContent?key=${apiKey}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    "contents": [{ "parts": [{ "text": promptText }] }]
                })
            });

            const data = await response.json();

            if (response.ok) {
                const aiResponse = data.candidates[0].content.parts[0].text;
                chatWindow.innerHTML += `<br><br><span style="color:#00ff00">[GEMINI]:</span> ${aiResponse}`;
                terminal.innerHTML += `\\n> HTTP_200: OK`;
            } else {
                const msg = data.error ? data.error.message : "Unknown Error";
                chatWindow.innerHTML += `<br><br><span style="color:red">[API ERROR]: ${msg}</span>`;
                terminal.innerHTML += `\\n> HTTP_${response.status}: FAIL`;
            }
        } catch (err) {
            chatWindow.innerHTML += `<br><br><span style="color:red">[NETWORK ERROR]: ${err.message}</span>`;
        }
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    // 4. Event Listener for Input
    document.getElementById('user-prompt').addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            const text = this.value.trim();
            if(text) {
                document.getElementById('ai-chat').innerHTML += `<br><br><span style="color:#800080">[USER]:</span> ${text}`;
                callGemini(text);
                this.value = "";
            }
        }
    });
</script>
</body>
</html>
"""

# Render Component
components.html(cad_app_html, height=800)

# Auto-resize hack for Streamlit
st.components.v1.html(
    f"""<script>
        window.parent.document.querySelector('iframe').style.height = '95vh';
    </script>""",
    height=0
)
