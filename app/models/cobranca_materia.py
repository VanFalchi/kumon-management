import uuid
from sqlalchemy import Column, Numeric, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base

class CobrancaMateria(Base):
    __tablename__ = "cobranças_materias"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cobranca_id = Column(UUID(as_uuid=True), ForeignKey("cobranças.id"), nullable=False)
    matricula_id = Column(UUID(as_uuid=True), ForeignKey("matriculas.id"), nullable=False)
    valor_real_materia = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())