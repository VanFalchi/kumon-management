from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from uuid import UUID
from decimal import Decimal

class CobrancaMateriaSchema(BaseModel):
    matricula_id: UUID
    valor_real_materia: Decimal

class CobrancaCreate(BaseModel):
    aluno_id: UUID
    responsavel_id: UUID
    mes_referencia: date
    tipo: str = "mensalidade"
    valor_real: Decimal
    data_vencimento: date
    ciclo_ano: Optional[int] = None
    observacoes: Optional[str] = None
    materias: Optional[List[CobrancaMateriaSchema]] = []

class CobrancaUpdate(BaseModel):
    valor_real: Optional[Decimal] = None
    data_vencimento: Optional[date] = None
    observacoes: Optional[str] = None
    status: Optional[str] = None

class CobrancaResponse(BaseModel):
    id: UUID
    aluno_id: UUID
    responsavel_id: UUID
    mes_referencia: date
    tipo: str
    valor_real: Decimal
    valor_cheio: Decimal
    data_vencimento: date
    status: str
    ciclo_ano: Optional[int] = None
    observacoes: Optional[str] = None
    data_pagamento: Optional[date] = None
    valor_pago: Optional[Decimal] = None
    forma_pagamento: Optional[str] = None
    efi_charge_id: Optional[str] = None
    efi_pix_link: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True