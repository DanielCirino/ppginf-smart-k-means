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
    children=[
        html.Div(
            id="detalhes-arquivo",
            children=[
                html.Div(className="row", children=[
                    html.Div(className="col-md-4 d-flex", children=[
                        html.Div(className="card text-white bg-dark mb-3", children=[
                            # html.Img(className="card-img-top", src="./assets/upload_icon.png", width="24px"),
                            html.Div(className="card-body", children=[
                                html.H5(className="card-title", children="Fazer upload"),
                                html.P(className="card-text",
                                       children="Qual a melhor classificação para os seus dados?"
                                                "Faça um upload dos seus dados e descubra ;)")
                            ]),
                            html.Div(className="card-body", children=[
                                html.Div(
                                    className="row",
                                    children=[
                                        html.Div(className="col-md-12", children=[
                                            dcc.Upload(
                                                id='upload-data',
                                                children=html.Div([
                                                    html.A(' Arraste ou clique para selecionar um arquivo')
                                                ]),
                                                style={
                                                    'width': '100%',
                                                    'borderWidth': '1px',
                                                    'borderStyle': 'dashed',
                                                    'borderRadius': '10px',
                                                    'textAlign': 'center',
                                                    'padding': '5px 5px 5px 5px',
                                                    'font-family': 'Courier New'
                                                },
                                                # Permite o upload de múltiplos arquivos
                                                multiple=False
                                            )
                                        ]),
                                    ])
                            ])
                        ])
                    ]),
                    html.Div(
                        className="col-md-4 d-flex",
                        children=[
                            html.Div(
                                className="card text-white bg-dark mb-3",
                                children=[

                                    html.Div(className="card-body", children=[
                                        html.H5(className="card-title", children="Detalhes do arquivo"),
                                        html.P(
                                            id="upload-details",
                                            className="card-text",
                                            children="Selecione um arquivo para ver os detalhes")
                                    ]),

                                ])
                        ]),
                    html.Div(className="col-md-4 d-flex", children=[
                        html.Div(className="card text-white bg-dark mb-3", children=[
                            # html.Div(className="card-header", children="Detalhes do Arquivo"),
                            html.Div(className="card-body", children=[
                                html.H5(className="card-title", children="Campos do dataset"),

                                html.Div(
                                    id="dataset-info",
                                    children="Selecione um arquivo para ver os detalhes do dastaset."),
                                html.Div(
                                    id="dataset-action",
                                    children="...")

                            ]),

                        ])
                    ])
                ])

            ]),
    ], style={"min-height": "100vh"}  # Definindo altura para ocupar o tamanho da tela
)

section_result = html.Section(
    id="section-result",
    children=[
        html.H3(className="mt-3", children="Resultado análise agrupamento"),
        html.Hr(className="mt-3"),
        html.Div(
            id="section-result-content",
            className="container mt-3",
            children=[
                html.P("Conteúdo da seção 2..."),
            ])
    ], style={"min-height": "100vh"})  # Definindo altura para ocupar o tamanho da tela

conteudo = html.Div(
    className="container mt-3 ml-3 mr-3 ",
    children=[
        section_upload,
        html.Br(),
        section_result,
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
