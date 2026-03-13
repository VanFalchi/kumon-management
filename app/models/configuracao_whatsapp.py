import uuid
from sqlalchemy import Column, String, Boolean, Enum, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base

class ConfiguracaoWhatsapp(Base):
    __tablename__ = "configuracoes_whatsapp"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    provedor = Column(Enum('evolution_api', 'z_api', name='provedor_whatsapp'), nullable=False)
    api_url = Column(Text, nullable=True)
    api_key = Column(Text, nullable=True)
    numero_instancia = Column(Text, nullable=True)
    ativo = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())