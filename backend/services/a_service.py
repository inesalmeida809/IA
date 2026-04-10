from fastapi import APIRouter
from algorithms.methodwithheuristic.a import a_star

router = APIRouter()

@router.get("/a-star")
def a_star_service(chegada, destino):
    caminho, custo = a_star(chegada, destino)

    if caminho is not None and custo is not None:
        return {
            "caminho": caminho,
            "custo": custo,
        }
    else:
        return {
            "erro": "Nenhum caminho encontrado"
        }