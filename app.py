import dash
from dash import html
import dash_bootstrap_components as dbc

# This version uses standard layout to avoid the TypeError loop
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server 

# Styles to match image_0d35a5.png
box_border = {"border": "2px solid black", "padding": "10px", "height": "100%", "backgroundColor": "white"}
red_line = {"width": "5px", "backgroundColor": "red", "height": "100%"}
green_line_h = {"height": "5px", "backgroundColor": "green", "width": "100%"}
small_box = {"width": "30px", "height": "30px", "border": "1px solid black", "margin": "2px", "display": "inline-block"}

app.layout = html.Div([
    # MAIN TOP SECTION (Visuals, AI, and Buttons)
    html.Div([
        # 1. Left: Visual Display
        html.Div("visual displays dynamic between coding and screen/CAD designs", 
                 style={**box_border, "flex": "6", "fontSize": "24px", "fontWeight": "bold", "color": "darkred"}),
        
        # 2. RED LINE
        html.Div(style=red_line),
        
        # 3. Middle: AI Sidebar
        html.Div([
            html.Div("AI TEXT REPLYING WINDOW", style={**box_border, "flex": "1", "color": "green"}),
            html.Div(style=green_line_h), # Inner Green Line
            html.Div("USER PROMPTING", style={**box_border, "flex": "1", "color": "purple"}),
        ], style={"flex": "3", "display": "flex", "flexDirection": "column"}),
        
        # 4. Right: Button Strip
        html.Div([html.Div(style=small_box) for _ in range(20)], 
                 style={"flex": "0.5", "padding": "5px", "borderLeft": "2px solid black", "display": "flex", "flexWrap": "wrap", "justifyContent": "center"}),
        
    ], style={"display": "flex", "height": "70vh"}),

    # MAIN GREEN LINE
    html.Div(style=green_line_h),

    # BOTTOM SECTION (Console and Grid)
    html.Div([
        html.Div("command prompt / system programming / project", 
                 style={**box_border, "height": "15vh", "color": "darkred"}),
        
        # Footer Row
        html.Div([
            html.Div("small indicators any", style={**box_border, "flex": "1", "color": "green"}),
            html.Div("buttons for controlling we will decide buttons as and when we", style={**box_border, "flex": "3", "color": "blue"}),
            html.Div([html.Div(style=small_box) for _ in range(12)], 
                     style={**box_border, "flex": "1", "display": "flex", "flexWrap": "wrap"}),
        ], style={"display": "flex", "height": "10vh"})
        
    ], style={"height": "25vh"})

], style={"height": "100vh", "padding": "10px", "backgroundColor": "white", "overflow": "hidden"})

if __name__ == "__main__":
    app.run_server(debug=True)
