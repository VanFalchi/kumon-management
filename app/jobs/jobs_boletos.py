from sqlalchemy.orm import Session
from datetime import date, timedelta
from app.database import SessionLocal
from app.models.cobranca import Cobranca
from app.models.responsavel import Responsavel
from app.services.efi_service import gerar_boleto_bolix


def emitir_boletos_digitais():
    """
    Job que roda todo dia às 08:00.
    Emite boletos para cobranças com vencimento nos próximos 5 dias
    que ainda não têm boleto emitido.
    Só emite para responsáveis com preferencia_boleto = 'digital'.
    """
    db: Session = SessionLocal()
    hoje = date.today()

    try:
        limite = hoje + timedelta(days=5)

        cobranças_pendentes = db.query(Cobranca).filter(
            Cobranca.status == "pendente",
            Cobranca.data_vencimento >= hoje,
            Cobranca.data_vencimento <= limite
        ).all()

        emitidos = 0
        erros = 0

        for cobranca in cobranças_pendentes:
            responsavel = db.query(Responsavel).filter(
                Responsavel.id == cobranca.responsavel_id
            ).first()

            if not responsavel or responsavel.preferencia_boleto != "digital":
                continue

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
                    emitidos += 1
                else:
                    erros += 1

            except Exception as e:
                print(f"Erro ao emitir boleto cobrança {cobranca.id}: {e}")
                erros += 1

        db.commit()
        print(f"Job emissão boletos: {emitidos} emitidos, {erros} erros")

    except Exception as e:
        db.rollback()
        print(f"Erro no job de emissão de boletos: {e}")
    finally:
        db.close()


def verificar_inadimplencia():
    """
    Job que roda todo dia às 09:00.
    Atualiza cobranças vencidas sem pagamento para status inadimplente.
    """
    db: Session = SessionLocal()
    hoje = date.today()

    try:
        cobranças_vencidas = db.query(Cobranca).filter(
            Cobranca.data_vencimento < hoje,
            Cobranca.status == "boleto_emitido"
        ).all()

        atualizadas = 0
        for cobranca in cobranças_vencidas:
            cobranca.status = "inadimplente"
            atualizadas += 1

        db.commit()
        print(f"Job inadimplência: {atualizadas} atualizadas para inadimplente")

    except Exception as e:
        db.rollback()
        print(f"Erro no job de inadimplência: {e}")
    finally:
        db.close()