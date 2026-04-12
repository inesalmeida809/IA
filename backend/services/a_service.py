from fastapi import APIRouter
from algorithms.methodwithheuristic.a import a_star

router = APIRouter()

@router.get("/a-star")
def a_star_service(partida, destino):
    caminho, custo, coordenadas = a_star(partida, destino)

    if caminho is not None and custo is not None and coordenadas is not None:
        return {
            "caminho": caminho,
            "custo": custo,
            "coordenadas": coordenadas,
        }
    else:
        return {
            "erro": "Nenhum caminho encontrado"
        }