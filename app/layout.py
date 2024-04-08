import dash_bootstrap_components as dbc
from dash import html, dcc

sidebar = html.Div([
    html.H5("Smart K-Means"),
    html.Br(),
    # Links para navegação

    html.Ul(
        className="nav flex-column",
        children=[
            html.Li(
                className="nav-item",
                children=[
                    html.A(
                        id="link-section-upload",
                        className="nav-link active",
                        href="#section-upload",
                        children="Upload"
                    ),
                    html.A(
                        id="link-section-1",
                        className="nav-link",
                        href="#section-1",
                        children="Detalhes"
                    ),

                    html.A(
                        id="link-section-2",
                        className="nav-link ",
                        href="#section-2",
                        children="Seção 2"
                    ),
                    html.A(
                        id="link-section-3",
                        className="nav-link",
                        href="#section-3",
                        children="Seção 3"
                    )
                ])
        ]),

], style={"position": "fixed", "height": "100vh"})

section_upload = html.Section(
    id="section-upload",
    children=html.Div(id="upload-content", children=[
        html.Div(html.Img(src="./assets/upload_icon.png", width="128 px")),
        html.P(className="lead mt-3", children=["Qual é a melhor classificação para os seus dados?"]),
        html.P(className="", children=["Faça um upload e vamos descobrir?"]),
        html.Div(
            className="container, text-center",
            children=[
                dcc.Upload(
                    id='upload-data',
                    children=html.Div([
                        'Arraste para cá ou ',
                        html.A('clique para selecionar um arquivo')
                    ]),
                    style={
                        'width': '100%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '10px',
                        'textAlign': 'center',
                        'margin': '50px 10px 10px 10px',
                        'font-family': 'Courier New'
                    },
                    # Permite o upload de múltiplos arquivos
                    multiple=False
                ),
            ]),
        html.Div(
            id='output-data-upload',
            className="container mt-3",
            children=[dbc.Progress(value=0, id="progress_bar"), ]),
    ]), style={"min-height": "100vh"}
)

conteudo = html.Div(
    className="container mt-3 ml-3 mr-3 ",
    children=[
        section_upload,
        html.Section(id="section-1", children=[
            html.Div(
                id="detalhes-arquivo",
                children=[
                    html.Div(className="jumbotron", children=[
                        html.H1("Hello word", className="display-4"),
                        html.P(
                            "This is a simple hero unit, a simple jumbotron-style component for calling extra attention to featured content or information.",
                            className="lead"),
                        html.Hr(className="my-4"),
                        html.P(
                            "It uses utility classes for typography and spacing to space content out within the larger container."),
                        html.A("Voltar", className="btn btn-light btn-large", href="#"),
                        html.A("Avançar", className="btn btn-primary btn-large", href="#")
                    ])
                ]),
        ], style={"min-height": "100vh"}),  # Definindo altura para ocupar o tamanho da tela
        html.Hr(),
        # Seção 2
        html.Div([
            html.H2("Seção 2", id="section-2", className="display-5"),
            html.P("Conteúdo da seção 2..."),
        ], style={"min-height": "100vh"}),  # Definindo altura para ocupar o tamanho da tela
        html.Hr(),
        # Seção 3
        html.Div([
            html.H2("Seção 3", id="section-3", className="display-5"),
            html.P("Conteúdo da seção 3..."),
        ], style={"min-height": "100vh"}),
    ])


def configurar_layout(app):
    app.layout = html.Div([
        dbc.Row([
            # Barra lateral com tamanho de 2 colunas
            dbc.Col(
                sidebar,
                width=2,
                style={"background-color": "#171717",
                       "color": "#ffffff",
                       "padding": "20px", "min-height": "100vh"}
            ),
            # Conteúdo principal com tamanho de 10 colunas
            dbc.Col(
                conteudo,
                width=10,
                style={"color": "#ffffff", }
            )
        ]),
    ], className="container-fluid", style={"background-color": "#212121", "min-height": "100vh"}
    )
