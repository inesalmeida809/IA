from fastapi import APIRouter
from algorithms.methodwithheuristic.procura_sofrega import procura_sofrega

router = APIRouter()

@router.get("/procura-sofrega")
def procura_sofrega_service(chegada, destino):
    caminho, distancia = procura_sofrega(chegada, destino)
    
    if caminho is not None and distancia is not None:
        return {
            "caminho": caminho,
            "distancia": distancia,
        }
    else:
        return {
            "erro": "Nenhum caminho encontrado"
        }