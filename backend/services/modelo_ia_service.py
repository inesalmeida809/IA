from fastapi import APIRouter, Request, Query
from typing import List
from llm.llm_logic.prompt_atracoes import atracoes_monumentos

router = APIRouter()

@router.get("/atracoes_monumentos")
def atracoes_e_monumentos_service(request: Request, cidades: List[str] = Query(...)):

    motor_llm = getattr(request.app.state, "llm", None)
    if not motor_llm:
        return {"erro": "O modelo IA não está carregado no servidor."}

    json_atracoes = atracoes_monumentos(motor_llm, cidades)
    
    if json_atracoes:
        return json_atracoes
    else:
        return {
            "erro": "Nenhuma atração ou monumento foi encontrado."
        }