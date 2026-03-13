# Changelog

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

## [0.1.0] - 2026-03-13

### Adicionado
- Estrutura inicial do projeto
- Dockerfile (Python 3.12)
- docker-compose.yml (app + PostgreSQL + Adminer)
- FastAPI com rota GET / (health check)
- .env.example com todas as variáveis previstas
- .gitignore
- README.md com documentação da Fase 0
- docs/arquitetura.md com visão geral dos módulos
