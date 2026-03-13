import uuid
from sqlalchemy import Column, String, Boolean, Date, DateTime, Numeric, Integer, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base

class ContaFixa(Base):
    __tablename__ = "contas_fixas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    descricao = Column(String(200), nullable=False)
    valor = Column(Numeric(10, 2), nullable=False)
    dia_vencimento = Column(Integer, nullable=False)
    frequencia = Column(Enum('mensal', 'bimestral', 'trimestral', 'semestral', 'anual', name='frequencia_conta'), nullable=False)
    categoria_id = Column(UUID(as_uuid=True), ForeignKey("categorias_financeiras.id"), nullable=True)
    fornecedor_id = Column(UUID(as_uuid=True), ForeignKey("fornecedores.id"), nullable=True)
    ativa = Column(Boolean, default=True)
    data_inicio = Column(Date, nullable=False)
    data_fim = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())