from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from decimal import Decimal

from app.database import get_db
from app.models.matricula import Matricula
from app.schemas.matricula import MatriculaCreate, MatriculaUpdate, MatriculaResponse

router = APIRouter(prefix="/matriculas", tags=["Matrículas"])

@router.get("/", response_model=List[MatriculaResponse])
def listar_matriculas(db: Session = Depends(get_db)):
    return db.query(Matricula).all()

@router.get("/aluno/{aluno_id}", response_model=List[MatriculaResponse])
def listar_matriculas_aluno(aluno_id: UUID, db: Session = Depends(get_db)):
    return db.query(Matricula).filter(Matricula.aluno_id == aluno_id).all()

@router.get("/{matricula_id}", response_model=MatriculaResponse)
def buscar_matricula(matricula_id: UUID, db: Session = Depends(get_db)):
    matricula = db.query(Matricula).filter(Matricula.id == matricula_id).first()
    if not matricula:
        raise HTTPException(status_code=404, detail="Matrícula não encontrada")
    return matricula

@router.post("/", response_model=MatriculaResponse, status_code=status.HTTP_201_CREATED)
def criar_matricula(matricula: MatriculaCreate, db: Session = Depends(get_db)):
    dados = matricula.model_dump()
    dados["valor_cheio"] = round(dados["valor_real"] / Decimal("0.90"), 2)
    db_matricula = Matricula(**dados)
    db.add(db_matricula)
    db.commit()
    db.refresh(db_matricula)
    return db_matricula

@router.put("/{matricula_id}", response_model=MatriculaResponse)
def atualizar_matricula(matricula_id: UUID, matricula: MatriculaUpdate, db: Session = Depends(get_db)):
    db_matricula = db.query(Matricula).filter(Matricula.id == matricula_id).first()
    if not db_matricula:
        raise HTTPException(status_code=404, detail="Matrícula não encontrada")
    dados = matricula.model_dump(exclude_unset=True)
    if "valor_real" in dados:
        dados["valor_cheio"] = round(dados["valor_real"] / Decimal("0.90"), 2)
    for campo, valor in dados.items():
        setattr(db_matricula, campo, valor)
    db.commit()
    db.refresh(db_matricula)
    return db_matricula

@router.delete("/{matricula_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_matricula(matricula_id: UUID, db: Session = Depends(get_db)):
    db_matricula = db.query(Matricula).filter(Matricula.id == matricula_id).first()
    if not db_matricula:
        raise HTTPException(status_code=404, detail="Matrícula não encontrada")
    db.delete(db_matricula)
    db.commit()