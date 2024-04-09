import base64
import io

import dash
import pandas as pd
from dash import Input, Output, State, html, dash_table

from core.smart_k_means import obter_avaliacao_de_agrupamento
from layout import section_upload
import plotly.express as px


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
        [
            Output('data-store', 'data'),
            Output('upload-details', 'children'),
            Output('dataset-info', 'children'),
            Output('dataset-action', 'children')

        ],
        [Input('upload-data', 'contents')],
        [State('upload-data', 'filename')]
    )
    def update_output(contents, filename):
        if contents is None:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update

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
        data_json = df.to_json(date_format='iso', orient='split')
        return data_json, file_datails, dataset_info, dataset_actions

    # Callback para voltar e carregar um novo arquivo ou prosseguir com o arquivo carregado
    @app.callback([Output("entropy-graph", "figure")],
                  Output('iterate-summary', 'children'),
                  [Input('btn-process-dataset', 'n_clicks'),
                   Input('data-store', 'data')]
                  )
    def continue_with_file(n_clicks, data):
        if n_clicks is None or n_clicks == 0:
            return dash.no_update, dash.no_update

        df = pd.read_json(io.StringIO(data), orient='split')
        data = df.drop(["Census tract"], axis=1)
        df_entropy, best_cluster, iterate_summary, iterates = obter_avaliacao_de_agrupamento(data)

        # Gráfico da entropia
        fig_entropy_graph = px.bar(df_entropy,
                                   x="entropia",
                                   y="variavel",
                                   orientation='h',
                                   template="plotly_dark",
                                   color="entropia",
                                   title='Gráfico de Barras Horizontais',
                                   text="entropia")

        fig_entropy_graph.update_traces(texttemplate='%{text:.2s}', textposition='outside')

        df_iterate_summary = pd.DataFrame(iterate_summary)

        table_iterate_summary = dash_table.DataTable(
            data=df_iterate_summary.to_dict("records"),
            columns=[{"name": i, "id": i} for i in df_iterate_summary.columns],
            style_header={
                'backgroundColor': 'rgb(30, 30, 30)',
                'color': 'white'
            },
            style_data={
                'backgroundColor': 'rgb(50, 50, 50)',
                'color': 'white'
            },
        )

        return fig_entropy_graph, table_iterate_summary
