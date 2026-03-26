from algorithms.profundidade_limitada import profundidade_limitada
from data.cities_graph import cidades_vizinhas


def executar_profundidade(inicio, objetivo, limite=10):
    resultado = profundidade_limitada(
        cidades_vizinhas,
        inicio,
        objetivo,
        limite
    )
    
    if resultado:
        caminho, custo = resultado
        return {
            "caminho": caminho,
            "custo": custo
        }
    else:
        return {
            "erro": "Nenhum caminho encontrado dentro do limite"
        }
        
        
