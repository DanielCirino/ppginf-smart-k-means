import base64
import io

import dash
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
        [Output('upload-details', 'children'),
         Output('dataset-info', 'children'),
         Output('dataset-action', 'children')],
        [Input('upload-data', 'contents')],
        [State('upload-data', 'filename')]
    )
    def update_output(contents, filename):
        if contents is None:
            return dash.no_update, dash.no_update, dash.no_update

        df = process_upload(contents, filename)
        num_lines, num_columns = df.shape
        columns_types = zip(df.columns, df.dtypes)

        file_datails = f"""
        O arquivo '{filename}' possui {num_lines} registros e {num_columns} colunas.
        Os detalhes dos campos do arquivo podem ser observados ao lado."""

        # Retorna o nome do arquivo e a quantidade de linhas
        dataset_info = [
            html.P(className="card-text",
                   children="Estes são os atributos presentes no arquivo com seus respectivos tipos."),
            html.Ul(
                className="list-group",
                children=[
                    html.Li(
                        className="list-group-item list-group-item-dark",
                        children=f"{i + 1}. '{col[0]}' [{col[1]}]")
                    for i, col in enumerate(columns_types)]
            )]
        dataset_actions = html.A(
            id="btn-process-dataset",
            className="btn btn-primary mt-3",
            href="#section-result",
            children="Continuar",
            n_clicks=0)

        return file_datails, dataset_info, dataset_actions

    # Callback para voltar e carregar um novo arquivo ou prosseguir com o arquivo carregado
    @app.callback(
        Output('section-result-content', 'children'),
        [Input('btn-process-dataset', 'n_clicks')]
    )
    def continue_with_file(n_clicks):
        if n_clicks is None or n_clicks == 0:
            return dash.no_update

        # Adicione a lógica aqui para prosseguir com o arquivo carregado
        return f"Clique realizado {n_clicks} vezes..."

