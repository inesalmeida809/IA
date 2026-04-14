from algorithms.profundidade_limitada import profundidade_limitada
from data.cities_graph import cidades_vizinhas
from fastapi import APIRouter

router = APIRouter()

@router.get("/profundidade-limitada")
def profundidade_limitada_service(partida: str, destino: str, limite: int = 10):
    caminho, custo, iteracoes, coordenadas = profundidade_limitada(
        cidades_vizinhas, partida, destino, limite
    )

    if caminho and custo is not None:
        return {
            "algoritmo": "profundidade_limitada",
            "caminho": caminho,
            "custo": custo,
            "iteracoes": iteracoes,
            "coordenadas": coordenadas
        }

    return {
        "erro": "Nenhum caminho encontrado dentro do limite"
    }