"""
dev_limpar_banco.py
======================

FERRAMENTA DE DESENVOLVIMENTO -- NÃO FAZ PARTE DO EXERCÍCIO.

Limpa os DADOS de `application/database.sqlite`: roda um `DELETE FROM`
em cada tabela, mas mantém o arquivo e o schema intactos.

- Para recriar as tabelas do zero, use `dev_criar_banco.py`.
- Para apagar o banco por completo (arquivo e tudo), apague
  `database.sqlite` diretamente.

Uso:
    python application/dev_limpar_banco.py
"""

import sqlite3
from pathlib import Path

BANCO = Path(__file__).parent / "database.sqlite"

TABELAS = ["resumo_vendas_categoria", "vendas_por_mes", "top_clientes", "resumo_geral"]


def main() -> None:
    if not BANCO.exists():
        print(f"{BANCO} não existe -- nada a limpar.")
        print("Rode 'python application/dev_criar_banco.py' para criar o banco primeiro.")
        return

    conexao = sqlite3.connect(BANCO)
    tabelas_existentes = {
        linha[0] for linha in conexao.execute("SELECT name FROM sqlite_master WHERE type='table'")
    }

    for nome_tabela in TABELAS:
        if nome_tabela in tabelas_existentes:
            conexao.execute(f"DELETE FROM {nome_tabela}")
            print(f"{nome_tabela}: dados apagados.")
        else:
            print(f"{nome_tabela}: tabela não existe, ignorando.")

    conexao.commit()
    conexao.close()

    print(f"\nDados limpos em: {BANCO} (arquivo e schema mantidos).")


if __name__ == "__main__":
    main()
