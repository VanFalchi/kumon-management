import uuid
from sqlalchemy import Column, String, Date, Enum, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base

class Aluno(Base):
    __tablename__ = "alunos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String(150), nullable=False)
    data_nascimento = Column(Date, nullable=True)
    data_matricula = Column(Date, nullable=False)
    status = Column(Enum('ativo', 'inativo', 'concluinte', name='status_aluno'), default='ativo')
    observacoes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())