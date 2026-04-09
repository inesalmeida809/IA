from services.profundidade_service import executar_profundidade
from services.a_service import executar_a
from services.custo_service import executar_custo
from services.procura_service import executar_procura

def executar_busca(algoritmo, inicio, destino):
    
    if algoritmo == "profundidade":
        return executar_profundidade (inicio, destino)
    
    elif algoritmo == "a":
        return executar_a(inicio, destino)
    
    elif algoritmo == "custo_uniforme":
        return executar_custo(inicio, destino)
    
    elif algoritmo == "procura_sofrega":
        return executar_procura(inicio, destino)
    
    else:
        return{"erro": "Algoritmo inválido"}