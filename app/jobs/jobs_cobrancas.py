from sqlalchemy.orm import Session
from datetime import date
from decimal import Decimal
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
    dia_vencimento = 10  # todo dia 10

    try:
        # Busca todos os alunos ativos
        alunos = db.query(Aluno).filter(Aluno.status == "ativo").all()

        geradas = 0
        ignoradas = 0

        for aluno in alunos:
            # Busca matrículas ativas do aluno
            matriculas_ativas = db.query(Matricula).filter(
                Matricula.aluno_id == aluno.id,
                Matricula.data_fim == None
            ).all()

            if not matriculas_ativas:
                continue

            # Busca responsável financeiro
            vinculo = db.query(AlunoResponsavel).filter(
                AlunoResponsavel.aluno_id == aluno.id,
                AlunoResponsavel.responsavel_financeiro == True
            ).first()

            if not vinculo:
                continue

            # Verifica se já existe cobrança para este mês
            cobranca_existente = db.query(Cobranca).filter(
                Cobranca.aluno_id == aluno.id,
                Cobranca.mes_referencia == mes_referencia,
                Cobranca.tipo == "mensalidade",
                Cobranca.status != "cancelada"
            ).first()

            if cobranca_existente:
                ignoradas += 1
                continue

            # Calcula valor total das matrículas ativas
            valor_real_total = sum(m.valor_real for m in matriculas_ativas)
            valor_cheio = round(valor_real_total / Decimal("0.90"), 2)
            data_vencimento = date(hoje.year, hoje.month, dia_vencimento)

            # Cria a cobrança
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

            # Registra detalhamento por matéria
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