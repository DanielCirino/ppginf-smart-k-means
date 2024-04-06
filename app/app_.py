import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate

# Inicialização do aplicativo Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="/")),
            dbc.NavItem(dbc.NavLink("Resultados", href="/page-1")),
            dbc.NavItem(dbc.NavLink("Sobre", href="/page-2")),
        ],
        brand="Meu Aplicativo",
        brand_href="#",
        color="primary",
        dark=True,
    ),
    dbc.Container([
        html.Div(id='page-content'),  # Adicionando o elemento page-content

    ]), html.Footer(
        "Este é o rodapé do meu aplicativo.",
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


# Callback para processar o upload de arquivos
@app.callback(
    Output('output-data-upload', 'children'),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename'),
     State('upload-data', 'last_modified')]
)
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is None:
        raise PreventUpdate

    children = [
        html.H5(list_of_names),
        html.P(f"<code>{list_of_contents}</code>")
    ]

    return children


# Callback para atualizar o conteúdo da página com base na URL
@app.callback(
    Output('page-content', 'children'),  # Adicionando a saída do callback ao elemento page-content
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/page-1':
        return html.H1('Conteúdo da Página 1')
    elif pathname == '/page-2':
        return html.H1('Conteúdo da Página 2')
    else:
        return [html.H2("Página Inicial"),
                html.P("Faça o upload de um arquivo:"),
                dcc.Upload(
                    id='upload-data',
                    children=html.Div([
                        'Arraste e solte ou ',
                        html.A('selecione um arquivo')
                    ]),
                    style={
                        'width': '100%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px'
                    },
                    # Permite o upload de múltiplos arquivos
                    multiple=False
                ),
                html.Div(id='output-data-upload'),
                ]


# Executar o aplicativo
if __name__ == '__main__':
    app.run_server(debug=True)
