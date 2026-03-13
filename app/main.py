from fastapi import FastAPI

app = FastAPI(
    title="Kumon Management",
    description="Sistema de Gestão Financeira para Franquia Kumon",
    version="0.1.0"
)

@app.get("/")
def root():
    return {"status": "ok", "sistema": "Kumon Management", "versao": "0.1.0"}
