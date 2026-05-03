import streamlit as st

# 1. Set the page to wide mode to match a dashboard layout
st.set_page_config(layout="wide")

# 2. CSS to force the exact colors and lines from image_0d35a5.png
st.markdown("""
    <style>
    .main-box {
        border: 2px solid black;
        padding: 15px;
        background-color: white;
        height: 450px;
        color: darkred;
        font-weight: bold;
        font-size: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .red-line {
        background-color: red;
        width: 10px;
        height: 100%;
    }
    .green-line-v {
        background-color: green;
        width: 10px;
        height: 100%;
    }
    .green-line-h {
        background-color: green;
        height: 10px;
        width: 100%;
        margin: 10px 0;
    }
    .ai-box {
        border: 2px solid black;
        background-color: white;
        height: 215px;
        padding: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .btn-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 5px;
    }
    .small-btn {
        border: 1px solid black;
        height: 30px;
        width: 30px;
        background: #f0f0f0;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. TOP SECTION
col1, red, col2, buttons = st.columns([6, 0.2, 3, 0.5])

with col1:
    st.markdown('<div class="main-box">visual displays dynamic between coding and screen/CAD designs</div>', unsafe_allow_html=True)

with red:
    st.markdown('<div class="red-line"></div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="ai-box" style="color: green;">AI TEXT REPLYING WINDOW</div>', unsafe_allow_html=True)
    st.markdown('<div class="green-line-h"></div>', unsafe_allow_html=True)
    st.markdown('<div class="ai-box" style="color: purple;">USER PROMPTING</div>', unsafe_allow_html=True)

with buttons:
    # Small vertical button strip
    for _ in range(12):
        st.markdown('<div class="small-btn"></div>', unsafe_allow_html=True)

# 4. MIDDLE SEPARATOR
st.markdown('<div class="green-line-h"></div>', unsafe_allow_html=True)

# 5. BOTTOM SECTION
st.markdown('<div style="border: 2px solid black; padding: 10px; color: darkred; height: 100px;">command prompt for system programming for project</div>', unsafe_allow_html=True)

foot1, foot2, foot3 = st.columns([1, 3, 1])
with foot1:
    st.markdown('<div style="border: 2px solid black; padding: 5px; color: green;">small indicators any</div>', unsafe_allow_html=True)
with foot2:
    st.markdown('<div style="border: 2px solid black; padding: 5px; color: blue;">buttons for controlling we will decide buttons as and when we</div>', unsafe_allow_html=True)
with foot3:
    st.markdown('<div class="btn-grid">' + '<div class="small-btn"></div>'*8 + '</div>', unsafe_allow_html=True)
