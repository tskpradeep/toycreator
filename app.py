# app.py

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="CAD Designer Pro")

st.markdown("""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
.stApp { background:#000 !important; overflow:hidden !important; }
.block-container{
padding:0rem !important;
max-width:100% !important;
height:100vh !important;
overflow:hidden !important;
}
</style>
""", unsafe_allow_html=True)

with open("aiset.html","r",encoding="utf-8") as f:
    aiset_window = f.read()

cad_app_html = """
<script src="https://cdnjs.cloudflare.com/ajax/libs/split.js/1.6.0/split.min.js"></script>

<style>
html, body {
margin:0; padding:0; height:100%; width:100%;
overflow:hidden !important; background:#000;
font-family:'Segoe UI',Tahoma,sans-serif; color:white;
}

.master-container{
display:flex; flex-direction:column;
height:100vh; width:100vw; background:#000;
border:2px solid #d3d3d3; box-sizing:border-box;
position:relative;
}
""" + """
#ai-modular-setup{
position:absolute; top:10%; left:15%; width:70%; height:75%;
z-index:9999;
display:none;
}
""" + """
.ai-setup-header{
background:#0a1a0a; border-bottom:1px solid #00ff00;
padding:10px; display:flex; justify-content:space-between;
color:#00ff00; font-family:monospace; font-weight:bold;
align-items:center;
}

.ai-header-controls{display:flex; gap:10px; align-items:center;}
.ai-setup-body{display:flex; flex:1; overflow:hidden;}
.ai-setup-sidebar{
width:30%; border-right:1px solid #00ff00;
padding:10px; background:#050505; overflow-y:auto;
}

.ai-setup-content{
width:70%; padding:25px; color:#00ff00;
font-family:monospace; display:flex;
flex-direction:column; gap:20px;
overflow-y:auto;
}

.ai-tool-item{
padding:12px; border:1px solid #004400;
margin-bottom:8px; cursor:pointer; font-size:12px;
transition:0.2s;
}
.ai-tool-item:hover{border-color:#00ff00; background:#0a2a0a;}
.ai-tool-item.active{background:#00ff00; color:#000; font-weight:bold;}

.ai-select{
background:#000; border:1px solid #00ff00; color:#00ff00;
padding:10px; width:100%; outline:none; cursor:pointer;
font-family:monospace; appearance:none;
}

.ai-input{
background:#000; border:1px solid #00ff00; color:#00ff00;
padding:10px; width:100%; outline:none; box-sizing:border-box;
}

.title-action-btn{
padding:2px 12px; font-size:10px; cursor:pointer;
border:1px solid #00ff00; background:#000; color:#00ff00;
font-family:monospace; text-transform:uppercase;
}
.title-action-btn:hover{background:#00ff00; color:#000;}
.title-action-btn.close{border-color:#fff; color:#fff;}

.window-title-bar{
background:#1a1a1a; color:#888; height:30px; flex-shrink:0;
display:flex; align-items:center; justify-content:space-between;
padding:0 10px; font-size:12px; border-bottom:1px solid #333;
}

#dynamic-zone{
display:flex; flex-direction:row; flex:1; min-height:0; width:100%;
}

.fixed-right-strip{
width:65px; border-left:1px solid #333;
display:grid; grid-template-columns:1fr 1fr;
grid-auto-rows:min-content; gap:2px; padding:5px;
background:#000; overflow-y:scroll;
}

.btn-cell{
aspect-ratio:1/1; width:20px; height:20px; background:#e1e1e1;
color:#000; border-top:2px solid #fff; border-left:2px solid #fff;
border-right:2px solid #707070; border-bottom:2px solid #707070;
cursor:pointer; display:flex; align-items:center;
justify-content:center; box-sizing:border-box; flex-shrink:0;
}

.btn-cell:active{
border-top:2px solid #707070; border-left:2px solid #707070;
border-right:2px solid #fff; border-bottom:2px solid #fff;
background:#bebebe;
}

.pane{
background:#000 !important; border:1px solid #333 !important;
overflow:hidden; display:flex; align-items:center;
justify-content:center; box-sizing:border-box;
}

.gutter{background:#444 !important;}

.fixed-footer{
height:64px; display:flex; flex-direction:row;
border-top:2px solid #333; background:#000;
flex-shrink:0; align-items:flex-end;
padding:0px 4px 2px 4px;
}

.footer-left-content{
flex:1; display:flex; height:100%;
align-items:center; padding-left:10px;
}

.selection-b-container{width:130px; height:62px; margin-left:5px;}
.selection-a-stack{
display:flex; flex-direction:column; gap:1px;
width:130px; margin-left:5px;
}

.footer-palette-grid{
display:grid; grid-template-columns:repeat(6,20px);
grid-template-rows:repeat(3,20px); gap:1px; margin-left:8px;
}

.dropup{
position:relative; width:100%; height:20px;
background:#e1e1e1; color:#000; border:1px solid #707070;
display:flex; align-items:center; justify-content:space-between;
padding:0 5px; cursor:pointer; font-size:9px;
box-sizing:border-box;
}

.dropup.tall{height:62px;}

.dropup-content{
display:none; position:absolute; bottom:100%; left:-1px;
background:#f0f0f0; min-width:140px;
border:1px solid #707070; z-index:1000;
}

.dropup.active .dropup-content{display:block;}

.dropup-content a{
color:#000; padding:6px; text-decoration:none;
display:block; border-bottom:1px solid #ccc; font-size:10px;
}

.text-main{
color:#b22222; font-size:1.4vw; font-weight:bold;
text-align:center; width:100%; height:100%;
overflow:auto; display:flex; flex-direction:column;
align-items:center; justify-content:center;
}

.ai-text-area{
width:100%; height:100%; padding:10px; color:#00ff00;
font-family:'Consolas',monospace; font-size:13px;
overflow-y:auto; text-align:left;
}

.user-input-area{
width:100%; height:100%; background:transparent;
border:none; color:#800080; padding:10px;
font-family:'Consolas',monospace; outline:none;
resize:none; font-weight:bold;
}

.cmd-text{
width:100%; height:100%; color:#0f0;
font-family:monospace; font-size:11px;
padding:5px; overflow-y:auto; white-space:pre-wrap;
}
</style>

<div class="master-container">

<div id="ai-modular-setup">
""" + aiset_window + """
</div>

<!-- REST OF YOUR ORIGINAL HTML BELOW UNCHANGED -->
""" + """
"""  # keep remaining original html exactly same from your code after AI-SET block

components.html(cad_app_html, height=0)

st.components.v1.html(
"""
<script>
window.parent.document.querySelector('iframe').style.height='94vh';
</script>
""",
height=0
)
