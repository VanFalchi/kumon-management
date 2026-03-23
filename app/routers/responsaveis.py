from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.models.responsavel import Responsavel
from app.schemas.responsavel import ResponsavelCreate, ResponsavelUpdate, ResponsavelResponse

router = APIRouter(prefix="/responsaveis", tags=["Responsáveis"])

@router.get("/", response_model=List[ResponsavelResponse])
def listar_responsaveis(db: Session = Depends(get_db)):
    return db.query(Responsavel).all()

@router.get("/{responsavel_id}", response_model=ResponsavelResponse)
def buscar_responsavel(responsavel_id: UUID, db: Session = Depends(get_db)):
    responsavel = db.query(Responsavel).filter(Responsavel.id == responsavel_id).first()
    if not responsavel:
        raise HTTPException(status_code=404, detail="Responsável não encontrado")
    return responsavel

@router.post("/", response_model=ResponsavelResponse, status_code=status.HTTP_201_CREATED)
def criar_responsavel(responsavel: ResponsavelCreate, db: Session = Depends(get_db)):
    db_responsavel = Responsavel(**responsavel.model_dump())
    db.add(db_responsavel)
    db.commit()
    db.refresh(db_responsavel)
    return db_responsavel

@router.put("/{responsavel_id}", response_model=ResponsavelResponse)
def atualizar_responsavel(responsavel_id: UUID, responsavel: ResponsavelUpdate, db: Session = Depends(get_db)):
    db_responsavel = db.query(Responsavel).filter(Responsavel.id == responsavel_id).first()
    if not db_responsavel:
        raise HTTPException(status_code=404, detail="Responsável não encontrado")
    for campo, valor in responsavel.model_dump(exclude_unset=True).items():
        setattr(db_responsavel, campo, valor)
    db.commit()
    db.refresh(db_responsavel)
    return db_responsavel

@router.delete("/{responsavel_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_responsavel(responsavel_id: UUID, db: Session = Depends(get_db)):
    db_responsavel = db.query(Responsavel).filter(Responsavel.id == responsavel_id).first()
    if not db_responsavel:
        raise HTTPException(status_code=404, detail="Responsável não encontrado")
    db.delete(db_responsavel)
    db.commit()