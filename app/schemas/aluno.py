from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from uuid import UUID

class AlunoBase(BaseModel):
    nome: str
    data_nascimento: Optional[date] = None
    data_matricula: date
    observacoes: Optional[str] = None

class AlunoCreate(AlunoBase):
    pass

class AlunoUpdate(BaseModel):
    nome: Optional[str] = None
    data_nascimento: Optional[date] = None
    observacoes: Optional[str] = None
    status: Optional[str] = None

class AlunoResponse(AlunoBase):
    id: UUID
    status: str
    created_at: datetime

    class Config:
        from_attributes = True