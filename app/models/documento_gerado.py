import uuid
from sqlalchemy import Column, Text, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base

class DocumentoGerado(Base):
    __tablename__ = "documentos_gerados"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    template_id = Column(UUID(as_uuid=True), ForeignKey("templates_documentos.id"), nullable=False)
    aluno_id = Column(UUID(as_uuid=True), ForeignKey("alunos.id"), nullable=False)
    dados_utilizados = Column(Text, nullable=True)
    arquivo_path = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())