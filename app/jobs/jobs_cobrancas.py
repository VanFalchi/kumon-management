from sqlalchemy.orm import Session
from datetime import date
from decimal import Decimal
import calendar
from app.database import SessionLocal
from app.models.aluno import Aluno
from app.models.matricula import Matricula
from app.models.aluno_responsavel import AlunoResponsavel
from app.models.cobranca import Cobranca
from app.models.cobranca_materia import CobrancaMateria


def gerar_cobranças_mensais():
    """
    Job que roda todo dia 1 do mês às 06:00.
    Gera cobranças para todos os alunos ativos com matrículas ativas.
    Não gera duplicatas se já existir cobrança para o mês.
    """
    db: Session = SessionLocal()
    hoje = date.today()
    mes_referencia = date(hoje.year, hoje.month, 1)
    dia_vencimento = 10

    try:
        alunos = db.query(Aluno).filter(Aluno.status == "ativo").all()
        geradas = 0
        ignoradas = 0

        for aluno in alunos:
            matriculas_ativas = db.query(Matricula).filter(
                Matricula.aluno_id == aluno.id,
                Matricula.data_fim == None
            ).all()

            if not matriculas_ativas:
                continue

            vinculo = db.query(AlunoResponsavel).filter(
                AlunoResponsavel.aluno_id == aluno.id,
                AlunoResponsavel.responsavel_financeiro == True
            ).first()

            if not vinculo:
                continue

            existente = db.query(Cobranca).filter(
                Cobranca.aluno_id == aluno.id,
                Cobranca.mes_referencia == mes_referencia,
                Cobranca.tipo == "mensalidade",
                Cobranca.status != "cancelada"
            ).first()

            if existente:
                ignoradas += 1
                continue

            valor_real_total = sum(m.valor_real for m in matriculas_ativas)
            valor_cheio = round(valor_real_total / Decimal("0.90"), 2)
            data_vencimento = date(hoje.year, hoje.month, dia_vencimento)

            cobranca = Cobranca(
                aluno_id=aluno.id,
                responsavel_id=vinculo.responsavel_id,
                mes_referencia=mes_referencia,
                tipo="mensalidade",
                valor_real=valor_real_total,
                valor_cheio=valor_cheio,
                data_vencimento=data_vencimento,
                ciclo_ano=hoje.year,
                status="pendente"
            )
            db.add(cobranca)
            db.flush()

            for matricula in matriculas_ativas:
                detalhe = CobrancaMateria(
                    cobranca_id=cobranca.id,
                    matricula_id=matricula.id,
                    valor_real_materia=matricula.valor_real
                )
                db.add(detalhe)

            geradas += 1

        db.commit()
        print(f"Job cobranças mensais: {geradas} geradas, {ignoradas} ignoradas")

    except Exception as e:
        db.rollback()
        print(f"Erro no job de cobranças mensais: {e}")
    finally:
        db.close()


def gerar_cobranças_ciclo_anual(ciclo_ano: int, dia_vencimento: int = 10):
    """
    Gera cobranças do ciclo anual (outubro a setembro) para todos os alunos ativos.
    Chamado manualmente pelo usuário em outubro de cada ano.
    ciclo_ano: ex: 2026 = ciclo out/2026 a set/2027
    """
    db: Session = SessionLocal()

    try:
        meses = []
        for mes in range(10, 13):
            meses.append((ciclo_ano, mes))
        for mes in range(1, 10):
            meses.append((ciclo_ano + 1, mes))

        alunos = db.query(Aluno).filter(Aluno.status == "ativo").all()
        geradas = 0
        ignoradas = 0

        for aluno in alunos:
            matriculas_ativas = db.query(Matricula).filter(
                Matricula.aluno_id == aluno.id,
                Matricula.data_fim == None
            ).all()

            if not matriculas_ativas:
                continue

            vinculo = db.query(AlunoResponsavel).filter(
                AlunoResponsavel.aluno_id == aluno.id,
                AlunoResponsavel.responsavel_financeiro == True
            ).first()

            if not vinculo:
                continue

            valor_real_total = sum(m.valor_real for m in matriculas_ativas)
            valor_cheio = round(valor_real_total / Decimal("0.90"), 2)

            for ano, mes in meses:
                mes_referencia = date(ano, mes, 1)

                existente = db.query(Cobranca).filter(
                    Cobranca.aluno_id == aluno.id,
                    Cobranca.mes_referencia == mes_referencia,
                    Cobranca.tipo == "mensalidade",
                    Cobranca.status != "cancelada"
                ).first()

                if existente:
                    ignoradas += 1
                    continue

                ultimo_dia = calendar.monthrange(ano, mes)[1]
                dia = min(dia_vencimento, ultimo_dia)
                data_vencimento = date(ano, mes, dia)

                cobranca = Cobranca(
                    aluno_id=aluno.id,
                    responsavel_id=vinculo.responsavel_id,
                    mes_referencia=mes_referencia,
                    tipo="mensalidade",
                    valor_real=valor_real_total,
                    valor_cheio=valor_cheio,
                    data_vencimento=data_vencimento,
                    ciclo_ano=ciclo_ano,
                    status="pendente"
                )
                db.add(cobranca)
                db.flush()

                for matricula in matriculas_ativas:
                    detalhe = CobrancaMateria(
                        cobranca_id=cobranca.id,
                        matricula_id=matricula.id,
                        valor_real_materia=matricula.valor_real
                    )
                    db.add(detalhe)

                geradas += 1

        db.commit()
        print(f"Ciclo anual {ciclo_ano}: {geradas} cobranças geradas, {ignoradas} ignoradas")
        return {"geradas": geradas, "ignoradas": ignoradas}

    except Exception as e:
        db.rollback()
        print(f"Erro ao gerar ciclo anual: {e}")
        raise
    finally:
        db.close()