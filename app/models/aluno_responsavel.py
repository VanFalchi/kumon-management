import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base

class AlunoResponsavel(Base):
    __tablename__ = "alunos_responsaveis"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    aluno_id = Column(UUID(as_uuid=True), ForeignKey("alunos.id"), nullable=False)
    responsavel_id = Column(UUID(as_uuid=True), ForeignKey("responsaveis.id"), nullable=False)
    responsavel_financeiro = Column(Boolean, default=False)
    parentesco = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())