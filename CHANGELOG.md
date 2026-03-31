# Changelog

## [0.7.0] - 2026-03-31

### Adicionado
- Schema e router de cobranças (CRUD completo)
- Endpoint POST /cobrancas/{id}/emitir-boleto — integrado com Efi Bank
- Endpoint POST /cobrancas/{id}/baixa-manual — para pagamentos em dinheiro
- Job de geração automática de cobranças mensais (dia 1, 06:00)
- APScheduler integrado ao ciclo de vida do FastAPI
- Renomeação de arquivos para evitar problemas com caracteres especiais

## [0.6.0] - 2026-03-31

### Adicionado
- Integração com API Efi Bank (Pix cobv)
- Serviço de geração de boleto Bolix com desconto de 10%
- Serviço de cancelamento e consulta de boleto
- Endpoint webhook POST /webhook/efi/pagamento com idempotência
- Certificados SSL configurados para homologação

## [0.5.0] - 2026-03-31

### Adicionado
- Cloudflare Tunnel configurado (kumon-management)
- Domínio www.kumonjales.com.br com HTTPS automático
- Arquivo cloudflare/config.yml com configuração do túnel

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
