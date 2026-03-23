from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.models.aluno import Aluno
from app.models.responsavel import Responsavel
from app.models.aluno_responsavel import AlunoResponsavel
from app.schemas.aluno import AlunoCreate, AlunoUpdate, AlunoResponse

router = APIRouter(prefix="/alunos", tags=["Alunos"])

@router.get("/", response_model=List[AlunoResponse])
def listar_alunos(db: Session = Depends(get_db)):
    return db.query(Aluno).all()

@router.get("/{aluno_id}", response_model=AlunoResponse)
def buscar_aluno(aluno_id: UUID, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return aluno

@router.post("/", response_model=AlunoResponse, status_code=status.HTTP_201_CREATED)
def criar_aluno(aluno: AlunoCreate, db: Session = Depends(get_db)):
    db_aluno = Aluno(**aluno.model_dump())
    db.add(db_aluno)
    db.commit()
    db.refresh(db_aluno)
    return db_aluno

@router.put("/{aluno_id}", response_model=AlunoResponse)
def atualizar_aluno(aluno_id: UUID, aluno: AlunoUpdate, db: Session = Depends(get_db)):
    db_aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not db_aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    for campo, valor in aluno.model_dump(exclude_unset=True).items():
        setattr(db_aluno, campo, valor)
    db.commit()
    db.refresh(db_aluno)
    return db_aluno

@router.delete("/{aluno_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_aluno(aluno_id: UUID, db: Session = Depends(get_db)):
    db_aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not db_aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    db.delete(db_aluno)
    db.commit()