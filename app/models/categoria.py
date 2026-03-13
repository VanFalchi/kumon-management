import uuid
from sqlalchemy import Column, String, Boolean, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base

class CategoriaFinanceira(Base):
    __tablename__ = "categorias_financeiras"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String(100), nullable=False)
    tipo = Column(Enum('receita', 'despesa', name='tipo_categoria'), nullable=False)
    cor = Column(String(7), nullable=True)
    eh_retirada_pessoal = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())