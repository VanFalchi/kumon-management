from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from uuid import UUID

class HorarioAlunoBase(BaseModel):
    aluno_id: UUID
    matricula_id: UUID
    mesa_id: UUID
    slot_horario_id: UUID
    data_inicio: date

class HorarioAlunoCreate(HorarioAlunoBase):
    pass

class HorarioAlunoUpdate(BaseModel):
    data_fim: Optional[date] = None

class HorarioAlunoResponse(HorarioAlunoBase):
    id: UUID
    data_fim: Optional[date] = None
    created_at: datetime

    class Config:
        from_attributes = True