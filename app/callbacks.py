import base64
import io

import dash
import pandas as pd
from dash import Input, Output, State, html, dash_table

from core.smart_k_means import obter_avaliacao_de_agrupamento

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

        file_datails = html.Ul(
                className="list-group list-group-flush",
                children=[
                    html.Li(
                        className="list-group-item bg-info text-light",
                        children=f"Total de registros: {num_lines}"),
                    html.Li(
                        className="list-group-item bg-info text-light",
                        children=f"Qtd. Colunas: {num_columns}"),
                ]
            )


        # Retorna o nome do arquivo e a quantidade de linhas
        dataset_info = html.Div([
            html.P(className="card-text",
                   children="Estes são os atributos e seus respectivos tipos."),
            html.Ul(
                className="list-group list-group-flush",
                children=[
                    html.Li(
                        className="list-group-item bg-dark text-light",
                        children=f"{i + 1}. '{col[0]}' [{col[1]}]")
                    for i, col in enumerate(columns_types)]
            )],style={"height":"300px","overflow-y":"auto"})
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
        fig_entropy_graph = gerar_grafico_entropia(df_entropy)

        # tabela de iteracoes
        df_iterate_summary = pd.DataFrame(iterate_summary)
        table_iterate_summary = gerar_tabela_iteracoes(df_iterate_summary)

        return fig_entropy_graph, table_iterate_summary


def gerar_grafico_entropia(df):
    # Gráfico da entropia
    fig = px.bar(df,
                 x="entropia",
                 y="variavel",
                 orientation='h',
                 template="plotly_dark",
                 color="entropia",
                 title='Gráfico de Barras Horizontais',
                 text="entropia")

    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    return fig


def gerar_tabela_iteracoes(df):
    lista_iteracoes = html.Div(className="list-group ", children=[
        html.Div(className="list-group-item list-group-item-action bg-dark text-light", children=[
            html.Div(className="d-flex w-100 justify-content-between", children=[
                html.H5(className="mb-1", children=f"Iteração {row['iteracao']}"),
                html.Small(children="")
            ]),
            html.P(className="mb-1", children=f"Excluída a {row['variavel_excluida']}"),
            html.Small(children=f"{row['resultados_validos']} Resultados válidos")
        ]) for _, row in df.iterrows()
    ])

    return lista_iteracoes
