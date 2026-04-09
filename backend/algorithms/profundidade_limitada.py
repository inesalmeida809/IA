def profundidade_limitada(grafo, atual, objetivo, limite, caminho=None, custo=0, iteracoes=None):
    if caminho is None:
        caminho = [atual]
        
    if iteracoes is None:
        iteracoes = []
        
    iteracoes.append({
        "no_atual": atual,
        "caminho": caminho,
        "custo":  custo,
        "limite_restante": limite
    })
    
    if atual == objetivo:
        return caminho, custo, iteracoes
    
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
                custo + distancia,
                iteracoes
            )
            
            if resultado is not None:
                return resultado
            
    return None

