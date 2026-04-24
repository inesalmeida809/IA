from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from fastapi import HTTPException

# --- IMPORTS DO LLM ---
from llm.llm_logic.download_modelo import verificar_instalar_modelo
from llm.llm_logic.iniciar_modelo import iniciar_modelo

# --- IMPORTS DO OCR ---
from ocr.leitura_matricula import ler_matricula

# --- IMPORTS DOS SERVIÇOS ---
from services.procura_sofrega_service import router as procura_sofrega_router
from services.custo_uniforme_service import router as custo_uniforme_router
from services.profundidade_limitada_service import router as procura_limitada_router
from services.a_service import router as a_service_router
from services.cities_service import router as cities_router
from services.modelo_ia_service import router as modelo_ia_router
from services.save_history import router as save_history_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.llm = None
    
    modelo_pronto = verificar_instalar_modelo()

    if modelo_pronto:
        print("A iniciar o motor IA...")
        app.state.llm = iniciar_modelo()
        if app.state.llm:
            print("Motor IA ligado com sucesso e pronto para a API!")
    else:
        print("Arranque a prosseguir sem o LLM")

    yield 

    if app.state.llm:
        print("A limpar a memória da IA...")
        app.state.llm = None
    

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(procura_sofrega_router)
app.include_router(custo_uniforme_router)
app.include_router(procura_limitada_router)
app.include_router(a_service_router)
app.include_router(cities_router)
app.include_router(modelo_ia_router)
app.include_router(save_history_router)


@app.post("/login")
def login(file: UploadFile = File(...)):
    resultado = ler_matricula(file)

    if "erro" in resultado:
        erro = resultado["erro"]

        if erro == "MATRICULA_NAO_ENCONTRADA":
            raise HTTPException(status_code=404, detail="Matrícula não encontrada")

        elif erro == "OCR_SEM_RESULTADO":
            raise HTTPException(status_code=422, detail="Não foi possível ler a matrícula")

        elif erro.startswith("TEXTO_INCOMPLETO"):
            raise HTTPException(status_code=422, detail=erro)

        else:
            raise HTTPException(status_code=400, detail=erro)
    
    return {
        "matricula": resultado["matricula"],
        "valida": resultado["valida"],
        "texto_bruto": resultado["texto_bruto"],
        "mensagem": "Login efetuado"
    }

@app.get("/")
def health():
    return {"status": "ok"}