import uuid
from sqlalchemy import Column, String, Boolean, Date, DateTime, Numeric, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base

class Matricula(Base):
    __tablename__ = "matriculas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    aluno_id = Column(UUID(as_uuid=True), ForeignKey("alunos.id"), nullable=False)
    materia_id = Column(UUID(as_uuid=True), ForeignKey("materias.id"), nullable=False)
    valor_real = Column(Numeric(10, 2), nullable=False)
    valor_cheio = Column(Numeric(10, 2), nullable=False)
    escola = Column(String(150), nullable=True)
    serie_escolar = Column(String(50), nullable=True)
    ano_letivo = Column(Integer, nullable=True)
    eh_adulto = Column(Boolean, default=False)
    data_inicio = Column(Date, nullable=False)
    data_fim = Column(Date, nullable=True)
    motivo_encerramento = Column(String(200), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())