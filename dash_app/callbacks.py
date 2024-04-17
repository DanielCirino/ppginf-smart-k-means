import base64
import io
import json

import dash
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, State, html, dcc, dash_table
from plotly.subplots import make_subplots

from core.smart_k_means import obter_avaliacao_de_agrupamento


# Função para simular o processamento do arquivo
def processar_upload(contents, filename):
    if contents is not None:
        # Lê o conteúdo do arquivo como um DataFrame do Pandas
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string).decode('utf-8')

        # Lê o conteúdo do arquivo como um DataFrame do Pandas
        df = pd.read_csv(io.StringIO(decoded), sep=";")
        return df


def gerar_dropdown_resultados(resultados):
    arranjos = []

    for i, r in enumerate(resultados):
        arranjos.append({"value": i, "label": r["arranjo"]})

    return dcc.Dropdown(
        id="dropdown-resultado",
        className="form-control form-control-sm ",
        options=arranjos)


def configurar_callbacks(app):
    # Callback para carregar e exibir informações do arquivo
    @app.callback(
        [
            Output('conteudo-arquivo', 'data'),
            Output('dataset-original', 'data'),
            Output('upload-details', 'children'),
            Output('dataset-info', 'children'),
            Output('dataset-action', 'children')

        ],
        [Input('upload-data', 'contents')],
        [State('upload-data', 'filename')]
    )
    def processar_dados_arquivo(contents, filename):
        if contents is None:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update

        df = processar_upload(contents, filename)
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
            )], style={"height": "300px", "overflow-y": "auto"})

        dataset_actions = html.Form(children=[
            html.Hr(className="mt-3"),
            html.H6(className="", children="Qtd. Grupos"),
            html.Div(className="row mt-3", children=[
                html.Div(className="col", children=[
                    html.Label("Mín"),
                    dcc.Input(
                        id="in-qtd-min-grupos",
                        value=3,
                        className="form-control bg-dark text-white",
                        placeholder="Mín. Grupos",
                        type="number")
                ]),
                html.Label("Máx"),
                html.Div(
                    className="col", children=[
                        dcc.Input(
                            id="in-qtd-max-grupos",
                            value=7,
                            className="form-control bg-dark text-white",
                            placeholder="Max. Grupos", type="number")
                    ]),

                html.A(
                    id="btn-processar",
                    className="btn btn-primary mt-3",
                    href="#section-result",
                    children="Continuar",
                    n_clicks=0)

            ])
        ])

        data_json = df.to_json(date_format='iso', orient='split')
        return (contents,
                data_json,
                file_datails,
                dataset_info,
                dataset_actions)

    # Callback para voltar e carregar um novo arquivo ou prosseguir com o arquivo carregado
    @app.callback(
        [
            Output('qtd-otima-grupos', 'children'),
            Output('qtd-iteracoes', 'children'),
            Output('qtd-variaveis-restantes', 'children'),
            Output('vlr-silhueta-media', 'children'),
            Output('silhouette-graph', 'figure'),
            Output("container-detalhes-arranjo", "children"),
            Output("cluster-graph", "figure"),
            Output("comparison-graph", "figure"),
            Output("entropy-graph", "figure"),
            Output('iterate-summary', 'children'),
            Output('tabela-classificacao', 'children'),
            Output('tabela-variaveis-grupo', 'children'),
            Output('dataset-resultados', 'data'),
            Output('dataset-melhor-arranjo', 'data'),
            Output('dataset-iteracoes', 'data')
        ],
        [
            Input('btn-processar', 'n_clicks'),
            Input('in-qtd-min-grupos', 'value'),
            Input('in-qtd-max-grupos', 'value'),
            Input('dataset-original', 'data')],
        prevent_initial_call=True
    )
    def fazer_classificacao_dados(n_clicks, min_grupos, max_grupos, data):
        if n_clicks is None or n_clicks == 0:
            return dash.no_update, dash.no_update

        df = pd.read_json(io.StringIO(data), orient='split')
        dados = df.drop(df.columns[0], axis=1)

        # normalizar os dados
        for col in dados.columns:
            dados[col] = (dados[col] - dados[col].mean()) / (dados[col].std()).round(4)

        (df_entropia,
         melhor_cluster,
         sumario_iteracoes,
         iteracoes,
         variaveis_restantes,
         resultados,
         dados) = obter_avaliacao_de_agrupamento(dados.round(4), min_grupos, max_grupos)

        nome_melhor_cluster = melhor_cluster["arranjo"]
        silhueta_media = melhor_cluster["silhueta_media"]

        # Gráfico das silhuetas
        grafico_silhueta = gerar_grafico_silhueta(melhor_cluster)

        # Gráfico dos grupos
        grafico_agrupamento = gerar_grafico_agrupamento(melhor_cluster)

        # Dropdown dos resultados gerados
        dropdown_resultados = gerar_dropdown_resultados(resultados)

        # Gráfico de comparação de silhueta
        grafico_comparacao = gerar_grafico_comparacao(resultados)

        # Gráfico da entropia
        grafico_entropia = gerar_grafico_entropia(df_entropia)

        # tabela de iteracoes
        df_iteracoes = pd.DataFrame(sumario_iteracoes)
        tabela_iteracoes = gerar_tabela_colunas(df_iteracoes, df.columns)

        # tabela de resultados
        tabela_resultados = gerar_tabela_resultado(df,
                                                   melhor_cluster["rotulos"],
                                                   df_iteracoes["variavel_excluida"].values)
        # tabela de resultados
        tabela_variaveis_grupos = gerar_tabela_variaveis_grupo(df,
                                                               melhor_cluster["rotulos"],
                                                               df_iteracoes["variavel_excluida"].values)
        return (nome_melhor_cluster,
                iteracoes,
                len(variaveis_restantes),
                "{:.4f}".format(silhueta_media),
                grafico_silhueta,
                dropdown_resultados,
                grafico_agrupamento,
                grafico_comparacao,
                grafico_entropia,
                tabela_iteracoes,
                tabela_resultados,
                tabela_variaveis_grupos,
                resultados,
                melhor_cluster,
                df_iteracoes.to_json(date_format='iso', orient='split'))

    @app.callback(
        Output("cluster-graph", "figure", allow_duplicate=True),
        [
            Input('dropdown-resultado', 'value'),
            Input('dataset-resultados', 'data'),
        ],
        prevent_initial_call=True
    )
    def atualizar_grafico_grupo(value, data):
        resultado = data[value]
        return gerar_grafico_agrupamento(resultado)

    @app.callback(
        [Output("down-resultados", "data"),
         Output("dataset-final", "data")],
        [Input('btn-download-resultado', 'n_clicks'),
         Input('dataset-original', 'data'),
         Input('dataset-melhor-arranjo', 'data')
         ], prevent_initial_call=True,
    )
    def fazer_download_classificacao(n_clicks, dados_originais, dados_melhor_arranjo):
        if n_clicks <= 0:
            return None, None

        df_original = pd.read_json(io.StringIO(dados_originais), orient='split')
        df_classficacao = df_original.copy()
        primeira_coluna = df_classficacao.columns[0]
        df_classficacao[primeira_coluna] = df_classficacao[primeira_coluna].astype(str)
        df_classficacao["grupo"] = pd.Series(dados_melhor_arranjo["rotulos"])

        return (dcc.send_data_frame(df_classficacao.to_excel, "resultado_smart_k_means.xlsx", sheet_name="result"),
                df_classficacao.to_json(date_format='iso', orient='split'))

    @app.callback(
        [Output("down-anova", "data"),
         Output("dataset-anova", "data")],
        [Input('btn-download-anova', 'n_clicks'),
         Input('dataset-original', 'data'),
         Input('dataset-melhor-arranjo', 'data'),
         Input('dataset-iteracoes', 'data')
         ], prevent_initial_call=True
    )
    def fazer_download_anova(n_clicks, dados_originais, dados_melhor_arranjo,dados_iteracoes):
        if n_clicks <= 0:
            return None, None


        df_original = pd.read_json(io.StringIO(dados_originais), orient='split')
        df_classficacao = df_original.copy()
        primeira_coluna = df_classficacao.columns[0]
        df_classficacao[primeira_coluna] = df_classficacao[primeira_coluna].astype(str)

        df_classficacao["grupo"] = pd.Series(dados_melhor_arranjo["rotulos"])

        df_iteracoes=pd.read_json(io.StringIO(dados_iteracoes), orient='split')

        colunas_excluidas = df_iteracoes["variavel_excluida"].values
        novo_df_arquivo = df_classficacao.drop(colunas_excluidas, axis=1)

        cols = novo_df_arquivo.columns
        dados_anova = []

        for grupo in novo_df_arquivo["grupo"].unique():
            anova = novo_df_arquivo[novo_df_arquivo["grupo"] == grupo].describe()
            dados_anova.append(np.append(anova.iloc[[1]].values[0][:-1], f"G{grupo}"))

        df_variaveis = pd.DataFrame(dados_anova, columns=cols[1::])
        return (dcc.send_data_frame(df_variaveis.to_excel, "anova_smart_k_means.xlsx", sheet_name="result"),
                df_variaveis.to_json(date_format='iso', orient='split'))


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


def gerar_tabela_colunas(df_iteracoes, lista_colunas_df):
    lista_colunas_excluidas = df_iteracoes["variavel_excluida"].values

    itens_lista = []

    for col in lista_colunas_df[1::]:
        nome_variavel = f"Variável {col}"
        resultado_processamento = "Mantida"
        resultados_validos = ""
        cor_item = "text-light"

        coluna_excluida = col in lista_colunas_excluidas
        if coluna_excluida:
            iteracao = df_iteracoes.loc[df_iteracoes["variavel_excluida"] == col]
            num_iteracao = iteracao['iteracao'].values[0]
            entropia = iteracao['entropia'].values[0]
            resultados_validos = iteracao['resultados_validos'].values[0]

            resultado_processamento = (f"Deconsiderada na iteração: {num_iteracao}"
                                       f" Entropia={entropia:.4f}")
            resultados_validos = f"{resultados_validos} Resultados válidos"
            cor_item = "text-danger"

        itens_lista.append(
            html.Div(className=f"list-group-item list-group-item-action {cor_item} bg-dark",
                     children=[
                         html.Div(className="d-flex w-100 justify-content-between", children=[
                             html.H6(className="mb-1", children=nome_variavel),
                             html.Small(children="")
                         ]),
                         html.P(
                             className="mb-1",
                             children=resultado_processamento),
                         html.Small(children=resultados_validos)
                     ])
        )

    detalhes_colunas = html.Div(
        className="list-group ",
        children=itens_lista,
        style={"height": "500px", "overflow-y": "auto"})

    return detalhes_colunas


def gerar_grafico_silhueta(cluster):
    dados = zip(
        cluster["rotulos"],
        cluster["silhuetas"])
    df = pd.DataFrame(dados, columns=["rotulos", "silhuetas"])

    rotulos = list(df.groupby(["rotulos"]).count().index)

    fig = make_subplots(rows=1, cols=len(rotulos), shared_yaxes=True)

    for r in rotulos:
        fig.add_trace(
            go.Bar(y=df["silhuetas"][df["rotulos"] == r], name=f"Cluster {r}"), 1, r + 1
        )

    fig.add_hline(y=cluster["silhueta_media"],
                  line_width=1,
                  line_dash="dash",
                  line_color="yellow",
                  annotation_text="Silhueta média")
    return fig


def gerar_grafico_agrupamento(cluster):
    resumo = pd.DataFrame(cluster["resumo_classificacao"])
    resumo["nome_grupo"] = "G" + (resumo["grupo"]).astype(str)
    fig = px.treemap(resumo, path=["nome_grupo"], values="qtd")
    return fig


def gerar_grafico_comparacao(resultados):
    silhuetas = [r["silhueta_media"] for r in resultados]
    nomes_arranjo = [r["arranjo"] for r in resultados]

    df = pd.DataFrame({'arranjo': nomes_arranjo, 'silhueta_media': silhuetas})

    fig = px.bar(df, x="arranjo", y="silhueta_media", color="arranjo")

    fig.add_hline(y=df["silhueta_media"].mean(),
                  line_width=2,
                  line_dash="dash",
                  line_color="cyan",
                  annotation_text="Silhueta média geral")

    fig.add_hline(y=0.5,
                  line_width=2,
                  line_dash="dash",
                  line_color="yellow",
                  annotation_text="Limiar de aceitação")

    return fig


def gerar_tabela_resultado(df_original, rotulos, colunas_excluidas):
    df_classificacao = df_original.copy()
    df_classificacao.drop(colunas_excluidas, axis=1)
    df_classificacao["Grupo"] = pd.Series(rotulos)

    data_table = dash_table.DataTable(
        df_classificacao.to_dict('records'),
        [{"name": col, "id": col} for col in df_classificacao.columns],
        page_size=10,
        style_table={'overflowX': 'auto'},
        style_header={
            'backgroundColor': '#343a40',
            'fontWeight': 'bold'
        },
        style_data={
            'color': 'white',
            'backgroundColor': '#343a40'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgba(255, 255, 255, .05)',
            }
        ],
    )
    return data_table


def gerar_tabela_variaveis_grupo(df_original, rotulos, colunas_excluidas):
    df_classificacao = df_original.copy()
    df_classificacao.drop(colunas_excluidas, axis=1, inplace=True)
    df_classificacao["Grupo"] = pd.Series(rotulos)

    variaveis = df_classificacao.columns[1:-1]
    grupos = df_classificacao["Grupo"].unique()

    graficos = []
    for v in variaveis:
        fig = px.box(df_classificacao, x="Grupo", y=v, color="Grupo", points="all")
        grafico = dcc.Graph(figure=fig)
        graficos_variavel = {"variavel": v, "grafico": grafico}

        graficos.append(graficos_variavel)

    tabela = html.Div(className="row",
                      children=[
                          html.Div(
                              className="col-sm-12 col-md-6 col-lg-4 p-1",
                              children=[grafico["grafico"]])
                          for grafico in graficos], style={"overflow-x": "horizontal"})

    return tabela
