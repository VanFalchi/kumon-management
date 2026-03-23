from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from uuid import UUID
from decimal import Decimal

class MatriculaBase(BaseModel):
    aluno_id: UUID
    materia_id: UUID
    valor_real: Decimal
    escola: Optional[str] = None
    serie_escolar: Optional[str] = None
    ano_letivo: Optional[int] = None
    eh_adulto: Optional[bool] = False
    data_inicio: date

class MatriculaCreate(MatriculaBase):
    pass

class MatriculaUpdate(BaseModel):
    valor_real: Optional[Decimal] = None
    escola: Optional[str] = None
    serie_escolar: Optional[str] = None
    ano_letivo: Optional[int] = None
    data_fim: Optional[date] = None
    motivo_encerramento: Optional[str] = None

class MatriculaResponse(MatriculaBase):
    id: UUID
    valor_cheio: Decimal
    data_fim: Optional[date] = None
    motivo_encerramento: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True