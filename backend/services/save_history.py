from fastapi import APIRouter
from httpx import request

router = APIRouter()

@router.post("/save-history/plate")
def save_plate():
    data = request.get_json()
    plate = data.get("plate")
    return {"plate": plate}

@router.post("/save-history/history")
def save_history():
    data = request.get_json()
    matricula = data.get("matricula")
    pesquisa = data.get("pesquisa")
    return {"matricula": matricula, "pesquisa": pesquisa}