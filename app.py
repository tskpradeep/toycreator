import dash
from dash import html
import dash_resizable_panels as drp
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server 

# Visual styles to match your image_0d35a5.png
box_style = {"border": "2px solid black", "height": "100%", "width": "100%", "padding": "10px", "backgroundColor": "white", "overflow": "hidden"}
btn_small = {"width": "30px", "height": "30px", "border": "1px solid black", "margin": "2px", "display": "inline-block", "backgroundColor": "#f0f0f0"}

app.layout = html.Div([
    drp.PanelGroup(
        direction="vertical",
        children=[
            # TOP SECTION (Visuals + AI + Buttons)
            drp.Panel(
                defaultSize=70,
                children=drp.PanelGroup(
                    direction="horizontal",
                    children=[
                        # 1. Main CAD/Code Window
                        drp.Panel(
                            defaultSize=60,
                            children=html.Div("visual displays dynamic between coding and screen/CAD designs", style=box_style)
                        ),
                        
                        # RED SEPARATOR
                        drp.PanelResizeHandle(html.Div(style={"width": "5px", "backgroundColor": "red", "cursor": "col-resize"})),
                        
                        # 2. AI Sidebar (Vertical split)
                        drp.Panel(
                            defaultSize=30,
                            children=drp.PanelGroup(
                                direction="vertical",
                                children=[
                                    drp.Panel(defaultSize=50, children=html.Div("AI TEXT REPLYING WINDOW", style=box_style)),
                                    # GREEN SEPARATOR
                                    drp.PanelResizeHandle(html.Div(style={"height": "5px", "backgroundColor": "green", "cursor": "row-resize"})),
                                    drp.Panel(defaultSize=50, children=html.Div("USER PROMPTING", style=box_style)),
                                ]
                            )
                        ),
                        
                        # 3. Far Right Button Strip
                        drp.Panel(
                            defaultSize=10,
                            children=html.Div([html.Div(style=btn_small) for _ in range(16)], style={"padding": "5px", "textAlign": "center"})
                        ),
                    ]
                )
            ),
            
            # MAIN GREEN SEPARATOR
            drp.PanelResizeHandle(html.Div(style={"height": "5px", "backgroundColor": "green", "cursor": "row-resize"})),
            
            # BOTTOM SECTION (Command & Controls)
            drp.Panel(
                defaultSize=30,
                children=html.Div([
                    html.Div("command prompt / system programming / project", style=box_style),
                    html.Div([
                        html.Div("indicators", style={"border": "1px solid green", "flex": "1", "margin": "2px", "padding": "5px"}),
                        html.Div("controls", style={"border": "1px solid blue", "flex": "3", "margin": "2px", "padding": "5px"}),
                        html.Div([html.Div(style=btn_small) for _ in range(10)], style={"flex": "1.5", "border": "1px solid black", "margin": "2px"})
                    ], style={"display": "flex", "height": "60px", "marginTop": "5px"})
                ], style={"height": "100%", "padding": "5px"})
            ),
        ],
        style={"height": "100vh"}
    )
], style={"height": "100vh", "margin": "0", "overflow": "hidden"})

if __name__ == "__main__":
    app.run_server(debug=True)
