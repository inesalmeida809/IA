from algorithms.profundidade_limitada import profundidade_limitada
from data.cities_graph import cidades_vizinhas
from fastapi import APIRouter

router = APIRouter()

@router.get("/profundidade-limitada")
def profundidade_limitada_service(partida, destino, limite=10):
    resultado = profundidade_limitada(
        cidades_vizinhas,
        partida,
        destino,
        limite
    )
    
    if resultado:
        caminho, custo, iteracoes = resultado
        return {
            "algoritmo": "profundidade_limitada",
            "caminho": caminho,
            "custo": custo,
            "iteracoes": iteracoes
        }
    else:
        return {
            "erro": "Nenhum caminho encontrado dentro do limite"
        }