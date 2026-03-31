from fastapi import APIRouter, Request, HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends
from app.database import get_db
from app.models.cobranca import Cobranca
from datetime import date
import os
import hmac
import hashlib

router = APIRouter(prefix="/webhook", tags=["Webhook"])

@router.post("/efi/pagamento")
async def webhook_efi(request: Request, db: Session = Depends(get_db)):
    # Lê o payload
    payload = await request.json()
    
    # Verifica se é uma notificação de pagamento Pix
    if "pix" not in payload:
        return {"status": "ignored"}

    for pix in payload["pix"]:
        txid = pix.get("txid")
        valor_pago = float(pix.get("valor", 0))
        horario_pagamento = pix.get("horario")

        if not txid:
            continue

        # Busca a cobrança pelo efi_charge_id
        cobranca = db.query(Cobranca).filter(
            Cobranca.efi_charge_id == txid
        ).first()

        if not cobranca:
            continue

        # Evita processar duas vezes (idempotência)
        if cobranca.status == "paga":
            continue

        # Atualiza a cobrança
        cobranca.status = "paga"
        cobranca.data_pagamento = date.today()
        cobranca.valor_pago = valor_pago
        cobranca.forma_pagamento = "boleto"
        db.commit()

    return {"status": "ok"}