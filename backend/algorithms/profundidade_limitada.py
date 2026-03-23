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

def executarProfundidadeLimitada(inicio, objetivo, limite):
    print('\nProcura em Profundidade Limitada')
    print(f'[Início]: {inicio} | [Objetivo]: {objetivo} | [Limite]: {limite}\n')
    
    resultado = profundidade_limitada(
        cidades_vizinhas,
        inicio,
        objetivo,
        limite
    )
    
    if resultado:
        caminho, custo = resultado
        print('\nCaminho encontrado!')
        print('->'.join(caminho))
        print(f'Distância total: {custo} Km')
    else:
        print('Nenhum caminho encontrado dentro do limite')