from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class MateriaBase(BaseModel):
    nome: str
    abreviacao: str

class MateriaCreate(MateriaBase):
    pass

class MateriaUpdate(BaseModel):
    nome: Optional[str] = None
    abreviacao: Optional[str] = None
    ativa: Optional[bool] = None

class MateriaResponse(MateriaBase):
    id: UUID
    ativa: bool
    created_at: datetime

    class Config:
        from_attributes = True