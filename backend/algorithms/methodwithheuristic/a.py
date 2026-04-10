from ...data.cities_graph import cidades_vizinhas
from .calcular_heuristica import calcular_heuristica
from heapq import heappush, heappop

def reconstruir_caminho(pais, atual):
    caminho = [atual]
    while atual in pais:
        atual = pais[atual]
        caminho.append(atual)
    caminho.reverse()
    return caminho

def a_star(partida, destino):
    fila_aberta = []
    heappush(fila_aberta, (0, partida))

    pais = {}
    g_score = {partida: 0}
    f_score = {partida: calcular_heuristica(partida, destino)}
    fila_fechada = set()

    while fila_aberta:
        _, atual = heappop(fila_aberta)

        if atual == destino:
            return {"caminho": reconstruir_caminho(pais, destino), "custo": g_score[destino]}
        if atual in fila_fechada:
            continue
        fila_fechada.add(atual)
        for vizinho, custo in cidades_vizinhas.get(atual, {}).items():
            if vizinho in fila_fechada:
                continue
            tentative_g_score = g_score[atual] + custo
            if vizinho not in g_score or tentative_g_score < g_score[vizinho]:
                pais[vizinho] = atual
                g_score[vizinho] = tentative_g_score
                f_score[vizinho] = tentative_g_score + calcular_heuristica(vizinho, destino)
                heappush(fila_aberta, (f_score[vizinho], vizinho))

    return {"caminho": [], "custo": None}
