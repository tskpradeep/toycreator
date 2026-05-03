import dash
from dash import html
import dash_resizable_panels as drp
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server 

# Visual styles
box_style = {"border": "2px solid black", "height": "100%", "width": "100%", "padding": "10px", "backgroundColor": "white"}
btn_small = {"width": "35px", "height": "35px", "border": "1px solid black", "margin": "2px", "display": "inline-block"}

app.layout = html.Div([
    drp.PanelGroup(
        id="main-v-group",
        direction="vertical",
        children=[
            # TOP SECTION
            drp.Panel(
                id="top-section",
                defaultSize=70,
                children=drp.PanelGroup(
                    direction="horizontal",
                    children=[
                        # Visual Display
                        drp.Panel(children=html.Div("visual displays dynamic between coding and screen/CAD designs", style=box_style), id="cad-view", defaultSize=60),
                        
                        # RED LINE
                        drp.PanelResizeHandle(html.Div(style={"width": "5px", "backgroundColor": "red", "cursor": "col-resize"})),
                        
                        # AI SIDEBAR
                        drp.Panel(
                            id="ai-sidebar",
                            defaultSize=30,
                            children=drp.PanelGroup(
                                direction="vertical",
                                children=[
                                    drp.Panel(children=html.Div("AI TEXT REPLYING WINDOW", style=box_style), defaultSize=50),
                                    # GREEN LINE
                                    drp.PanelResizeHandle(html.Div(style={"height": "5px", "backgroundColor": "green", "cursor": "row-resize"})),
                                    drp.Panel(children=html.Div("USER PROMPTING", style=box_style), defaultSize=50),
                                ]
                            )
                        ),
                        
                        # FAR RIGHT BUTTONS
                        drp.Panel(
                            children=html.Div([html.Div(style=btn_small) for _ in range(15)], style={"padding": "5px"}),
                            defaultSize=10
                        ),
                    ]
                )
            ),
            
            # GREEN LINE (Main Horizontal)
            drp.PanelResizeHandle(html.Div(style={"height": "5px", "backgroundColor": "green", "cursor": "row-resize"})),
            
            # BOTTOM SECTION
            drp.Panel(
                id="bottom-section",
                defaultSize=30,
                children=html.Div([
                    html.Div("command prompt / system programming / project", style=box_style),
                    html.Div([
                        html.Div("small indicators", style={"border": "1px solid green", "flex": "1", "padding": "5px"}),
                        html.Div("buttons for controlling", style={"border": "1px solid blue", "flex": "3", "padding": "5px"}),
                        html.Div([html.Div(style=btn_small) for _ in range(8)], style={"flex": "1", "border": "1px solid black"})
                    ], style={"display": "flex", "height": "50px", "marginTop": "5px"})
                ])
            ),
        ],
        style={"height": "100vh"}
    )
], style={"height": "100vh", "overflow": "hidden", "margin": "0"})

if __name__ == "__main__":
    app.run_server(debug=True)
