# Finance Manager

Sistema web genérico de gestão financeira para pequenas organizações, equipes e negócios. O projeto reúne lançamentos, aprovações, planejamento, contas, relatórios e auditoria em uma interface única.

> Esta versão foi adaptada a partir de um sistema real desenvolvido para uma organização. As regras, dados e nomenclaturas específicas do cliente foram removidas para transformar o projeto em uma demonstração reutilizável de portfólio.

## Principais recursos

- Dashboard executivo e visão restrita por departamento.
- Despesas com rascunho, itens, comprovantes protegidos e fluxo de aprovação.
- Receitas por categoria, anexos, observações e aprovação.
- Gastos fixos mensais com geração de despesa ao registrar pagamento.
- Orçamento mensal por departamento e acompanhamento de consumo.
- Contas financeiras com movimentação manual e saldo consolidado.
- Livro-caixa, relatórios mensais/anuais, calendário e trilha de auditoria.
- Exportação Excel e relatórios PDF.
- Importação XLSX com validação de formato, período e duplicidade.
- Busca global, alertas operacionais, tema claro/escuro e backup.

## Perfis

| Perfil | Acesso |
|---|---|
| Responsável de departamento | Dashboard e despesas do próprio departamento |
| Administrador financeiro | Operação financeira, primeira revisão e relatórios |
| Administrador máximo | Acesso total, aprovação final, usuários, departamentos e auditoria |

## Tecnologias

Python · Django · PostgreSQL · Bootstrap · Chart.js · OpenPyXL · ReportLab · Gunicorn · WhiteNoise

## Segurança

A edição pública não contém dados reais, anexos de clientes, chaves, credenciais ou identidade visual da implementação original. Variáveis sensíveis são fornecidas por ambiente.

## Desenvolvimento local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Objetivo

Projeto de portfólio para demonstrar arquitetura Django, autenticação e autorização, modelagem relacional, regras de negócio, relatórios, automações financeiras e dashboards administrativos.
