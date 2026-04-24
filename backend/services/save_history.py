import json
import os
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any

router = APIRouter()

FICHEIRO_JSON = "dados.json"

def ler_json():
    """Lê o ficheiro JSON e retorna a lista de dados. Se não existir, retorna lista vazia."""
    if os.path.exists(FICHEIRO_JSON):
        with open(FICHEIRO_JSON, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def escrever_json(dados):
    """Escreve a lista de dados de volta no ficheiro JSON."""
    with open(FICHEIRO_JSON, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


class PlateSchema(BaseModel):
    plate: str

class HistorySchema(BaseModel):
    matricula: str
    pesquisa: Dict[str, Any]



@router.post("/save-history/plate")
def save_plate(data: PlateSchema):
    dados = ler_json()
    
    matricula_existe = any(item.get("matricula") == data.plate for item in dados)
    
    if not matricula_existe:
        novo_registo = {
            "matricula": data.plate,
            "historico": []
        }
        dados.append(novo_registo)
        escrever_json(dados)
        return {"mensagem": "Nova matrícula registada com sucesso!", "dados": novo_registo}
    
    return {"mensagem": "Matrícula já existia no sistema. Login efetuado."}


@router.post("/save-history/history")
def save_history(data: HistorySchema):
    dados = ler_json()
    
    matricula_encontrada = False
    
    for item in dados:
        if item.get("matricula") == data.matricula:

            if "historico" not in item:
                item["historico"] = [] 
            
            item["historico"].append(data.pesquisa)
            matricula_encontrada = True
            break
            
    if not matricula_encontrada:
        novo_registo = {
            "matricula": data.matricula,
            "historico": [data.pesquisa]
        }
        dados.append(novo_registo)

    escrever_json(dados)
    
    return {"mensagem": "Viagem adicionada ao histórico da matrícula!"}