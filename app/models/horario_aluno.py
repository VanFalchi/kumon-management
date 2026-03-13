import uuid
from sqlalchemy import Column, Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base

class HorarioAluno(Base):
    __tablename__ = "horarios_alunos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    aluno_id = Column(UUID(as_uuid=True), ForeignKey("alunos.id"), nullable=False)
    matricula_id = Column(UUID(as_uuid=True), ForeignKey("matriculas.id"), nullable=False)
    mesa_id = Column(UUID(as_uuid=True), ForeignKey("mesas.id"), nullable=False)
    slot_horario_id = Column(UUID(as_uuid=True), ForeignKey("slots_horario.id"), nullable=False)
    data_inicio = Column(Date, nullable=False)
    data_fim = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())