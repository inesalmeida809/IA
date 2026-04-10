from fastapi import FastAPI

from services.procura_sofrega_service import router as procura_sofrega_router


app = FastAPI()

app.include_router(procura_sofrega_router)

@app.get("/")
def health():
    return {"status": "ok"}