from ...data.cities_graph import cidades_vizinhas
from ...data.heuristics import distancias_retas
from calcular_heuristica import calcular_heuristica

def procura_sofrega(cidade_origem, cidade_destino):
    caminho = [cidade_origem]
    cidade_atual = cidade_origem

    while cidade_atual != cidade_destino:
        proximos_nos = cidades_vizinhas.get(cidade_atual, {})

        for pn in proximos_nos:
            calcular_heuristica(pn, cidade_destino)
