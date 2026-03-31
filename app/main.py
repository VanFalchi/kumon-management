from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from contextlib import asynccontextmanager
from app.auth import create_access_token, verify_password
from app.routers import alunos, responsaveis, materias, matriculas, mesas, slots_horario, horarios_alunos, webhook, cobrancas, boletos
from app.jobs.scheduler import iniciar_scheduler, parar_scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    iniciar_scheduler()
    yield
    parar_scheduler()

app = FastAPI(
    title="Kumon Management",
    description="Sistema de Gestão Financeira para Franquia Kumon",
    version="0.1.0",
    lifespan=lifespan
)

TEMP_USER = {
    "username": "admin",
    "hashed_password": "$2b$12$3fq0UA2Reo2n.tYkdF0HY.6WNm6fCdKnFl9tYCdptMjY/HvZdGB.i"
}

@app.get("/")
def root():
    return {"status": "ok", "sistema": "Kumon Management", "versao": "0.1.0"}

@app.post("/auth/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != TEMP_USER["username"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos"
        )
    if not verify_password(form_data.password, TEMP_USER["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos"
        )
    token = create_access_token(data={"sub": form_data.username})
    return {"access_token": token, "token_type": "bearer"}

app.include_router(alunos.router)
app.include_router(responsaveis.router)
app.include_router(materias.router)
app.include_router(matriculas.router)
app.include_router(mesas.router)
app.include_router(slots_horario.router)
app.include_router(horarios_alunos.router)
app.include_router(webhook.router)
app.include_router(cobrancas.router)
app.include_router(boletos.router)