import base64
import io

import pandas as pd
from dash import Input, Output, State, html

from layout import section_upload


# Função para simular o processamento do arquivo
def process_upload(contents, filename):
    if contents is not None:
        # Lê o conteúdo do arquivo como um DataFrame do Pandas
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string).decode('utf-8')

        # Lê o conteúdo do arquivo como um DataFrame do Pandas
        df = pd.read_csv(io.StringIO(decoded), sep=";")
        return df


def configurar_callbacks(app):
    # Callback para carregar e exibir informações do arquivo
    @app.callback(
        Output('upload-content', 'children'),
        [Input('upload-data', 'contents')],
        [State('upload-data', 'filename')]
    )
    def update_output(contents, filename):
        if contents is None:
            return section_upload

        if contents is not None:
            df = process_upload(contents, filename)
            num_lines, num_columns = df.shape

            # Retorna o nome do arquivo e a quantidade de linhas
            return html.Div([
                html.Div(className="jumbotron", children=[
                    html.H1("Detalhes Arquivo", className="display-4"),
                    html.P(
                        "Confira abaixo os detalhes do arquivo carregado.",
                        className="lead"),
                    html.Hr(className="my-4"),
                    html.Div(
                        [html.H5(f'Nome do Arquivo: {filename}'),
                         html.H6(f'Quantidade de Linhas: {num_lines}'),
                         html.Hr(className="my-4"),
                         html.Table(className="table table-sm table-dark table-striped", children=[
                             html.Thead(children=[html.Tr([html.Th("Variável"), html.Th("Excluir")])]),
                             html.Tbody(
                                 children=
                                 [html.Tr(html.Td(col)) for col in df.columns]

                             )
                         ])
                         ]
                    ),

                    html.Div(
                        className="btn-group",
                        children=[
                            html.A("Voltar", className="btn btn-light btn-large mr-2", href="#"),
                            html.A("Avançar", className="btn btn-primary btn-large ml-3", href="#")]
                    ),

                ]),
            ])
        else:
            return html.Div()
