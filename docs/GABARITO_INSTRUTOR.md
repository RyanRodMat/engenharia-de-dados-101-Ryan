# Gabarito do Instrutor

> ⚠️ Este arquivo é só para quem está aplicando a aula. Não compartilhe
> com os alunos antes do exercício — ele lista exatamente os problemas
> plantados nos dados e uma implementação de referência.

## Problemas plantados em `lakehouse/landing/vendas.csv`

(300 vendas originais + 8 duplicadas = 308 linhas)

- 45 linhas com `data_venda` em formato `DD/MM/AAAA` (resto em ISO).
- 30 linhas com `valor_total` usando vírgula decimal (`"179,80"`).
- 15 linhas com `quantidade` vazia.
- 15 linhas com `valor_total` vazio.
- 15 linhas com espaços extras em `data_venda`/`valor_total`.
- 5 linhas com `id_cliente = 9999` (cliente inexistente — órfão).
- 3 linhas com `quantidade = 0`.
- 8 linhas duplicadas (mesmo `id_venda` repetido, cópia exata).

## Problemas plantados em `lakehouse/landing/clientes.json`

(30 clientes originais + 2 duplicados conflitantes = 32 registros)

- 5 registros com `estado` bagunçado (minúsculo ou com espaços).
- 4 registros com `email` normalizável (maiúsculo ou com espaços).
- 2 registros com `email` **irrecuperável** (sem `@`) — devem ser
  descartados na silver.
- 3 registros sem a chave `data_cadastro` (ausente, não só vazia).
- 3 registros com `data_cadastro: null`.
- 2 registros com `id_cliente` como string em vez de número.
- 2 registros com campo extra `telefone` (schema drift).
- 2 registros duplicados: mesmo `id_cliente` de um registro existente,
  mas com `email` diferente (mais recente) — a regra é "o último no
  arquivo vence".

## Problemas plantados em `lakehouse/landing/produtos.txt`

(19 produtos originais + 2 duplicados = 21 linhas de dados)

- Comentários (`#`) e linhas em branco intercaladas — inclusive um bloco
  "lote 2" no meio do arquivo.
- 6 linhas com `categoria` fora do padrão (minúsculo, maiúsculo, com
  espaços, sem acento).
- 6 linhas com `preco` usando vírgula decimal.
- 5 linhas com `ativo` como `"sim"`/`"nao"` em vez de `"1"`/`"0"`.
- 2 linhas com `ativo` vazio (deve virar `0`/inativo).
- 4 linhas com `nome` com espaços extras nas pontas.
- 2 linhas duplicadas (mesmo `id_produto`, cópia exata).

## Implementação de referência

As soluções completas (usadas para validar os `verificar_*.py` antes de
entregar o projeto) não ficam neste repositório para não estragar o
exercício. Se precisar delas para corrigir alunos, você pode:

1. Preencher você mesmo `lakehouse/bronze/ingestao.py`,
   `lakehouse/silver/transformacao.py`, `lakehouse/gold/agregacao.py` e
   `application/etl_reverso.py` seguindo os `TODO`s e docstrings — eles
   já descrevem a lógica esperada em detalhe.
2. Rodar os `verificar_*.py` correspondentes para confirmar.

Números de referência (com a semente padrão `SEED = 7`), calculados com
uma implementação correta das regras da silver:

| Arquivo                | Linhas |
|--------------------------|--------|
| `clientes_silver.csv`   | 28     |
| `produtos_silver.csv`   | 19     |
| `vendas_silver.csv`     | 242    |

Se um aluno chegar a números bem diferentes desses, vale conferir se
alguma regra de descarte (e-mail inválido, referência órfã, quantidade
≤ 0, etc.) não foi implementada.
