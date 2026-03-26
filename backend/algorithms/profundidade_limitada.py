from data.cities_graph import cidades_vizinhas

def profundidade_limitada(grafo, atual, objetivo, limite, caminho=None, custo=0):
    if caminho is None:
        caminho = [atual]
    
    print(f"[Visita] {atual} | [Limite]: {limite} | [Custo]: {custo}")
    
    if atual == objetivo:
        return caminho, custo
    
    if limite == 0:
        return None
    
    for vizinho, distancia in grafo[atual].items():
        if vizinho not in caminho:
            resultado = profundidade_limitada(
                grafo,
                vizinho,
                objetivo,
                limite - 1,
                caminho + [vizinho],
                custo + distancia
            )
            
            if resultado is not None:
                return resultado
            
    return None

