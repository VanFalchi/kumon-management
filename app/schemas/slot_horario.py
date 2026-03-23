from pydantic import BaseModel
from typing import Optional
from datetime import time, datetime
from uuid import UUID

class SlotHorarioBase(BaseModel):
    dia_semana: str
    hora_inicio: time
    hora_fim: time

class SlotHorarioCreate(SlotHorarioBase):
    pass

class SlotHorarioUpdate(BaseModel):
    dia_semana: Optional[str] = None
    hora_inicio: Optional[time] = None
    hora_fim: Optional[time] = None
    ativo: Optional[bool] = None

class SlotHorarioResponse(SlotHorarioBase):
    id: UUID
    ativo: bool
    created_at: datetime

    class Config:
        from_attributes = True