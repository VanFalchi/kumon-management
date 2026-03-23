from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.models.horario_aluno import HorarioAluno
from app.models.mesa import Mesa
from app.schemas.horario_aluno import HorarioAlunoCreate, HorarioAlunoUpdate, HorarioAlunoResponse

router = APIRouter(prefix="/horarios", tags=["Horários dos Alunos"])

@router.get("/", response_model=List[HorarioAlunoResponse])
def listar_horarios(db: Session = Depends(get_db)):
    return db.query(HorarioAluno).filter(HorarioAluno.data_fim == None).all()

@router.get("/aluno/{aluno_id}", response_model=List[HorarioAlunoResponse])
def listar_horarios_aluno(aluno_id: UUID, db: Session = Depends(get_db)):
    return db.query(HorarioAluno).filter(
        HorarioAluno.aluno_id == aluno_id,
        HorarioAluno.data_fim == None
    ).all()

@router.post("/", response_model=HorarioAlunoResponse, status_code=status.HTTP_201_CREATED)
def criar_horario(horario: HorarioAlunoCreate, db: Session = Depends(get_db)):
    # Verificar se há vaga disponível
    mesa = db.query(Mesa).filter(Mesa.id == horario.mesa_id).first()
    if not mesa:
        raise HTTPException(status_code=404, detail="Mesa não encontrada")
    
    ocupados = db.query(HorarioAluno).filter(
        HorarioAluno.mesa_id == horario.mesa_id,
        HorarioAluno.slot_horario_id == horario.slot_horario_id,
        HorarioAluno.data_fim == None
    ).count()

    if ocupados >= mesa.capacidade:
        raise HTTPException(
            status_code=400,
            detail=f"Mesa {mesa.nome} está lotada neste horário ({ocupados}/{mesa.capacidade} vagas)"
        )

    db_horario = HorarioAluno(**horario.model_dump())
    db.add(db_horario)
    db.commit()
    db.refresh(db_horario)
    return db_horario

@router.put("/{horario_id}", response_model=HorarioAlunoResponse)
def encerrar_horario(horario_id: UUID, horario: HorarioAlunoUpdate, db: Session = Depends(get_db)):
    db_horario = db.query(HorarioAluno).filter(HorarioAluno.id == horario_id).first()
    if not db_horario:
        raise HTTPException(status_code=404, detail="Horário não encontrado")
    for campo, valor in horario.model_dump(exclude_unset=True).items():
        setattr(db_horario, campo, valor)
    db.commit()
    db.refresh(db_horario)
    return db_horario