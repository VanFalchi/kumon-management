import uuid
from sqlalchemy import Column, String, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base

class Responsavel(Base):
    __tablename__ = "responsaveis"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String(150), nullable=False)
    cpf = Column(String(14), unique=True, nullable=True)
    telefone_whatsapp = Column(String(20), nullable=False)
    email = Column(String(150), nullable=True)
    endereco = Column(String(300), nullable=True)
    profissao = Column(String(150), nullable=True)
    empresa = Column(String(150), nullable=True)
    preferencia_boleto = Column(Enum('digital', 'impresso', name='preferencia_boleto'), default='digital')
    created_at = Column(DateTime(timezone=True), server_default=func.now())