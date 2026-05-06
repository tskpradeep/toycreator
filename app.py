import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="CAD Designer Pro")

# 1. CSS Styling
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stApp { background-color: #000 !important; overflow: hidden !important; }
        .block-container { padding: 0rem !important; max-width: 100% !important; height: 100vh !important; }
    </style>
""", unsafe_allow_html=True)

# 2. Main Application
cad_app_html = """
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/split.js/1.6.0/split.min.js"></script>
    <style>
        html, body { margin: 0; padding: 0; height: 100%; width: 100%; background: #000; font-family: monospace; color: white; overflow: hidden; }
        .master-container { display: flex; flex-direction: column; height: 100vh; border: 2px solid #333; }
        
        /* AI Config Modal */
        #ai-modular-setup {
            position: absolute; top: 15%; left: 20%; width: 60%; height: 60%;
            background: #000; border: 2px solid #00ff00; z-index: 9999;
            display: none; flex-direction: column; padding: 20px;
        }
        .ai-input, .ai-select { background: #111; border: 1px solid #00ff00; color: #00ff00; padding: 10px; margin-bottom: 20px; width: 100%; }
        
        /* Layout Panes */
        .window-title-bar { background: #1a1a1a; padding: 5px 10px; font-size: 12px; border-bottom: 1px solid #333; }
        #dynamic-zone { display: flex; flex: 1; min-height: 0; }
        .pane { background: #000; border: 1px solid #222; overflow: hidden; display: flex; flex-direction: column; }
        .gutter { background-color: #333; }
        
        /* Content Areas */
        .ai-text-area { flex: 1; padding: 10px; color: #00ff00; overflow-y: auto; white-space: pre-wrap; border-bottom: 1px solid #222; }
        .user-input-area { height: 100%; background: transparent; border: none; color: #800080; padding: 10px; outline: none; resize: none; font-weight: bold; }
        .cmd-text { height: 100%; color: #0f0; font-size: 11px; padding: 10px; overflow-y: auto; }
        
        .fixed-footer { height: 50px; background: #111; border-top: 1px solid #333; display: flex; align-items: center; padding: 0 10px; }
        .ai-btn { background: #e1e1e1; color: #000; padding: 5px 15px; cursor: pointer; font-weight: bold; }
    </style>
</head>
<body>

<div class="master-container">
    <div id="ai-modular-setup">
        <h3 style="color:#00ff00">AI SYSTEM CONFIG</h3>
        <label>SELECT MODEL:</label>
        <select id="version-select" class="ai-select">
            <option value="gemini-1.5-flash">Gemini 1.5 Flash (Fast)</option>
            <option value="gemini-1.5-pro">Gemini 1.5 Pro (Complex)</option>
        </select>
        <label>API KEY:</label>
        <input type="password" id="api-field-input" class="ai-input" placeholder="Paste Key Here...">
        <button class="ai-btn" onclick="saveConfig()">SAVE & CLOSE</button>
    </div>

    <div class="window-title-bar">CAD DESIGNER PRO v1.0</div>

    <div id="dynamic-zone">
        <div id="left-stack" style="width: 70%;">
            <div id="cad-pane" class="pane" style="height: 75%;">
                <div id="visual-monitor" style="padding:20px; color:#444;">[ CANVAS IDLE ]</div>
            </div>
            <div id="cmd-pane" class="pane" style="height: 25%;">
                <div id="terminal-out" class="cmd-text">>_ SYSTEM INITIALIZED</div>
            </div>
        </div>
        <div id="right-stack" style="width: 30%;">
            <div id="ai-output" class="pane" style="height: 50%;">
                <div id="ai-chat" class="ai-text-area">AWAITING CONNECTION...</div>
            </div>
            <div id="ai-input" class="pane" style="height: 50%;">
                <textarea id="user-prompt" class="user-input-area" placeholder="TYPE MESSAGE..."></textarea>
            </div>
        </div>
    </div>

    <div class="fixed-footer">
        <div class="ai-btn" onclick="toggleModal(true)">AI-SET ▲</div>
    </div>
</div>

<script>
    // Initialize Splits
    Split(['#left-stack', '#right-stack'], { sizes: [70, 30], gutterSize: 5 });
    
    function toggleModal(show) { 
        document.getElementById('ai-modular-setup').style.display = show ? 'flex' : 'none'; 
    }

    function saveConfig() {
        const key = document.getElementById('api-field-input').value.trim();
        const model = document.getElementById('version-select').value;
        if(key) {
            localStorage.setItem('gemini_key', key);
            localStorage.setItem('gemini_model', model);
            document.getElementById('terminal-out').innerHTML += `\\n> CONFIG UPDATED: ${model}`;
            toggleModal(false);
        }
    }

    async function callGemini(text) {
        const key = localStorage.getItem('gemini_key');
        const model = localStorage.getItem('gemini_model') || "gemini-1.5-flash";
        const chat = document.getElementById('ai-chat');
        const term = document.getElementById('terminal-out');

        if(!key) {
            chat.innerHTML += "\\n[ERROR] NO API KEY. CLICK AI-SET.";
            return;
        }

        term.innerHTML += `\\n> CALLING API: ${model}...`;
        
        try {
            const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${key}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ contents: [{ parts: [{ text: text }] }] })
            });

            const data = await response.json();
            const reply = data.candidates[0].content.parts[0].text;
            
            chat.innerHTML += `\\n\\n[GEMINI]: ${reply}`;
            term.innerHTML += `\\n> HTTP 200: OK`;
            chat.scrollTop = chat.scrollHeight;
        } catch (e) {
            chat.innerHTML += `\\n[ERROR] API FAILED.`;
            term.innerHTML += `\\n> ERROR: CHECK KEY OR NETWORK`;
        }
    }

    document.getElementById('user-prompt').addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            const val = this.value.trim();
            if(val) {
                document.getElementById('ai-chat').innerHTML += `\\n\\n[USER]: ${val}`;
                callGemini(val);
                this.value = "";
            }
        }
    });
</script>
</body>
</html>
"""

components.html(cad_app_html, height=800)
