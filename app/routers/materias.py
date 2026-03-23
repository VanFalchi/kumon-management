from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.models.materia import Materia
from app.schemas.materia import MateriaCreate, MateriaUpdate, MateriaResponse

router = APIRouter(prefix="/materias", tags=["Matérias"])

@router.get("/", response_model=List[MateriaResponse])
def listar_materias(db: Session = Depends(get_db)):
    return db.query(Materia).all()

@router.get("/{materia_id}", response_model=MateriaResponse)
def buscar_materia(materia_id: UUID, db: Session = Depends(get_db)):
    materia = db.query(Materia).filter(Materia.id == materia_id).first()
    if not materia:
        raise HTTPException(status_code=404, detail="Matéria não encontrada")
    return materia

@router.post("/", response_model=MateriaResponse, status_code=status.HTTP_201_CREATED)
def criar_materia(materia: MateriaCreate, db: Session = Depends(get_db)):
    db_materia = Materia(**materia.model_dump())
    db.add(db_materia)
    db.commit()
    db.refresh(db_materia)
    return db_materia

@router.put("/{materia_id}", response_model=MateriaResponse)
def atualizar_materia(materia_id: UUID, materia: MateriaUpdate, db: Session = Depends(get_db)):
    db_materia = db.query(Materia).filter(Materia.id == materia_id).first()
    if not db_materia:
        raise HTTPException(status_code=404, detail="Matéria não encontrada")
    for campo, valor in materia.model_dump(exclude_unset=True).items():
        setattr(db_materia, campo, valor)
    db.commit()
    db.refresh(db_materia)
    return db_materia

@router.delete("/{materia_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_materia(materia_id: UUID, db: Session = Depends(get_db)):
    db_materia = db.query(Materia).filter(Materia.id == materia_id).first()
    if not db_materia:
        raise HTTPException(status_code=404, detail="Matéria não encontrada")
    db.delete(db_materia)
    db.commit()