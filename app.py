# app.py

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="CAD Designer Pro")

st.markdown("""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
.stApp {background:#000;}
.block-container{padding:0rem;max-width:100%;height:100vh;}
</style>
""", unsafe_allow_html=True)

html = """
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
border:2px solid #d3d3d3;
box-sizing:border-box;
}
.window-title-bar{
background:#1a1a1a;color:#888;
height:30px;display:flex;
align-items:center;justify-content:space-between;
padding:0 10px;font-size:12px;
border-bottom:1px solid #333;
}
#dynamic-zone{
display:flex;flex:1;width:100%;
}
.pane{
background:#000;border:1px solid #333;
overflow:hidden;display:flex;
align-items:center;justify-content:center;
}
.text-main{
color:#b22222;font-size:1.4vw;font-weight:bold;
}
.ai-text-area{
width:100%;height:100%;padding:10px;
color:#00ff00;font-family:Consolas;
font-size:13px;overflow-y:auto;
}
.user-input-area{
width:100%;height:100%;
background:transparent;border:none;
color:#800080;padding:10px;
font-family:Consolas;outline:none;
resize:none;font-weight:bold;
}
.cmd-text{
width:100%;height:100%;
color:#0f0;font-family:monospace;
font-size:11px;padding:5px;
white-space:pre-wrap;
overflow-y:auto;
}
.fixed-footer{
height:64px;
display:flex;
align-items:flex-end;
border-top:2px solid #333;
background:#000;
padding:0 4px 2px 4px;
}
.dropbtn{
width:130px;height:62px;
background:#e1e1e1;color:#000;
border:1px solid #707070;
cursor:pointer;font-size:12px;
}
</style>

<div class="master-container">

<div class="window-title-bar">
<div>CAD DESIGNER PRO</div>
<div>− ❐ ×</div>
</div>

<div id="dynamic-zone">

<div id="split-container" style="display:flex;flex:1;">

<div id="left-stack" style="display:flex;flex-direction:column;width:70%;">

<div id="cad-pane" class="pane text-main">
<div>[ IDLE: AWAITING CIRCUIT REQUEST ]</div>
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

</div>

<div class="fixed-footer">
<button class="dropbtn" onclick="openAISet()">AI-SET ▲</button>
</div>

</div>

<script>
Split(['#left-stack','#right-stack'],{sizes:[70,30],gutterSize:4});
Split(['#cad-pane','#cmd-pane'],{direction:'vertical',sizes:[80,20],gutterSize:4});
Split(['#ai-output','#ai-input'],{direction:'vertical',sizes:[50,50],gutterSize:4});

function openAISet(){
window.open("aiset.html","aiset","width=900,height=700");
}

async function callGemini(promptText){

const apiKey = localStorage.getItem("gemini_api_key");
const model = localStorage.getItem("gemini_model") || "gemini-2.5-flash";
const apiUrl = localStorage.getItem("gemini_url") || "https://generativelanguage.googleapis.com/v1beta/models/";

const chat = document.getElementById("ai-chat");
const term = document.getElementById("terminal-out");

if(!apiKey){
chat.innerHTML += "<br><span style='color:red'>[ERROR]: OPEN AI-SET</span>";
return;
}

try{

term.innerHTML += "\\n> API_CALL STARTED";

const r = await fetch(`${apiUrl}${model}:generateContent?key=${apiKey}`,{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({
contents:[{parts:[{text:promptText}]}]
})
});

const d = await r.json();

const txt = d.candidates?.[0]?.content?.parts?.[0]?.text || "No text returned.";

chat.innerHTML += "<br><span style='color:#00ff00'>[GEMINI]:</span> " + txt;
chat.scrollTop = chat.scrollHeight;

term.innerHTML += "\\n> SUCCESS";

}catch(e){
chat.innerHTML += "<br><span style='color:red'>[API ERROR]</span>";
}

}

document.getElementById("user-prompt").addEventListener("keydown",function(e){

if(e.key==="Enter" && !e.shiftKey){
e.preventDefault();

const t=this.value.trim();

if(t!==""){

document.getElementById("ai-chat").innerHTML += "<br><br><span style='color:#800080'>[USER]:</span> "+t;

callGemini(t);

this.value="";
}
}

});
</script>
"""

components.html(html, height=940)
