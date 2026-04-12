from algorithms.profundidade_limitada import profundidade_limitada
from data.cities_graph import cidades_vizinhas
from fastapi import APIRouter

router = APIRouter()

@router.get("/profundidade-limitada")
def profundidade_limitada_service(partida, destino, limite=10):
    caminho, custo, iteracoes, coordenadas =  profundidade_limitada(cidades_vizinhas, partida, destino, limite)
    
    if caminho is not None and custo is not None and coordenadas is not None:
        return {
            "caminho": caminho,
            "custo": custo,
            "coordenadas": coordenadas,
        }
    else:
        return {
            "erro": "Nenhum caminho encontrado dentro do limite"
        }