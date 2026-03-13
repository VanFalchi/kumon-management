import uuid
from sqlalchemy import Column, String, Enum, DateTime, Numeric, Date, Text, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base

class Cobranca(Base):
    __tablename__ = "cobranças"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    aluno_id = Column(UUID(as_uuid=True), ForeignKey("alunos.id"), nullable=False)
    responsavel_id = Column(UUID(as_uuid=True), ForeignKey("responsaveis.id"), nullable=False)
    mes_referencia = Column(Date, nullable=False)
    tipo = Column(Enum('mensalidade', 'matricula', 'rescisao', name='tipo_cobranca'), nullable=False)
    valor_real = Column(Numeric(10, 2), nullable=False)
    valor_cheio = Column(Numeric(10, 2), nullable=False)
    data_vencimento = Column(Date, nullable=False)
    status = Column(Enum('pendente', 'boleto_emitido', 'paga', 'inadimplente', 'cancelada', name='status_cobranca'), default='pendente')
    ciclo_ano = Column(Integer, nullable=True)
    observacoes = Column(Text, nullable=True)
    data_pagamento = Column(Date, nullable=True)
    valor_pago = Column(Numeric(10, 2), nullable=True)
    forma_pagamento = Column(Enum('boleto', 'dinheiro', name='forma_pagamento'), nullable=True)
    efi_charge_id = Column(String(100), nullable=True)
    efi_pix_link = Column(Text, nullable=True)
    efi_boleto_pdf = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())