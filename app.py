# app.py

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="CAD Designer Pro")

st.markdown("""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
.stApp {background:#000 !important;overflow:hidden !important;}
.block-container{
padding:0rem !important;
max-width:100% !important;
height:100vh !important;
overflow:hidden !important;
}
</style>
""", unsafe_allow_html=True)

with open("aiset.html", "r", encoding="utf-8") as f:
    aiset_html = f.read()

cad_app_html = """
<script src="https://cdnjs.cloudflare.com/ajax/libs/split.js/1.6.0/split.min.js"></script>

<style>
html,body{
margin:0;padding:0;height:100%;width:100%;
overflow:hidden;background:#000;color:#fff;
font-family:Segoe UI,Tahoma,sans-serif;
}
.master-container{
display:flex;flex-direction:column;
height:100vh;width:100vw;
background:#000;border:2px solid #d3d3d3;
box-sizing:border-box;position:relative;
}
#ai-modular-setup{
position:absolute;top:10%;left:15%;
width:70%;height:75%;
display:none;z-index:9999;
}
.window-title-bar{
background:#1a1a1a;color:#888;
height:30px;display:flex;
align-items:center;justify-content:space-between;
padding:0 10px;font-size:12px;
border-bottom:1px solid #333;
}
#dynamic-zone{
display:flex;flex:1;min-height:0;width:100%;
}
.fixed-right-strip{
width:65px;border-left:1px solid #333;
display:grid;grid-template-columns:1fr 1fr;
grid-auto-rows:min-content;gap:2px;
padding:5px;background:#000;overflow-y:scroll;
}
.btn-cell{
width:20px;height:20px;background:#e1e1e1;
border-top:2px solid #fff;
border-left:2px solid #fff;
border-right:2px solid #707070;
border-bottom:2px solid #707070;
}
.pane{
background:#000;border:1px solid #333;
display:flex;overflow:hidden;
align-items:center;justify-content:center;
}
.gutter{background:#444 !important;}
.fixed-footer{
height:64px;display:flex;
border-top:2px solid #333;
background:#000;
align-items:flex-end;
padding:0 4px 2px 4px;
}
.footer-left-content{
flex:1;display:flex;height:100%;
align-items:center;padding-left:10px;
}
.selection-a-stack{
display:flex;flex-direction:column;
gap:1px;width:130px;margin-left:5px;
}
.selection-b-container{
width:130px;height:62px;margin-left:5px;
}
.footer-palette-grid{
display:grid;
grid-template-columns:repeat(6,20px);
grid-template-rows:repeat(3,20px);
gap:1px;margin-left:8px;
}
.dropup{
width:100%;height:20px;
background:#e1e1e1;color:#000;
border:1px solid #707070;
display:flex;align-items:center;
justify-content:space-between;
padding:0 5px;font-size:9px;
}
.dropup.tall{height:62px;}
.text-main{
color:#b22222;font-size:1.4vw;
font-weight:bold;width:100%;height:100%;
display:flex;align-items:center;
justify-content:center;
}
.ai-text-area{
width:100%;height:100%;
padding:10px;color:#00ff00;
font-family:Consolas,monospace;
font-size:13px;overflow-y:auto;
}
.user-input-area{
width:100%;height:100%;
background:transparent;border:none;
color:#800080;padding:10px;
font-family:Consolas,monospace;
resize:none;outline:none;
font-weight:bold;
}
.cmd-text{
width:100%;height:100%;
color:#0f0;font-family:monospace;
font-size:11px;padding:5px;
white-space:pre-wrap;overflow-y:auto;
}
</style>

<div class="master-container">

<div id="ai-modular-setup">
""" + aiset_html + """

</div>

<div class="window-title-bar">
<div>CAD DESIGNER PRO</div>
<div><span>−</span><span style="margin:0 10px;">❐</span><span>×</span></div>
</div>

<div id="dynamic-zone">

<div id="split-container" style="display:flex;flex:1;width:100%;">

<div id="left-stack" style="display:flex;flex-direction:column;width:70%;">
<div id="cad-pane" class="pane text-main">
<div style="color:#444;font-size:12px;font-family:monospace;">
[ IDLE: AWAITING CIRCUIT REQUEST ]
</div>
</div>

<div id="cmd-pane" class="pane" style="justify-content:flex-start;align-items:flex-start;">
<div id="terminal-out" class="cmd-text">>_ SYSTEM INITIALIZED</div>
</div>
</div>

<div id="right-stack" style="display:flex;flex-direction:column;width:30%;">
<div id="ai-output" class="pane">
<div id="ai-chat" class="ai-text-area">AI TEXT REPLYING WINDOW</div>
</div>

<div id="ai-input" class="pane">
<textarea id="user-prompt" class="user-input-area" placeholder="TYPE HERE..."></textarea>
</div>
</div>

</div>

<div class="fixed-right-strip" id="side-strip"></div>
</div>

<div class="fixed-footer">

<div class="footer-left-content">
<span style="color:#008000;font-size:11px;margin-right:20px;">READY</span>
<span style="color:#0000ff;font-size:11px;">SYSTEM STATUS: ONLINE</span>
</div>

<div id="foot-palette" class="footer-palette-grid"></div>

<div class="selection-a-stack">
<div class="dropup"><span>File</span><span>▲</span></div>
<div class="dropup"><span>Tools</span><span>▲</span></div>
<div class="dropup"><span>View</span><span>▲</span></div>
</div>

<div class="selection-b-container">
<div class="dropup tall" onclick="toggleAISet(true)">
<span>AI-SET</span><span>▲</span>
</div>
</div>

</div>
</div>

<script>
Split(['#left-stack','#right-stack'],{sizes:[70,30],gutterSize:4});
Split(['#cad-pane','#cmd-pane'],{direction:'vertical',sizes:[80,20],gutterSize:4});
Split(['#ai-output','#ai-input'],{direction:'vertical',sizes:[50,50],gutterSize:4});

for(let i=0;i<100;i++){
document.getElementById('side-strip').innerHTML += '<div class="btn-cell"></div>';
}

for(let i=0;i<18;i++){
document.getElementById('foot-palette').innerHTML += '<div class="btn-cell"></div>';
}

function toggleAISet(show){
document.getElementById('ai-modular-setup').style.display = show ? 'block':'none';
}
</script>
"""

components.html(cad_app_html, height=0)

st.components.v1.html("""
<script>
window.parent.document.querySelector('iframe').style.height='94vh';
</script>
""", height=0)
