import uuid
from sqlalchemy import Column, String, Enum, Text, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base

class MensagemLog(Base):
    __tablename__ = "mensagens_whatsapp_log"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    responsavel_id = Column(UUID(as_uuid=True), ForeignKey("responsaveis.id"), nullable=False)
    cobranca_id = Column(UUID(as_uuid=True), ForeignKey("cobranças.id"), nullable=True)
    tipo = Column(Enum('boleto_preventivo', 'cobranca_d1', 'cobranca_d7', 'cobranca_d15', name='tipo_mensagem'), nullable=False)
    status = Column(Enum('enviado', 'erro', name='status_mensagem'), nullable=False)
    erro_detalhes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())