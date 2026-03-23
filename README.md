# Kumon Management

Sistema de gestão de unidade para franquia Kumon. 

## Stack

- **Backend:** Python 3.12 + FastAPI
- **Banco de dados:** PostgreSQL 16
- **Frontend:** HTMX + Alpine.js + Jinja2 + Tailwind CSS
- **Jobs:** APScheduler
- **PDF:** WeasyPrint
- **Integrações:** Efi Bank (boletos + extrato) + WhatsApp (Z-API)
- **Infra:** Docker + Docker Compose + Cloudflare Tunnel

## Pré-requisitos

- Windows 11 com WSL2 (Ubuntu 22.04+)
- Docker Desktop com integração WSL2 ativa
- Python 3.12 (dentro do WSL2)
- VS Code com extensão Remote Development

## Setup local
```bash
# 1. Clonar o repositório (dentro do WSL2)
git clone git@github.com:VanFalchi/kumon-management.git
cd kumon-management

# 2. Copiar e configurar variáveis de ambiente
cp .env.example .env
# editar o .env com suas credenciais

# 3. Subir os containers
docker compose up --build

# 4. Acessar
# API:     http://localhost:8000
# Docs:    http://localhost:8000/docs
# Adminer: http://localhost:8080
```

## Fases do Projeto

| Fase | Nome | Status |
|------|------|--------|
| 0 | Planejamento e estrutura inicial | ✅ Concluída |
| 1 | Setup: FastAPI + PostgreSQL + Docker + JWT | ✅ Concluída |
| 2 | Models e migrations (Alembic) | ✅ Concluída |
| 3 | CRUDs: alunos, responsáveis, matrículas | ✅ Concluída |
| 4 | Integração Efi Bank | 🔄 Próxima |
| 5 | Cobranças e boletos | ⏳ Backlog |
| 6 | Inadimplência e régua de cobrança | ⏳ Backlog |
| 7 | Importação de extrato Efi | ⏳ Backlog |
| 8 | Migração de dados do Kaits | ⏳ Backlog |
| 9 | Contas a pagar | ⏳ Backlog |
| 10 | Dashboard | ⏳ Backlog |
| 11 | Relatórios | ⏳ Backlog |
| 12 | Geração de documentos PDF | ⏳ Backlog |
| 13 | Projeção de fluxo de caixa | ⏳ Backlog |
| 14 | Grade de horários PDF | ⏳ Backlog |

## Changelog

## [0.4.0] - 2026-03-23

### Adicionado
- Schemas Pydantic para alunos, responsáveis, matrículas, matérias, mesas, slots e horários
- CRUD completo: alunos, responsáveis, matérias, matrículas
- CRUD completo: mesas, slots de horário, horários dos alunos
- Endpoint de verificação de vagas por mesa + slot em tempo real
- Validação automática de capacidade ao alocar aluno em horário

## [0.3.0] - 2026-03-13

### Adicionado
- 18 models SQLAlchemy (alunos, responsáveis, matrículas, mesas, slots, horários, cobranças, lançamentos, categorias, fornecedores, contas fixas, documentos, WhatsApp log)
- Migration Alembic criando todas as tabelas no PostgreSQL
- Enum types para status, tipos e categorias

## [0.2.0] - 2026-03-13

### Adicionado
- Configuração do Alembic para migrations
- Conexão com PostgreSQL via SQLAlchemy (app/database.py)
- Autenticação JWT (app/auth.py)
- Rota POST /auth/token com login por usuário temporário
- bcrypt para hash de senhas

### v0.1.0 — Fase 0 (Março 2026)
- Estrutura inicial do projeto
- Dockerfile e docker-compose configurados
- FastAPI com rota de health check
- Documentação base (README, .env.example)
