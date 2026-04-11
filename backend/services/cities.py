from fastapi import APIRouter
from data.city_coordinates import coordenadas
router = APIRouter()

@router.get("/cities")
def cities_service():
    return {
        "cidades": list(coordenadas.keys())
    }