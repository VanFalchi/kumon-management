from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.models.slot_horario import SlotHorario
from app.schemas.slot_horario import SlotHorarioCreate, SlotHorarioUpdate, SlotHorarioResponse

router = APIRouter(prefix="/slots", tags=["Slots de Horário"])

@router.get("/", response_model=List[SlotHorarioResponse])
def listar_slots(db: Session = Depends(get_db)):
    return db.query(SlotHorario).all()

@router.get("/{slot_id}", response_model=SlotHorarioResponse)
def buscar_slot(slot_id: UUID, db: Session = Depends(get_db)):
    slot = db.query(SlotHorario).filter(SlotHorario.id == slot_id).first()
    if not slot:
        raise HTTPException(status_code=404, detail="Slot não encontrado")
    return slot

@router.post("/", response_model=SlotHorarioResponse, status_code=status.HTTP_201_CREATED)
def criar_slot(slot: SlotHorarioCreate, db: Session = Depends(get_db)):
    db_slot = SlotHorario(**slot.model_dump())
    db.add(db_slot)
    db.commit()
    db.refresh(db_slot)
    return db_slot

@router.put("/{slot_id}", response_model=SlotHorarioResponse)
def atualizar_slot(slot_id: UUID, slot: SlotHorarioUpdate, db: Session = Depends(get_db)):
    db_slot = db.query(SlotHorario).filter(SlotHorario.id == slot_id).first()
    if not slot:
        raise HTTPException(status_code=404, detail="Slot não encontrado")
    for campo, valor in slot.model_dump(exclude_unset=True).items():
        setattr(db_slot, campo, valor)
    db.commit()
    db.refresh(db_slot)
    return db_slot

@router.delete("/{slot_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_slot(slot_id: UUID, db: Session = Depends(get_db)):
    db_slot = db.query(SlotHorario).filter(SlotHorario.id == slot_id).first()
    if not db_slot:
        raise HTTPException(status_code=404, detail="Slot não encontrado")
    db.delete(db_slot)
    db.commit()