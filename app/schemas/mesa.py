from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class MesaBase(BaseModel):
    nome: str
    capacidade: int

class MesaCreate(MesaBase):
    pass

class MesaUpdate(BaseModel):
    nome: Optional[str] = None
    capacidade: Optional[int] = None
    ativa: Optional[bool] = None

class MesaResponse(MesaBase):
    id: UUID
    ativa: bool
    created_at: datetime

    class Config:
        from_attributes = True