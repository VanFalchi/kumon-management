import uuid
from sqlalchemy import Column, String, Enum, DateTime, Numeric, Date, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base

class Lancamento(Base):
    __tablename__ = "lancamentos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    data = Column(Date, nullable=False)
    descricao = Column(String(200), nullable=False)
    valor = Column(Numeric(10, 2), nullable=False)
    tipo = Column(Enum('entrada', 'saida', name='tipo_lancamento'), nullable=False)
    categoria_id = Column(UUID(as_uuid=True), ForeignKey("categorias_financeiras.id"), nullable=True)
    status = Column(Enum('previsto', 'confirmado', 'cancelado', name='status_lancamento'), default='confirmado')
    origem = Column(Enum('manual', 'importacao_extrato', 'mensalidade', 'conta_fixa', name='origem_lancamento'), nullable=False)
    efi_transacao_id = Column(String(100), nullable=True)
    observacoes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())