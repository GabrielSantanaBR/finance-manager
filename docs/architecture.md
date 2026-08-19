# Arquitetura

O Finance Manager segue uma arquitetura Django modular. Cada domínio possui models, forms, views e rotas próprias.

## Domínios

- `accounts`: autenticação, perfis e autorização.
- `ministries`: nome técnico legado para departamentos/centros de responsabilidade.
- `expenses`: despesas, itens, comprovantes e estados de aprovação.
- `revenues`: receitas e workflow de revisão.
- `fixed_expenses`: recorrências mensais.
- `treasury`: contas financeiras e movimentações.
- `reports`: relatórios PDF, livro-caixa e consolidações.
- `exports`: importação/exportação XLSX.
- `dashboard`: indicadores e gráficos.
- `core`: auditoria, segurança, validações e serviços compartilhados.

A nomenclatura técnica `ministry` foi preservada em pontos internos para compatibilidade histórica do schema, mas a edição pública representa o conceito como **departamento**.

## Segurança

Arquivos enviados passam por validação de extensão, tamanho e assinatura. A aplicação ativa HTTPS, cookies seguros, HSTS, CSRF e cabeçalhos de segurança em produção. Segredos e conexões ficam exclusivamente em variáveis de ambiente.
