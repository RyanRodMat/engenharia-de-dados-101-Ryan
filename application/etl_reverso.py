import csv
import sqlite3
from pathlib import Path

GOLD_SAIDA = Path(__file__).parent.parent / "lakehouse" / "gold" / "saida"
BANCO = Path(__file__).parent / "database.sqlite"

# nome da tabela -> colunas esperadas (na mesma ordem do CSV de origem)
TABELAS = {
    "resumo_vendas_categoria": ["categoria", "quantidade_vendida", "valor_total"],
    "vendas_por_mes": ["mes", "quantidade_vendas", "valor_total"],
    "top_clientes": ["id_cliente", "nome", "valor_total"],
    "resumo_geral": ["total_vendas", "valor_total_geral", "ticket_medio"],
}


def ler_csv_gold(nome_tabela: str) -> list[dict]:
    caminho = GOLD_SAIDA / f"{nome_tabela}.csv"
    with open(caminho, newline="", encoding="utf-8") as arquivo:
        return list(csv.DictReader(arquivo))

#Nunca tinha criado uma tabela antes, tive que pedir ajuda ao amigo claudinho 
def criar_tabela(conexao: sqlite3.Connection, nome_tabela: str, colunas: list[str]) -> None:
    with conexao:
        colunas_sql = ", ".join(f"{coluna} TEXT" for coluna in colunas)
        sql = f"CREATE TABLE {nome_tabela} ({colunas_sql})"
        conexao.execute(sql)



def inserir_linhas(conexao: sqlite3.Connection, nome_tabela: str, colunas: list[str], linhas: list[dict]) -> None:
    with conexao:
        colunas_sql = ", ".join(colunas)
        placeholders = ", ".join("?" for _ in colunas)
        sql = f"INSERT INTO {nome_tabela} ({colunas_sql}) VALUES ({placeholders})"
        for linha in linhas:
            valores = [linha.get(coluna, "") for coluna in colunas]
            conexao.execute(sql, valores)


def main() -> None:
    if BANCO.exists():
        BANCO.unlink()  # recomeça do zero a cada execução

    conexao = sqlite3.connect(BANCO)
    for nome_tabela, colunas in TABELAS.items():
        linhas = ler_csv_gold(nome_tabela)
        criar_tabela(conexao, nome_tabela, colunas)
        inserir_linhas(conexao, nome_tabela, colunas, linhas)
        print(f"{nome_tabela}: {len(linhas)} linhas carregadas")
    conexao.commit()
    conexao.close()

    print("\nAgora rode: python application/verificar_etl_reverso.py")


if __name__ == "__main__":
    main()
