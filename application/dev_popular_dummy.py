"""
dev_popular_dummy.py
=======================

FERRAMENTA DE DESENVOLVIMENTO -- NÃO FAZ PARTE DO EXERCÍCIO.

Popula `application/database.sqlite` com dados fictícios, sem precisar
rodar o pipeline inteiro (landing -> bronze -> silver -> gold ->
etl_reverso). Serve para testar `app.py` rapidamente enquanto se
desenvolve ou revisa o projeto.

Usa `dev_criar_banco.py` para (re)criar o schema antes de inserir os
dados -- as duas ferramentas compartilham a mesma definição de tabelas.

Se você é aluno: isso NÃO substitui o exercício. Os dados aqui são
inventados, não vêm de `lakehouse/gold/saida/` -- use `etl_reverso.py`
para o exercício de verdade.

Uso:
    python application/dev_popular_dummy.py
"""

import random
import sqlite3
from pathlib import Path

from dev_criar_banco import BANCO, criar_banco

CATEGORIAS = ["Eletrônicos", "Livros", "Roupas", "Alimentos", "Brinquedos"]
MESES = ["2025-01", "2025-02", "2025-03", "2025-04", "2025-05", "2025-06"]
NOMES = ["Ana", "Bruno", "Carla", "Daniel", "Elisa", "Fábio", "Gabriela", "Hugo", "Isabela", "João"]
SOBRENOMES = ["Silva", "Souza", "Oliveira", "Santos", "Pereira", "Costa", "Ferreira", "Almeida", "Lima", "Gomes"]


def gerar_dados(rng: random.Random) -> dict:
    resumo_categoria = []
    for categoria in CATEGORIAS:
        quantidade = rng.randint(20, 120)
        valor = round(quantidade * rng.uniform(30, 150), 2)
        resumo_categoria.append((categoria, quantidade, valor))
    resumo_categoria.sort(key=lambda linha: linha[2], reverse=True)

    vendas_por_mes = []
    for mes in MESES:
        quantidade = rng.randint(30, 80)
        valor = round(quantidade * rng.uniform(150, 300), 2)
        vendas_por_mes.append((mes, quantidade, valor))

    top_clientes = []
    for id_cliente in range(1, 11):
        nome = f"{rng.choice(NOMES)} {rng.choice(SOBRENOMES)}"
        valor = round(rng.uniform(500, 3000), 2)
        top_clientes.append((id_cliente, nome, valor))
    top_clientes.sort(key=lambda linha: linha[2], reverse=True)

    total_vendas = sum(linha[1] for linha in vendas_por_mes)
    valor_total_geral = round(sum(linha[2] for linha in vendas_por_mes), 2)
    ticket_medio = round(valor_total_geral / total_vendas, 2)
    resumo_geral = [(total_vendas, valor_total_geral, ticket_medio)]

    return {
        "resumo_vendas_categoria": resumo_categoria,
        "vendas_por_mes": vendas_por_mes,
        "top_clientes": top_clientes,
        "resumo_geral": resumo_geral,
    }


def main() -> None:
    rng = random.Random()  # sem semente fixa -- dados diferentes a cada execução
    criar_banco()
    conexao = sqlite3.connect(BANCO)

    dados = gerar_dados(rng)
    conexao.executemany("INSERT INTO resumo_vendas_categoria VALUES (?, ?, ?)", dados["resumo_vendas_categoria"])
    conexao.executemany("INSERT INTO vendas_por_mes VALUES (?, ?, ?)", dados["vendas_por_mes"])
    conexao.executemany("INSERT INTO top_clientes VALUES (?, ?, ?)", dados["top_clientes"])
    conexao.executemany("INSERT INTO resumo_geral VALUES (?, ?, ?)", dados["resumo_geral"])

    conexao.commit()
    conexao.close()

    print(f"database.sqlite populado com dados fictícios em: {BANCO}")
    print("Rode: streamlit run application/app.py")


if __name__ == "__main__":
    main()
