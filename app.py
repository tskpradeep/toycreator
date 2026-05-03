import dash
from dash import html, dcc
import dash_resizable_panels as drp
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Styling for the buttons and placeholders
box_style = {"border": "1px solid black", "height": "100%", "width": "100%", "padding": "10px"}
sidebar_btn_style = {"width": "30px", "height": "30px", "border": "1px solid black", "margin": "2px"}

app.layout = html.Div([
    # MAIN HORIZONTAL SPLIT (Top Area vs Bottom Console/Buttons)
    drp.PanelGroup(
        direction="vertical",
        children=[
            # TOP SECTION (Visual Display + AI Sidebar)
            drp.Panel(
                drp.PanelGroup(
                    direction="horizontal",
                    children=[
                        # Visual Display / CAD Window
                        drp.Panel(
                            html.Div("Visual Displays: Coding & CAD", style=box_style),
                            defaultSize=70
                        ),
                        # RED VERTICAL SEPARATOR
                        drp.PanelResizeHandle(html.Div(style={"width": "5px", "backgroundColor": "red", "cursor": "col-resize"})),
                        # AI WINDOWS
                        drp.Panel(
                            drp.PanelGroup(
                                direction="vertical",
                                children=[
                                    drp.Panel(html.Div("AI Text Replying", style=box_style), defaultSize=50),
                                    # GREEN HORIZONTAL SEPARATOR
                                    drp.PanelResizeHandle(html.Div(style={"height": "5px", "backgroundColor": "green", "cursor": "row-resize"})),
                                    drp.Panel(html.Div("User Prompting", style=box_style), defaultSize=50),
                                ]
                            ),
                            defaultSize=25
                        ),
                        # FAR RIGHT BUTTON COLUMN
                        drp.Panel(
                            html.Div([html.Div(style=sidebar_btn_style) for _ in range(12)], style={"padding": "5px"}),
                            defaultSize=5
                        ),
                    ]
                ),
                defaultSize=70
            ),
            
            # GREEN HORIZONTAL SEPARATOR
            drp.PanelResizeHandle(html.Div(style={"height": "5px", "backgroundColor": "green", "cursor": "row-resize"})),
            
            # BOTTOM SECTION (Command Prompt & System Buttons)
            drp.Panel(
                html.Div([
                    html.Div("Command Prompt / System Programming", style=box_style),
                    html.Div([
                        html.Div("Small Indicators", style={"border": "1px solid black", "width": "20%", "display": "inline-block"}),
                        html.Div("Control Buttons Area", style={"border": "1px solid black", "width": "60%", "display": "inline-block"}),
                        html.Div("Grid Buttons", style={"border": "1px solid black", "width": "20%", "display": "inline-block"}),
                    ], style={"display": "flex", "height": "40%"})
                ]),
                defaultSize=30
            ),
        ],
        style={"height": "100vh"} # Full Screen
    )
], style={"height": "100vh", "margin": "0", "overflow": "hidden"})

if __name__ == "__main__":
    app.run_server(debug=True)
