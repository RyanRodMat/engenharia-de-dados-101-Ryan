
import csv
import json
from datetime import datetime, timezone
from pathlib import Path

LAKEHOUSE = Path(__file__).parent.parent
LANDING = LAKEHOUSE / "landing"
SAIDA = Path(__file__).parent / "saida"

# Use o mesmo timestamp para todos os registros de uma mesma execução.
DT_INGESTAO = datetime.now(timezone.utc).isoformat()


def ler_vendas_csv() -> list[dict]:
    try:
        with open(LANDING / "vendas.csv", newline="", encoding="utf-8") as arquivo:
            ler = csv.DictReader(arquivo)
            return list(ler)
    except FileNotFoundError:
        print("Arquivo não encontrado.")
        return []
    except Exception as error:
        print(f"Erro ao ler vendas.csv: {error}")
        return []



def ler_clientes_json() -> list[dict]:
    try:
        with open(LANDING / "clientes.json", "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        print("Arquivo não encontrado.")
        return []
    except Exception as error:
        print(f"Erro ao ler clientes.json: {error}")
        return []


def ler_produtos_txt() -> list[dict]:
    try:
        with open(LANDING / "produtos.txt", "r", encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()

        registros = []
        cabecalho = None

        for linha in linhas:
            linha = linha.strip()
            if not linha or linha.startswith("#"):
                continue  # Ignora linhas em branco e comentários
            if cabecalho is None:
                cabecalho = linha.split("|")  # Define o cabeçalho
                continue
            valores = linha.split("|")
            registro = dict(zip(cabecalho, valores))
            registros.append(registro)

        return registros
    except FileNotFoundError:
        print("Arquivo não encontrado.")
        return []
    except Exception as error:
        print(f"Erro ao ler produtos.txt: {error}")
        return []


def adicionar_metadados(registros: list[dict], nome_arquivo: str) -> list[dict]:
    for registro in registros:
        registro["arquivo_origem"] = nome_arquivo
        registro["dt_ingestao"] = DT_INGESTAO
    return registros


def salvar_csv(registros: list[dict], caminho_saida: Path, colunas: list[str]) -> None:
    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    with open(caminho_saida, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=colunas)
        escritor.writeheader()
        for registro in registros:
            escritor.writerow({coluna: registro.get(coluna, "") for coluna in colunas})


def main() -> None:
    vendas = adicionar_metadados(ler_vendas_csv(), "vendas.csv")
    clientes = adicionar_metadados(ler_clientes_json(), "clientes.json")
    produtos = adicionar_metadados(ler_produtos_txt(), "produtos.txt")

    salvar_csv(
        vendas,
        SAIDA / "vendas_bronze.csv",
        ["id_venda", "id_cliente", "id_produto", "quantidade", "data_venda", "valor_total", "arquivo_origem", "dt_ingestao"],
    )
    salvar_csv(
        clientes,
        SAIDA / "clientes_bronze.csv",
        ["id_cliente", "nome", "email", "cidade", "estado", "data_cadastro", "telefone", "arquivo_origem", "dt_ingestao"],
    )
    salvar_csv(
        produtos,
        SAIDA / "produtos_bronze.csv",
        ["id_produto", "nome", "categoria", "preco", "ativo", "arquivo_origem", "dt_ingestao"],
    )

    print(f"vendas_bronze.csv:   {len(vendas)} linhas")
    print(f"clientes_bronze.csv: {len(clientes)} linhas")
    print(f"produtos_bronze.csv: {len(produtos)} linhas")
    print("\nAgora rode: python lakehouse/bronze/verificar_bronze.py")


if __name__ == "__main__":
    main()
