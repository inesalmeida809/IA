from data.city_coordinates import coordenadas

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
        coordenadas_cidades = [coordenadas.get(cidade) for cidade in caminho]
        return caminho, custo, iteracoes, coordenadas_cidades
    
    if limite == 0:
        return [], None, iteracoes, []
    
    for vizinho, distancia in grafo.get(atual, {}).items():
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
            
            if resultado[0]:
                return resultado
            
    return [], None, iteracoes, []

