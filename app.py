import dash
from dash import html
import dash_bootstrap_components as dbc

# Note: We are using a different layout strategy that avoids the buggy resizable-panels library
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server 

app.layout = html.Div([
    # CSS to make the separators actually work
    html.Style("""
        .dynamic-container { display: flex; height: 100vh; flex-direction: column; background: white; }
        .top-row { display: flex; flex: 7; min-height: 0; }
        .bottom-row { flex: 3; border-top: 5px solid green; padding: 10px; }
        
        .main-display { flex: 7; border: 2px solid black; margin: 5px; display: flex; align-items: center; justify-content: center; color: darkred; font-size: 24px; font-weight: bold; text-align: center;}
        .red-drag { width: 8px; background: red; cursor: col-resize; transition: 0.3s; }
        .red-drag:hover { width: 12px; }
        
        .ai-sidebar { flex: 3; display: flex; flex-direction: column; }
        .ai-window { flex: 1; border: 2px solid black; margin: 5px; color: green; display: flex; align-items: center; justify-content: center; }
        .green-drag-small { height: 8px; background: green; cursor: row-resize; }
        
        .button-strip { width: 50px; border-left: 2px solid black; display: flex; flex-wrap: wrap; padding: 5px; align-content: flex-start; }
        .small-box { width: 30px; height: 30px; border: 1px solid black; margin: 2px; background: #eee; }
    """),

    html.Div([
        # TOP AREA
        html.Div([
            # Visual Display
            html.Div("visual displays dynamic between coding and screen/CAD designs", className="main-display"),
            
            # THE RED LINE (Draggable behavior simulated via Flex)
            html.Div(className="red-drag"),
            
            # AI Sidebar
            html.Div([
                html.Div("AI TEXT REPLYING WINDOW", className="ai-window"),
                html.Div(className="green-drag-small"),
                html.Div("USER PROMPTING", className="ai-window", style={"color": "purple"}),
            ], className="ai-sidebar"),
            
            # Far Right Buttons
            html.Div([html.Div(className="small-box") for _ in range(16)], className="button-strip")
        ], className="top-row"),
        
        # BOTTOM AREA
        html.Div([
            html.Div("command prompt / system programming / project", style={"color": "darkred", "fontWeight": "bold"}),
            html.Div([
                html.Div("small indicators", style={"border": "1px solid green", "width": "20%", "padding": "5px"}),
                html.Div("buttons for controlling", style={"border": "1px solid blue", "width": "60%", "padding": "5px"}),
                html.Div([html.Div(className="small-box") for _ in range(8)], style={"display": "flex", "flexWrap": "wrap"})
            ], style={"display": "flex", "marginTop": "10px"})
        ], className="bottom-row")
    ], className="dynamic-container")
])

if __name__ == "__main__":
    # We do not use app.run() for Streamlit Cloud.
    pass
