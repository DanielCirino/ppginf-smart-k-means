from dash import html, dcc, dash_table

sidebar = html.Div(
    [
        html.H5("Smart K-Means"),
        html.Br(),
        html.Div(className="container-fluid", children=[
            html.Div(
                className="row",
                children=[
                    html.Div(
                        className="col-sm-12",
                        children=[
                            html.Div(
                                className="card text-white bg-dark mb-3",
                                children=[
                                    # html.Img(className="card-img-top", src="./assets/upload_icon.png", width="24px"),
                                    html.Div(className="card-body", children=[
                                        html.H5(className="card-title", children="Fazer upload"),
                                        html.P(className="card-text",
                                               children=[])
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
                        ]
                    )
                ]
            ),
            html.Div(
                className="row",
                children=[
                    html.Div(
                        className="col-md-12",
                        children=[
                            html.Div(
                                className="card text-white bg-info mb-3",
                                children=[

                                    html.Div(className="card-body", children=[
                                        html.H5(className="card-title", children="Detalhes do arquivo"),
                                        html.P(
                                            id="upload-details",
                                            className="card-text",
                                            children="Selecione um arquivo para ver os detalhes")
                                    ]),

                                ])
                        ]
                    )
                ]
            ),
            html.Div(
                className="row",
                children=[
                    html.Div(
                        className="col-md-12",
                        children=[
                            html.Div(className="card text-white bg-dark mb-3", children=[
                                # html.Div(className="card-header", children="Detalhes do Arquivo"),
                                html.Div(
                                    className="card-body",
                                    children=[
                                        html.H5(className="card-title", children="Campos do dataset"),
                                        html.Div(
                                            id="dataset-info",
                                            className="h-25",
                                            children="Selecione um arquivo para ver os detalhes do dastaset."),
                                        html.Div(
                                            id="dataset-action",
                                            children="...")

                                    ]),

                            ])
                        ]
                    )
                ]
            )
        ])

    ], style={"height": "100vh"})

section_result = html.Section(
    id="section-result",
    children=[
        html.H3(className="mt-3", children="Resultado análise agrupamento"),
        html.Hr(className="mt-3"),
        html.Div(
            id="section-result-content",
            className="container-fluid mt-3",
            children=[
                html.Div(className="row", children=[
                    html.Div(className="col-md-3", children=[
                        html.Div(
                            className="card text-white bg-primary",
                            children=[

                                html.Div(className="card-body", children=[
                                    html.H5(className="card-title", children="Qtd. Ótima"),
                                    html.H5(id="qtd-otima-grupos", className="display-6 p-2", children=0)
                                ]),
                            ])

                    ]),
                    html.Div(className="col-md-3", children=[

                        html.Div(
                            className="card text-white bg-dark",
                            children=[
                                html.Div(className="card-body", children=[
                                    html.H5(className="card-title", children="Silhueta Média"),
                                    html.H1(id="vlr-silhueta-media", className="display-6 p-2", children="0.0000")
                                ]),

                            ])

                    ]),
                    html.Div(className="col-md-3", children=[
                        html.Div(
                            className="card text-white bg-dark",
                            children=[
                                html.Div(className="card-body", children=[
                                    html.H5(className="card-title", children="Iterações"),
                                    html.H1(id="qtd-iteracoes", className="display-6 p-2", children=0)
                                ]),

                            ])
                    ]),

                    html.Div(className="col-md-3", children=[
                        html.Div(
                            className="card text-white bg-dark",
                            children=[

                                html.Div(className="card-body", children=[
                                    html.H5(className="card-title", children="Variáveis Restantes"),
                                    html.H1(id="qtd-variaveis-restantes", className="display-6 p-2", children=0)
                                ]),

                            ])

                    ])
                ]),

                html.Div(className="row mt-3", children=[
                    html.Div(className="col-md-12", children=[
                        html.Div(
                            className="card text-white bg-dark",
                            children=[
                                html.Div(className="card-header", children="Silhueta melhor arranjo"),
                                html.Div(className="card-body p-0", children=[
                                    dcc.Graph(id="silhouette-graph")
                                ]),

                            ]
                        )
                    ]),

                ]),

                html.Div(className="row mt-3", children=[
                    html.Div(className="col-md-6", children=[

                        html.Div(
                            className="card text-white bg-dark",
                            children=[
                                html.Div(className="card-header", children="Comparação dos grupos"),
                                html.Div(className="card-body p-0", children=[
                                    dcc.Graph(id="comparison-graph")
                                ]),

                            ]
                        )

                    ]),

                    html.Div(className="col-md-6", children=[
                        html.Div(
                            className="card text-white bg-dark",
                            children=[
                                html.Div(
                                    id="container-detalhes-arranjo",
                                    className="card-header",
                                    children="Detalhes do arranjo"),
                                html.Div(className="card-body p-0", children=[

                                    dcc.Graph(id="cluster-graph")
                                ]),

                            ]
                        )
                    ]),
                ]),

                html.Div(className="row mt-3", children=[
                    html.Div(className="col-md-8", children=[
                        html.Div(
                            className="card text-white bg-dark",
                            children=[
                                html.Div(className="card-header", children="Entropia das variáveis"),
                                html.Div(className="card-body p-0", children=[
                                    dcc.Graph(id="entropy-graph")
                                ]),

                            ]
                        )

                    ]),

                    html.Div(className="col-md-4", children=[
                        html.Div(
                            className="card text-white bg-dark",
                            children=[
                                html.Div(
                                    className="card-header",
                                    children="Detalhes das iterações"),
                                html.Div(
                                    id="iterate-summary",
                                    className="card-body",
                                    children="Informações sobre as iterações realizadas no dataset."),
                            ])

                    ])

                ]),

            ])
    ], style={"min-height": "100vh"})  # Definindo altura para ocupar o tamanho da tela

conteudo = html.Div(
    className="container-fluid m-3",
    children=[
        section_result,
        html.Hr(),
        # Seção resultados
        html.Div([
            html.H2("Resultado da classificação", id="section-3", className="display-5"),

            html.Div(className="row mt-3", children=[
                html.H4(
                    children=[
                        "Atribuição dos grupos",
                        html.Small(html.Button(
                            id="btn-download-resultado",
                            className="btn btn-outline-primary btn-large m-3",
                            children="Download")),
                        dcc.Download(id="down-resultados")
                    ]
                ),
                html.Div(id="tabela-classificacao", className="col-md-12",
                         children=[])
            ]),

            html.Div(className="row mt-3", children=[
                html.H4(
                    children=[
                        "Dashboard variáveis x Grupos",
                        html.Small(html.Button(
                            id="btn-download-anova",
                            className="btn btn-outline-primary btn-large m-3",
                            children="Download")),
                        dcc.Download(id="down-anova")
                    ]
                ),
                html.Div(id="tabela-variaveis-grupo", className="col-md-12",
                         children=[

                         ])
            ]),

        ], style={"min-height": "100vh"}),
    ])


def configurar_layout(app):
    app.layout = html.Div(
        className="container-fluid",
        children=[
            html.Div(className="row", children=[
                # Barra lateral com tamanho de 3 colunas
                html.Div(
                    className="col-md-3 sticky-top",
                    children=[sidebar],
                    style={"background-color": "#171717",
                           "color": "#ffffff",
                           "padding": "20px", "min-height": "100vh"}
                ),
                # Conteúdo principal com tamanho de 9 colunas
                html.Div(
                    className="col-md-9",
                    children=[
                        conteudo],
                    style={"color": "#ffffff", }
                )
            ]),
            dcc.Store(id='data-store'),
            dcc.Store(id='conteudo-arquivo'),
            dcc.Store(id='dataset-original'),
            dcc.Store(id='dataset-resultados'),
            dcc.Store(id='dataset-melhor-arranjo'),
            dcc.Store(id='dataset-iteracoes'),
            dcc.Store(id='dataset-final'),
            dcc.Store(id='dataset-anova')

        ], style={"background-color": "#212121", "min-height": "100vh"}
    )
