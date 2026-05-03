import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# Initialize the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server 

# Layout logic
app.layout = html.Div([
    # TOP SECTION
    html.Div([
        # Left CAD Window
        html.Div("visual displays dynamic between coding and screen/CAD designs", 
                 style={"flex": "7", "border": "3px solid black", "margin": "5px", "color": "darkred", "fontWeight": "bold", "fontSize": "22px", "display": "flex", "alignItems": "center", "justifyContent": "center", "backgroundColor": "white"}),
        
        # RED LINE (The Separator)
        html.Div(style={"width": "10px", "backgroundColor": "red", "cursor": "col-resize"}),
        
        # AI SIDEBAR
        html.Div([
            html.Div("AI TEXT REPLYING WINDOW", style={"flex": "1", "border": "3px solid black", "margin": "5px", "color": "green", "display": "flex", "alignItems": "center", "justifyContent": "center", "backgroundColor": "white"}),
            # GREEN LINE
            html.Div(style={"height": "10px", "backgroundColor": "green", "cursor": "row-resize"}),
            html.Div("USER PROMPTING", style={"flex": "1", "border": "3px solid black", "margin": "5px", "color": "purple", "display": "flex", "alignItems": "center", "justifyContent": "center", "backgroundColor": "white"}),
        ], style={"flex": "3", "display": "flex", "flexDirection": "column"}),
        
        # BUTTON STRIP
        html.Div([html.Div(style={"width": "30px", "height": "30px", "border": "1px solid black", "margin": "2px", "backgroundColor": "#ddd"}) for _ in range(16)], 
                 style={"width": "50px", "borderLeft": "3px solid black", "display": "flex", "flexWrap": "wrap", "justifyContent": "center", "padding": "5px"})
        
    ], style={"display": "flex", "height": "70vh"}),

    # MAIN GREEN LINE
    html.Div(style={"height": "10px", "backgroundColor": "green", "width": "100%", "cursor": "row-resize"}),

    # BOTTOM SECTION
    html.Div([
        html.Div("command prompt / system programming / project", style={"color": "darkred", "fontWeight": "bold", "padding": "10px"}),
        html.Div([
            html.Div("small indicators", style={"border": "2px solid black", "flex": "1", "margin": "5px", "color": "green", "padding": "5px"}),
            html.Div("buttons for controlling", style={"border": "2px solid black", "flex": "3", "margin": "5px", "color": "blue", "padding": "5px"}),
            html.Div([html.Div(style={"width": "30px", "height": "30px", "border": "1px solid black", "margin": "2px", "backgroundColor": "#ddd"}) for _ in range(8)], 
                     style={"flex": "1", "display": "flex", "flexWrap": "wrap", "justifyContent": "center"})
        ], style={"display": "flex"})
    ], style={"height": "25vh", "backgroundColor": "white", "border": "3px solid black", "margin": "5px"})

], style={"height": "100vh", "backgroundColor": "#f8f9fa", "padding": "10px", "overflow": "hidden"})

# IMPORTANT: Do not add app.run() if you are on a cloud host
