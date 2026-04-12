from algorithms.custo_uniforme import custo_uniforme
from fastapi import APIRouter

router = APIRouter()

@router.get("/custo-uniforme")
def custo_uniforme_service(partida, destino):
    caminho, custo, coordenadas = custo_uniforme(partida, destino)
    
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