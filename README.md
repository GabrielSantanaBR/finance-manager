# Finance Manager

Sistema web genérico de gestão financeira para pequenas organizações, equipes e negócios. A base pública demonstra modelagem de receitas, despesas, departamentos, contas, gastos recorrentes, auditoria, autenticação e regras de aprovação.

> Esta versão foi adaptada a partir de um sistema real. Dados, anexos, identidade visual e regras específicas do cliente foram removidos antes da publicação.

## Domínios demonstrados

- Usuários com perfis de administrador financeiro e responsável de departamento.
- Despesas com itens, comprovantes, categorias e estados de aprovação.
- Receitas categorizadas e workflow de revisão.
- Gastos fixos e pagamentos por competência.
- Orçamentos por departamento.
- Contas financeiras e movimentações.
- Auditoria de ações administrativas.
- Validação de documentos por extensão, tamanho e assinatura do arquivo.
- Configuração segura para PostgreSQL e ambientes de produção.

## Edição pública

A implementação privada que originou este case possui fluxos operacionais, relatórios e telas adicionais. Neste repositório público, a camada de domínio e segurança foi preservada e a interface foi reduzida a uma demonstração genérica para não expor particularidades do cliente.

O nome técnico `ministries` permanece em alguns pontos do schema por compatibilidade histórica; na versão genérica ele representa **departamentos/centros de responsabilidade**.

## Tecnologias

Python · Django · PostgreSQL · Bootstrap · OpenPyXL · ReportLab · Gunicorn · WhiteNoise

## Desenvolvimento local

Requer Python 3.12+.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Para desenvolvimento local, ajuste `.env` para `DEBUG=True` e então gere o schema da edição pública:

```bash
python manage.py makemigrations accounts core ministries expenses revenues fixed_expenses treasury
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

A aplicação ficará disponível em `http://127.0.0.1:8000/` e o health check em `/health/`.

## Segurança

- Nenhuma credencial ou chave real é versionada.
- Arquivos enviados são validados antes da persistência.
- `DEBUG` fica desligado por padrão.
- HTTPS, HSTS, cookies seguros, CSRF e cabeçalhos de segurança são ativados em produção.
- Configuração de banco, hosts e segredos é fornecida por variáveis de ambiente.

## Arquitetura

Veja [`docs/architecture.md`](docs/architecture.md) para a divisão dos módulos e decisões de compatibilidade.

## Objetivo

Projeto de portfólio para demonstrar arquitetura Django, autenticação e autorização, modelagem relacional, regras de negócio, segurança de uploads e construção de sistemas administrativos orientados a dados.
