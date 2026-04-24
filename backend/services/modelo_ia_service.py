from fastapi import APIRouter, Request, Query
from fastapi.responses import StreamingResponse
from typing import List
from llm.llm_logic.prompt_atracoes import atracoes_monumentos_stream

router = APIRouter()

@router.get("/atracoes_monumentos")
def atracoes_e_monumentos_service(request: Request, cidades: List[str] = Query(...)):

    motor_llm = getattr(request.app.state, "llm", None)
    if not motor_llm:
        return {"erro": "O modelo IA não está carregado no servidor."}
    
    return StreamingResponse(
        atracoes_monumentos_stream(motor_llm, cidades),
        media_type="application/x-ndjson"
    )