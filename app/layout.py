import dash_bootstrap_components as dbc
from dash import dcc, html

# Layout
layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="/")),
            dbc.NavItem(dbc.NavLink("Resultados", href="/page-1")),
            dbc.NavItem(dbc.NavLink("Sobre", href="/page-2")),
        ],
        brand="Smart K-means",
        brand_href="#",
        color="primary",
        dark=True,
    ),
    dbc.Container([
        html.Div(id='page-content',style={"padding-top":"5px"}),  # Adicionando o elemento page-content

    ]), html.Footer(
        "© 2024 Daniel Cirino. Todos os direitos reservados.",
        style={
            "background-color": "#343a40",
            "color": "#ffffff",
            "padding": "20px",
            "position": "fixed",
            "bottom": "0",
            "width": "100%"
        }
    )

], style={"background-color": "#f8f9fa", "min-height": "100vh"})
