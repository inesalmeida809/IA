from fastapi import FastAPI, UploadFile, File
from ocr.leitura_matricula import ler_matricula

from services.procura_sofrega_service import router as procura_sofrega_router
from services.custo_uniforme_service import router as custo_uniforme_router
from services.profundidade_limitada_service import router as procura_limitada_router
from services.a_service import router as a_service_router


app = FastAPI()


app.include_router(procura_sofrega_router)
app.include_router(custo_uniforme_router)
app.include_router(procura_limitada_router)
app.include_router(a_service_router)


@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/login")
def login(file: UploadFile = File(...)):
    matricula = ler_matricula(file)
    
    return {
        "matricula": matricula,
        "mensagem": "Login efetuado"
    }
