from sqlalchemy.orm import Session
from datetime import date
from dateutil.relativedelta import relativedelta
from decimal import Decimal
from app.database import SessionLocal
from app.models.cobranca import Cobranca
from app.models.responsavel import Responsavel
from app.models.aluno import Aluno
from app.services.efi_service import gerar_boleto_bolix


def gerar_carne(
    aluno_id: str,
    responsavel_id: str,
    mes_inicio: date,
    mes_fim: date,
    db: Session
):
    """
    Gera boletos em lote para impressão (carnê).
    Emite todos os boletos do range de meses de uma vez na Efi.
    Retorna lista de cobranças com boletos emitidos.
    """
    responsavel = db.query(Responsavel).filter(
        Responsavel.id == responsavel_id
    ).first()

    aluno = db.query(Aluno).filter(
        Aluno.id == aluno_id
    ).first()

    if not responsavel or not aluno:
        raise ValueError("Aluno ou responsável não encontrado")

    # Busca cobranças pendentes no range de meses
    cobranças_range = []
    mes_atual = mes_inicio
    while mes_atual <= mes_fim:
        cobranca = db.query(Cobranca).filter(
            Cobranca.aluno_id == aluno_id,
            Cobranca.mes_referencia == mes_atual,
            Cobranca.tipo == "mensalidade",
            Cobranca.status == "pendente"
        ).first()

        if cobranca:
            cobranças_range.append(cobranca)

        mes_atual = mes_atual + relativedelta(months=1)

    if not cobranças_range:
        raise ValueError("Nenhuma cobrança pendente encontrada no período informado")

    # Emite todos os boletos na Efi
    emitidos = []
    erros = []

    for cobranca in cobranças_range:
        try:
            resultado = gerar_boleto_bolix(
                charge_id_interno=str(cobranca.id),
                valor_cheio=float(cobranca.valor_cheio),
                valor_real=float(cobranca.valor_real),
                data_vencimento=cobranca.data_vencimento.strftime("%Y-%m-%d"),
                nome_responsavel=responsavel.nome,
                cpf_responsavel=responsavel.cpf or "00000000000",
                descricao=f"Mensalidade Kumon - {cobranca.mes_referencia.strftime('%m/%Y')}"
            )

            if "txid" in resultado:
                cobranca.efi_charge_id = resultado["txid"]
                cobranca.efi_pix_link = resultado.get("pixCopiaECola")
                cobranca.status = "boleto_emitido"
                emitidos.append({
                    "mes": cobranca.mes_referencia.strftime("%m/%Y"),
                    "vencimento": cobranca.data_vencimento.strftime("%d/%m/%Y"),
                    "valor_real": float(cobranca.valor_real),
                    "valor_cheio": float(cobranca.valor_cheio),
                    "pix_copia_cola": resultado.get("pixCopiaECola"),
                    "txid": resultado["txid"]
                })
            else:
                erros.append(cobranca.mes_referencia.strftime("%m/%Y"))

        except Exception as e:
            erros.append(f"{cobranca.mes_referencia.strftime('%m/%Y')}: {str(e)}")

    db.commit()

    return {
        "aluno": aluno.nome,
        "responsavel": responsavel.nome,
        "total_emitidos": len(emitidos),
        "total_erros": len(erros),
        "boletos": emitidos,
        "erros": erros
    }
