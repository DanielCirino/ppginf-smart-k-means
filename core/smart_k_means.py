# importar bibliotecas
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples
from sklearn.metrics import silhouette_score


def avaliar_opcoes_arranjo(qtd_min_clusters, qtd_max_clusters, dataset):
    # Definir range de clusters
    range_clusters = range(qtd_min_clusters, qtd_max_clusters + 1)

    # Lista para armazenar os resultados da clusterização para cada arranjo
    resultados = []

    for i, k in enumerate(range_clusters):
        resultado = {"arranjo": f"{k} Grupos", "qtd_grupos": k}

        # print("="*24)
        # print(f"Calculando K-Means para {k } clusters")
        # print("_"*24)
        # Criar um objeto KMeans
        kmeans = KMeans(n_clusters=k)

        # Treinar o modelo
        kmeans.fit(dataset)
        # Obter os rótulos dos clusters para cada ponto de dados
        rotulos = kmeans.labels_
        centroides = kmeans.cluster_centers_

        resumo_classificacao = []
        qtd_por_grupos = pd.DataFrame(rotulos).groupby(0)[0].count()

        for i, qtd in enumerate(qtd_por_grupos):
            resumo_classificacao.append({"grupo": i + 1, "qtd": qtd, "silhueta": 0})

        # Calcular a silhueta para cada amostra
        silhuetas = silhouette_samples(dataset, rotulos)

        # Calcular a média da silhueta
        silhueta_media = silhouette_score(dataset, rotulos)
        resultado["silhueta_media"] = silhueta_media

        # Calcular a média da silhueta para cada grupo
        for i in np.unique(rotulos):
            resumo_classificacao[i]["silhueta"] = np.mean(silhuetas[rotulos == i])
            resumo_classificacao[i]["centroides"] = centroides[i]

        resultado["resumo_classificacao"] = resumo_classificacao
        resultado["rotulos"] = rotulos
        resultado["silhuetas"] = silhuetas
        resultado["centroides"] = centroides
        # print(resultado)

        resultados.append(resultado)
    return resultados


def obter_resultados_validos(resultados, silhueta_corte=0.50):
    # Avaliar resultados de clusterização para cada arranjo
    resultados_validos = []
    for res in resultados:
        if res["silhueta_media"] > silhueta_corte:
            res["e_valido"] = True
            for grupo in res["resumo_classificacao"]:
                if grupo["silhueta"] < silhueta_corte:  # largura da silhueta do grupo
                    res["e_valido"] = False
                    pass

            resultados_validos.append(res)

    return resultados_validos


def calcular_entropia(valores_variavel):
    unique_values, value_counts = np.unique(valores_variavel, return_counts=True)
    value_probs = value_counts / len(valores_variavel)
    entropy = -np.sum(value_probs * np.log2(value_probs + 1e-10))  # Adicionando um pequeno valor para evitar log(0)
    return entropy


def selecionar_melhor_opcao_arranjo(resultados_validos):
    if len(resultados_validos) == 0:
        return None

    arranjo_selecionado = None
    todos_arranjos_validos = False

    menor_grupo = resultados_validos[0]["qtd_grupos"]
    maior_silhueta = resultados_validos[0]["silhueta_media"]

    indice_menor_grupo = 0
    indice_maior_silhueta = 0

    for i, res in enumerate(resultados_validos):
        if menor_grupo > res["qtd_grupos"]:
            menor_grupo = res["qtd_grupos"]
            indice_menor_grupo = i
            print(menor_grupo, res["qtd_grupos"])

        if maior_silhueta < res["silhueta_media"]:
            maior_silhueta = res["silhueta_media"]
            indice_maior_silhueta = i
            print(maior_silhueta, res["silhueta_media"])

    if todos_arranjos_validos:
        arranjo_selecionado = resultados_validos[indice_menor_grupo]
    else:
        arranjo_selecionado = resultados_validos[indice_maior_silhueta]

    return arranjo_selecionado


def calcular_entropia_dataset(dados):
    entropias = []

    for col in range(dados.shape[1]):
        entropias.append({"variavel": dados.columns[col], "entropia": calcular_entropia(dados.iloc[:, col])})

    dfEntropias = pd.DataFrame(entropias)
    dfEntropias.sort_values(by=["entropia"], ascending=False, inplace=True)

    return dfEntropias


def obter_avaliacao_de_agrupamento(dados, min_clusters=3, max_clusters=7):
    df_entropias = calcular_entropia_dataset(dados)
    resultados = avaliar_opcoes_arranjo(min_clusters, max_clusters, dados)
    resultados_validos = obter_resultados_validos(resultados)
    melhor_arranjo = selecionar_melhor_opcao_arranjo(resultados_validos)

    i_entropia = 0
    iteracao = 1
    sumario_iteracoes = []

    while melhor_arranjo is None:
        qtd_variaveis_restante = dados.shape[1]
        if qtd_variaveis_restante < 3:
            print(
                f"{iteracao} - SEM RESULTADOS VÁLIDOS: Dataset após a exclusão das variáveis não encontrou um resultado.")
            return pd.DataFrame(), None, sumario_iteracoes, iteracao + 1, 0, None

        # recuperar os dados da da maior entropia
        maior_entropia = df_entropias.iloc[i_entropia]

        # Excluir varíavel com maior entropia
        dados = dados.drop([maior_entropia["variavel"]], axis=1)

        # Refazer o K-means utilizando o novo dataset sem a variável com a maior entropia
        resultados = avaliar_opcoes_arranjo(min_clusters, max_clusters, dados)
        resultados_validos = obter_resultados_validos(resultados)

        melhor_arranjo = selecionar_melhor_opcao_arranjo(resultados_validos)

        dados_iteracao = {"iteracao": iteracao,
                          "resultados_validos": len(resultados_validos),
                          "variavel_excluida": maior_entropia["variavel"],
                          "entropia": maior_entropia["entropia"]}

        sumario_iteracoes.append(dados_iteracao)
        i_entropia += 1
        iteracao += 1

    return (df_entropias,
            melhor_arranjo,
            sumario_iteracoes,
            iteracao - 1,
            dados.columns,
            resultados,
            dados)
