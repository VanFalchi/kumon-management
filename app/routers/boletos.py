from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import date

from app.database import get_db
from app.models.cobranca import Cobranca
from app.models.responsavel import Responsavel
from app.models.aluno import Aluno
from app.services.efi_service import consultar_boleto

router = APIRouter(prefix="/boletos", tags=["Boletos"])


@router.get("/{txid}")
def consultar(txid: str):
    """Consulta o status de um boleto na Efi pelo txid."""
    return consultar_boleto(txid)


@router.post("/carne")
def gerar_carne(
    aluno_id: UUID,
    responsavel_id: UUID,
    mes_inicio: date,
    mes_fim: date,
    db: Session = Depends(get_db)
):
    """
    Gera boletos em lote para impressão (carnê).
    Emite todos os boletos do range de meses de uma vez na Efi.
    """
    from app.services.carne_service import gerar_carne
    try:
        resultado = gerar_carne(
            aluno_id=str(aluno_id),
            responsavel_id=str(responsavel_id),
            mes_inicio=mes_inicio,
            mes_fim=mes_fim,
            db=db
        )
        return resultado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar carnê: {str(e)}")