from data.cities_graph import cidades_vizinhas
from data.city_coordinates import coordenadas

def custo_uniforme(cidade_partida, cidade_chegada):
    print(f"Eu quero ir de {cidade_partida} para {cidade_chegada}!")
    dict_caminho = [(0, cidade_partida, [cidade_partida])]
    visitados = {}

    while dict_caminho:
        dict_caminho.sort(key=lambda x: x[0])

        custo_atual, cidade_atual, caminho = dict_caminho.pop(0)

        if cidade_atual == cidade_chegada:
            print(f"Chegou ao destino!\nCaminho: {' -> '.join(caminho)}\nCusto: {custo_atual} km")
            coordenadas_cidades = [coordenadas.get(cidade) for cidade in caminho]
            return caminho, custo_atual, coordenadas_cidades
        
        if cidade_atual in visitados and visitados[cidade_atual] <= custo_atual:
            continue

        visitados[cidade_atual] = custo_atual

        for vizinho, custo in cidades_vizinhas.get(cidade_atual, {}).items():
            novo_custo = custo_atual + custo
            novo_caminho = caminho + [vizinho]
            dict_caminho.append((novo_custo, vizinho, novo_caminho))

    print("Não existe caminho.")
    return [], None, []
