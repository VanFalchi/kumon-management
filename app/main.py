from fastapi import FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
from app.auth import create_access_token, verify_password, get_password_hash

app = FastAPI(
    title="Kumon Management",
    description="Sistema de Gestão Financeira para Franquia Kumon",
    version="0.1.0"
)

# Usuário temporário até termos o banco configurado na Fase 2
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