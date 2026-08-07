"""
dev_criar_banco.py
=====================

FERRAMENTA DE DESENVOLVIMENTO -- NÃO FAZ PARTE DO EXERCÍCIO.

Cria `application/database.sqlite` com as 4 tabelas vazias (o mesmo
schema que `etl_reverso.py` deve produzir), sem inserir nenhum dado.
Útil pra ter o banco com a estrutura pronta na mão -- pra testar
consultas manualmente, ou como base para `dev_popular_dummy.py`.

Uso:
    python application/dev_criar_banco.py
"""

import sqlite3
from pathlib import Path

BANCO = Path(__file__).parent / "database.sqlite"

TABELAS = {
    "resumo_vendas_categoria": ["categoria", "quantidade_vendida", "valor_total"],
    "vendas_por_mes": ["mes", "quantidade_vendas", "valor_total"],
    "top_clientes": ["id_cliente", "nome", "valor_total"],
    "resumo_geral": ["total_vendas", "valor_total_geral", "ticket_medio"],
}


def criar_banco() -> None:
    conexao = sqlite3.connect(BANCO)
    for nome_tabela, colunas in TABELAS.items():
        conexao.execute(f"DROP TABLE IF EXISTS {nome_tabela}")
        lista_colunas = ", ".join(colunas)
        conexao.execute(f"CREATE TABLE {nome_tabela} ({lista_colunas})")
    conexao.commit()
    conexao.close()


def main() -> None:
    criar_banco()
    print(f"Banco criado (tabelas vazias) em: {BANCO}")
    print("Tabelas:", ", ".join(TABELAS))


if __name__ == "__main__":
    main()
