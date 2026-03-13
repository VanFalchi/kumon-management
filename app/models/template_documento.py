import uuid
from sqlalchemy import Column, String, Boolean, Enum, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base

class TemplateDocumento(Base):
    __tablename__ = "templates_documentos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String(100), nullable=False)
    tipo = Column(Enum('contrato_matricula', 'termo_rescisao', 'outro', name='tipo_template'), nullable=False)
    conteudo_html = Column(Text, nullable=False)
    variaveis_disponiveis = Column(Text, nullable=True)
    ativo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())