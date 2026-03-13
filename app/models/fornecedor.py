import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base

class Fornecedor(Base):
    __tablename__ = "fornecedores"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String(150), nullable=False)
    cnpj = Column(String(18), nullable=True)
    categoria_padrao_id = Column(UUID(as_uuid=True), ForeignKey("categorias_financeiras.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())