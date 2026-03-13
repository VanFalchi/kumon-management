# Arquitetura do Sistema

## Módulos

| Módulo | Descrição |
|--------|-----------|
| Cadastros Base | Alunos, responsáveis, matrículas, mesas, horários |
| Contas a Receber | Cobranças, boletos, ciclo anual, carnê |
| Inadimplência | Régua de cobrança automática via WhatsApp |
| Contas a Pagar | Fixas recorrentes + lançamentos avulsos |
| Extrato | Importação e categorização automática via API Efi |
| Dashboard | Resumo financeiro do mês + alertas |
| Relatórios | DRE, extrato, inadimplência, previsto x realizado |
| Documentos PDF | Contratos e termos via templates |
| Fluxo de Caixa | Projeção dia a dia |
| Horários PDF | Grade mensal de chamada por mesa e slot |

## Integrações Externas

- **Efi Bank:** boletos Bolix, webhook de baixa automática, importação de extrato
- **WhatsApp (Z-API):** envio de boletos e régua de cobrança
- **Cloudflare Tunnel:** HTTPS automático sem IP fixo

## Banco de Dados

PostgreSQL 16 com UUID como primary key em todas as tabelas.
Migrations gerenciadas via Alembic.

Consulte o documento de especificação completo para o schema detalhado.
