import uuid
from sqlalchemy import Column, Enum, Time, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base

class SlotHorario(Base):
    __tablename__ = "slots_horario"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dia_semana = Column(Enum('seg', 'ter', 'qua', 'qui', 'sex', 'sab', name='dia_semana'), nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fim = Column(Time, nullable=False)
    ativo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())