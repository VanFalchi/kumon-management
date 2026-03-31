from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from decimal import Decimal
from datetime import date

from app.database import get_db
from app.models.cobranca import Cobranca
from app.models.cobranca_materia import CobrancaMateria
from app.models.matricula import Matricula
from app.models.responsavel import Responsavel
from app.schemas.cobranca import CobrancaCreate, CobrancaUpdate, CobrancaResponse
from app.services.efi_service import gerar_boleto_bolix

router = APIRouter(prefix="/cobrancas", tags=["Cobranças"])


@router.get("/", response_model=List[CobrancaResponse])
def listar_cobranças(db: Session = Depends(get_db)):
    return db.query(Cobranca).all()


@router.get("/aluno/{aluno_id}", response_model=List[CobrancaResponse])
def listar_cobranças_aluno(aluno_id: UUID, db: Session = Depends(get_db)):
    return db.query(Cobranca).filter(Cobranca.aluno_id == aluno_id).all()


@router.get("/pendentes", response_model=List[CobrancaResponse])
def listar_pendentes(db: Session = Depends(get_db)):
    return db.query(Cobranca).filter(
        Cobranca.status.in_(["pendente", "inadimplente"])
    ).all()


@router.get("/{cobranca_id}", response_model=CobrancaResponse)
def buscar_cobrança(cobranca_id: UUID, db: Session = Depends(get_db)):
    cobranca = db.query(Cobranca).filter(Cobranca.id == cobranca_id).first()
    if not cobranca:
        raise HTTPException(status_code=404, detail="Cobrança não encontrada")
    return cobranca


@router.post("/", response_model=CobrancaResponse, status_code=status.HTTP_201_CREATED)
def criar_cobrança(cobranca: CobrancaCreate, db: Session = Depends(get_db)):
    valor_cheio = round(cobranca.valor_real / Decimal("0.90"), 2)

    db_cobranca = Cobranca(
        aluno_id=cobranca.aluno_id,
        responsavel_id=cobranca.responsavel_id,
        mes_referencia=cobranca.mes_referencia,
        tipo=cobranca.tipo,
        valor_real=cobranca.valor_real,
        valor_cheio=valor_cheio,
        data_vencimento=cobranca.data_vencimento,
        ciclo_ano=cobranca.ciclo_ano,
        observacoes=cobranca.observacoes,
        status="pendente"
    )
    db.add(db_cobranca)
    db.flush()

    for mat in cobranca.materias:
        db_mat = CobrancaMateria(
            cobranca_id=db_cobranca.id,
            matricula_id=mat.matricula_id,
            valor_real_materia=mat.valor_real_materia
        )
        db.add(db_mat)

    db.commit()
    db.refresh(db_cobranca)
    return db_cobranca


@router.post("/{cobranca_id}/emitir-boleto")
def emitir_boleto(cobranca_id: UUID, db: Session = Depends(get_db)):
    cobranca = db.query(Cobranca).filter(Cobranca.id == cobranca_id).first()
    if not cobranca:
        raise HTTPException(status_code=404, detail="Cobrança não encontrada")

    if cobranca.status == "boleto_emitido":
        raise HTTPException(status_code=400, detail="Boleto já emitido para esta cobrança")

    if cobranca.status == "paga":
        raise HTTPException(status_code=400, detail="Cobrança já está paga")

    responsavel = db.query(Responsavel).filter(
        Responsavel.id == cobranca.responsavel_id
    ).first()

    resultado = gerar_boleto_bolix(
        charge_id_interno=str(cobranca.id),
        valor_cheio=float(cobranca.valor_cheio),
        valor_real=float(cobranca.valor_real),
        data_vencimento=cobranca.data_vencimento.strftime("%Y-%m-%d"),
        nome_responsavel=responsavel.nome,
        cpf_responsavel=responsavel.cpf or "00000000000",
        descricao=f"Mensalidade Kumon - {cobranca.mes_referencia.strftime('%m/%Y')}"
    )

    if "txid" not in resultado:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar boleto: {resultado}")

    cobranca.efi_charge_id = resultado["txid"]
    cobranca.efi_pix_link = resultado.get("pixCopiaECola")
    cobranca.status = "boleto_emitido"
    db.commit()
    db.refresh(cobranca)

    return {
        "mensagem": "Boleto emitido com sucesso",
        "txid": resultado["txid"],
        "pix_copia_cola": resultado.get("pixCopiaECola"),
        "cobranca_id": str(cobranca.id)
    }


@router.put("/{cobranca_id}", response_model=CobrancaResponse)
def atualizar_cobrança(cobranca_id: UUID, cobranca: CobrancaUpdate, db: Session = Depends(get_db)):
    db_cobranca = db.query(Cobranca).filter(Cobranca.id == cobranca_id).first()
    if not db_cobranca:
        raise HTTPException(status_code=404, detail="Cobrança não encontrada")

    dados = cobranca.model_dump(exclude_unset=True)
    if "valor_real" in dados:
        dados["valor_cheio"] = round(dados["valor_real"] / Decimal("0.90"), 2)

    for campo, valor in dados.items():
        setattr(db_cobranca, campo, valor)

    db.commit()
    db.refresh(db_cobranca)
    return db_cobranca


@router.post("/{cobranca_id}/baixa-manual")
def baixa_manual(cobranca_id: UUID, db: Session = Depends(get_db)):
    cobranca = db.query(Cobranca).filter(Cobranca.id == cobranca_id).first()
    if not cobranca:
        raise HTTPException(status_code=404, detail="Cobrança não encontrada")

    cobranca.status = "paga"
    cobranca.data_pagamento = date.today()
    cobranca.forma_pagamento = "dinheiro"
    cobranca.valor_pago = cobranca.valor_real
    db.commit()

    return {"mensagem": "Baixa manual registrada com sucesso"}


@router.delete("/{cobranca_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancelar_cobrança(cobranca_id: UUID, db: Session = Depends(get_db)):
    cobranca = db.query(Cobranca).filter(Cobranca.id == cobranca_id).first()
    if not cobranca:
        raise HTTPException(status_code=404, detail="Cobrança não encontrada")
    cobranca.status = "cancelada"
    db.commit()