import dash
from dash import html
import dash_bootstrap_components as dbc

# Initialize the app with a clean theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
server = app.server 

# Explicit styles to override dark mode/black screens
box_border = {
    "border": "3px solid #000000", 
    "padding": "10px", 
    "height": "100%", 
    "backgroundColor": "#FFFFFF", 
    "color": "#000000",
    "display": "flex",
    "alignItems": "center",
    "justifyContent": "center",
    "textAlign": "center"
}

red_line = {"width": "10px", "backgroundColor": "red", "height": "100%"}
green_line_h = {"height": "10px", "backgroundColor": "green", "width": "100%"}
small_box = {"width": "35px", "height": "35px", "border": "2px solid black", "margin": "2px", "display": "inline-block", "backgroundColor": "#EEE"}

app.layout = html.Div([
    # MAIN WRAPPER (FORCING WHITE BACKGROUND)
    html.Div([
        
        # TOP HALF
        html.Div([
            # 1. Visual Display
            html.Div("visual displays dynamic between coding and screen/CAD designs", 
                     style={**box_border, "flex": "6", "fontSize": "24px", "fontWeight": "bold", "color": "darkred"}),
            
            # RED LINE
            html.Div(style=red_line),
            
            # AI SIDEBAR
            html.Div([
                html.Div("AI TEXT REPLYING WINDOW", style={**box_border, "flex": "1", "color": "green"}),
                html.Div(style=green_line_h), 
                html.Div("USER PROMPTING", style={**box_border, "flex": "1", "color": "purple"}),
            ], style={"flex": "3", "display": "flex", "flexDirection": "column"}),
            
            # RIGHT BUTTONS
            html.Div([html.Div(style=small_box) for _ in range(20)], 
                     style={"flex": "1", "padding": "5px", "borderLeft": "3px solid black", "display": "flex", "flexWrap": "wrap", "justifyContent": "center"}),
            
        ], style={"display": "flex", "height": "65vh"}),

        # MIDDLE GREEN LINE
        html.Div(style=green_line_h),

        # BOTTOM HALF
        html.Div([
            html.Div("command prompt / system programming / project", 
                     style={**box_border, "height": "15vh", "color": "darkred"}),
            
            # FOOTER
            html.Div([
                html.Div("small indicators any", style={**box_border, "flex": "1", "color": "green"}),
                html.Div("buttons for controlling", style={**box_border, "flex": "3", "color": "blue"}),
                html.Div([html.Div(style=small_box) for _ in range(12)], 
                         style={**box_border, "flex": "1", "display": "flex", "flexWrap": "wrap"}),
            ], style={"display": "flex", "height": "15vh"})
            
        ], style={"height": "30vh"})

    ], style={"backgroundColor": "white", "height": "100vh", "padding": "10px"})
], style={"backgroundColor": "white"})

# NO app.run() here—just let the server handle it
