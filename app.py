import streamlit as st
import streamlit.components.v1 as components
import os

st.set_page_config(layout="wide", page_title="CAD Designer Pro")

st.markdown("""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

.stApp{
background:#000 !important;
overflow:hidden !important;
}

.block-container{
padding:0rem !important;
max-width:100% !important;
height:100vh !important;
overflow:hidden !important;
}

iframe{
width:100% !important;
border:none !important;
}
</style>
""", unsafe_allow_html=True)

# FIXED PATH + LOAD HTML
html_file = "main_window.html"

if os.path.isfile(html_file):
    with open(html_file, "r", encoding="utf-8") as f:
        page = f.read()
else:
    page = """
    <html>
    <body style="margin:0;background:black;color:red;font-family:monospace;">
    <div style="padding:30px;">
    ERROR:<br><br>
    main_window.html not found.<br>
    Upload both files in same GitHub folder:
    <br><br>
    app.py<br>
    main_window.html
    </div>
    </body>
    </html>
    """

components.html(page, height=940, scrolling=False)
