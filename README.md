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
| 1 | Setup: FastAPI + PostgreSQL + Docker + JWT | 🔄 Próxima |
| 2 | Models e migrations (Alembic) | ⏳ Backlog |
| 3 | CRUDs: alunos, responsáveis, matrículas | ⏳ Backlog |
| 4 | Integração Efi Bank | ⏳ Backlog |
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

### v0.1.0 — Fase 0 (Março 2026)
- Estrutura inicial do projeto
- Dockerfile e docker-compose configurados
- FastAPI com rota de health check
- Documentação base (README, .env.example)
