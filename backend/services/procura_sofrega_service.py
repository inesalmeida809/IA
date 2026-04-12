from fastapi import APIRouter
from algorithms.methodwithheuristic.procura_sofrega import procura_sofrega

router = APIRouter()

@router.get("/procura-sofrega")
def procura_sofrega_service(partida, destino):
    caminho, distancia, coordenadas = procura_sofrega(partida, destino)
    
    if caminho is not None and distancia is not None and coordenadas is not None:
        return {
            "caminho": caminho,
            "distancia": distancia,
            "coordenadas": coordenadas,
        }
    else:
        return {
            "erro": "Nenhum caminho encontrado"
        }