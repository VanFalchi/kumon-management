from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.models.mesa import Mesa
from app.models.horario_aluno import HorarioAluno
from app.schemas.mesa import MesaCreate, MesaUpdate, MesaResponse

router = APIRouter(prefix="/mesas", tags=["Mesas"])

@router.get("/", response_model=List[MesaResponse])
def listar_mesas(db: Session = Depends(get_db)):
    return db.query(Mesa).all()

@router.get("/{mesa_id}", response_model=MesaResponse)
def buscar_mesa(mesa_id: UUID, db: Session = Depends(get_db)):
    mesa = db.query(Mesa).filter(Mesa.id == mesa_id).first()
    if not mesa:
        raise HTTPException(status_code=404, detail="Mesa não encontrada")
    return mesa

@router.get("/{mesa_id}/vagas/{slot_id}")
def verificar_vagas(mesa_id: UUID, slot_id: UUID, db: Session = Depends(get_db)):
    mesa = db.query(Mesa).filter(Mesa.id == mesa_id).first()
    if not mesa:
        raise HTTPException(status_code=404, detail="Mesa não encontrada")
    ocupados = db.query(HorarioAluno).filter(
        HorarioAluno.mesa_id == mesa_id,
        HorarioAluno.slot_horario_id == slot_id,
        HorarioAluno.data_fim == None
    ).count()
    return {
        "mesa": mesa.nome,
        "capacidade": mesa.capacidade,
        "ocupados": ocupados,
        "vagas_disponiveis": mesa.capacidade - ocupados
    }

@router.post("/", response_model=MesaResponse, status_code=status.HTTP_201_CREATED)
def criar_mesa(mesa: MesaCreate, db: Session = Depends(get_db)):
    db_mesa = Mesa(**mesa.model_dump())
    db.add(db_mesa)
    db.commit()
    db.refresh(db_mesa)
    return db_mesa

@router.put("/{mesa_id}", response_model=MesaResponse)
def atualizar_mesa(mesa_id: UUID, mesa: MesaUpdate, db: Session = Depends(get_db)):
    db_mesa = db.query(Mesa).filter(Mesa.id == mesa_id).first()
    if not db_mesa:
        raise HTTPException(status_code=404, detail="Mesa não encontrada")
    for campo, valor in mesa.model_dump(exclude_unset=True).items():
        setattr(db_mesa, campo, valor)
    db.commit()
    db.refresh(db_mesa)
    return db_mesa

@router.delete("/{mesa_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_mesa(mesa_id: UUID, db: Session = Depends(get_db)):
    db_mesa = db.query(Mesa).filter(Mesa.id == mesa_id).first()
    if not db_mesa:
        raise HTTPException(status_code=404, detail="Mesa não encontrada")
    db.delete(db_mesa)
    db.commit()