from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

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

modelo_ia = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global modelo_ia
    
    verificar_instalar_modelo()
    
    app.state.llm = iniciar_modelo()
    
    if app.state.llm:
        print("Motor IA ligado com sucesso e pronto para a API!")
    
    yield 
    
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


@app.post("/login")
def login(file: UploadFile = File(...)):
    matricula = ler_matricula(file)
    
    return {
        "matricula": matricula,
        "mensagem": "Login efetuado"
    }

@app.get("/")
def health():
    return {"status": "ok"}