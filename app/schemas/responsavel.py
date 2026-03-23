from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class ResponsavelBase(BaseModel):
    nome: str
    cpf: Optional[str] = None
    telefone_whatsapp: str
    email: Optional[str] = None
    endereco: Optional[str] = None
    profissao: Optional[str] = None
    empresa: Optional[str] = None
    preferencia_boleto: Optional[str] = "digital"

class ResponsavelCreate(ResponsavelBase):
    pass

class ResponsavelUpdate(BaseModel):
    nome: Optional[str] = None
    cpf: Optional[str] = None
    telefone_whatsapp: Optional[str] = None
    email: Optional[str] = None
    endereco: Optional[str] = None
    profissao: Optional[str] = None
    empresa: Optional[str] = None
    preferencia_boleto: Optional[str] = None

class ResponsavelResponse(ResponsavelBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True