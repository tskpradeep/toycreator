import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai

# --- 1. SETTINGS ---
# Paste your key from Google AI Studio between the quotes
API_KEY = "AIzaSyDKkohD9a0D0AF1yMr5QDzCzDUEUjebfSs"

if API_KEY != "AIzaSyDKkohD9a0D0AF1yMr5QDzCzDUEUjebfSs":
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None

st.set_page_config(layout="wide", page_title="CAD Designer Pro")

# --- 2. THE DESIGN (CLEAN & MINIMAL) ---
st.markdown("""
    <style>
        #MainMenu, footer, header {visibility: hidden;}
        .stApp { background-color: #000 !important; overflow: hidden !important; }
        .block-container { padding: 0rem !important; max-width: 100% !important; height: 100vh !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. YOUR FULL GUI (RESTORED & PROTECTED) ---
cad_app_html = f"""
<script src="https://cdnjs.cloudflare.com/ajax/libs/split.js/1.6.0/split.min.js"></script>
<style>
    html, body {{ margin: 0; padding: 0; height: 100%; width: 100%; background: #000; font-family: 'Segoe UI', sans-serif; color: white; overflow: hidden; }}
    .master-container {{ display: flex; flex-direction: column; height: 100vh; border: 2px solid #d3d3d3; box-sizing: border-box; }}
    
    /* AI-SET WINDOW */
    #ai-modular-setup {{ position: absolute; top: 10%; left: 15%; width: 70%; height: 75%; background: #000; border: 2px solid #00ff00; z-index: 9999; display: none; flex-direction: column; box-shadow: 0 0 50px rgba(0,255,0,0.3); }}
    .ai-setup-header {{ background: #0a1a0a; border-bottom: 1px solid #00ff00; padding: 10px; color: #00ff00; font-family: monospace; display: flex; justify-content: space-between; }}
    .ai-setup-body {{ display: flex; flex: 1; }}
    .ai-setup-sidebar {{ width: 30%; border-right: 1px solid #00ff00; padding: 10px; background: #050505; }}
    .ai-setup-content {{ width: 70%; padding: 25px; color: #00ff00; font-family: monospace; }}
    
    /* PANES */
    .pane {{ background: #000; border: 1px solid #333; display: flex; align-items: center; justify-content: center; overflow: hidden; }}
    .ai-text-area {{ width: 100%; height: 100%; padding: 10px; color: #008000; font-family: 'Consolas', monospace; font-size: 13px; overflow-y: auto; text-align: left; }}
    .user-input-area {{ width: 100%; height: 100%; background: transparent; border: none; color: #800080; padding: 10px; font-family: 'Consolas', monospace; outline: none; resize: none; font-weight: bold; }}
    .footer {{ height: 64px; border-top: 2px solid #333; display: flex; align-items: center; padding: 0 10px; background: #000; }}
</style>

<div class="master-container">
    <div id="ai-modular-setup">
        <div class="ai-setup-header"><span>[ SYSTEM AI-SET ]</span><span onclick="toggleAISet(false)" style="cursor:pointer;">[ X ]</span></div>
        <div class="ai-setup-body">
            <div class="ai-setup-sidebar"><div style="padding:10px; border:1px solid #00ff00; background:#00ff00; color:#000;">GEMINI CORE</div></div>
            <div class="ai-setup-content">
                <div style="font-size: 20px; color:#fff;">ENGINE: GEMINI 1.5</div>
                <p>Status: Online / Ready</p>
                <button style="width: 120px; height: 35px; background:#00ff00; border:none; font-weight:bold;" onclick="toggleAISet(false)">SAVE & CLOSE</button>
            </div>
        </div>
    </div>

    <div style="background:#1a1a1a; height:30px; border-bottom:1px solid #333; display:flex; align-items:center; padding:0 10px; font-size:12px; color:#888;">CAD DESIGNER PRO</div>

    <div style="display:flex; flex:1; min-height:0;">
        <div id="left-stack" style="width:70%; display:flex; flex-direction:column;">
            <div class="pane" style="height:80%; color:#b22222; font-weight:bold;">VISUAL MONITOR</div>
            <div class="pane" style="height:20%; color:#0f0; font-family:monospace; font-size:11px; justify-content:flex-start; padding:5px;">>_ SYSTEM READY</div>
        </div>
        <div id="right-stack" style="width:30%; display:flex; flex-direction:column;">
            <div class="pane" style="height:70%;"><div id="ai-chat" class="ai-text-area">GEMINI STANDBY...</div></div>
            <div class="pane" style="height:30%;"><textarea id="user-prompt" class="user-input-area" placeholder="TYPE HERE..."></textarea></div>
        </div>
    </div>

    <div class="footer">
        <div style="flex:1; color:#008000; font-size:11px;">READY | SECURE OFFLINE INTERFACE</div>
        <div style="background:#e1e1e1; color:#000; padding:15px; font-size:10px; font-weight:bold; cursor:pointer;" onclick="toggleAISet(true)">AI-SET ▲</div>
    </div>
</div>

<script>
    function toggleAISet(show) {{ document.getElementById('ai-modular-setup').style.display = show ? 'flex' : 'none'; }}
    
    const promptInput = document.getElementById('user-prompt');
    const chatWindow = document.getElementById('ai-chat');

    promptInput.addEventListener('keydown', function(e) {{
        if (e.key === 'Enter' && !e.shiftKey) {{
            e.preventDefault();
            const text = promptInput.value.trim();
            if(text !== "") {{
                chatWindow.innerHTML += "<br><br><span style='color:#800080'>[USER]:</span> " + text;
                // Communication to Python
                window.parent.postMessage({{type: 'streamlit:setComponentValue', value: text}}, '*');
                promptInput.value = "";
            }}
        }}
    }});

    window.addEventListener('message', function(e) {{
        if(e.data.type === 'GEMINI_REPLY') {{
            chatWindow.innerHTML += "<br><br><span style='color:#00ff00'>[GEMINI]:</span> " + e.data.content;
            chatWindow.scrollTop = chatWindow.scrollHeight;
        }}
    }});
</script>
"""

# --- 4. BACKEND BRIDGE ---
user_query = components.html(cad_app_html, height=0)

# Make the UI full screen
components.html("<script>window.parent.document.querySelector('iframe').style.height = '94vh';</script>", height=0)

if user_query:
    if model:
        response = model.generate_content(user_query)
        # Clean the text for Javascript safety
        ai_reply = response.text.replace("'", "\\'").replace("\\n", "<br>") 
        components.html(f"<script>window.parent.postMessage({{type: 'GEMINI_REPLY', content: '{ai_reply}'}}, '*');</script>", height=0)
    else:
        st.warning("Please check AI-SET for connection status.")
