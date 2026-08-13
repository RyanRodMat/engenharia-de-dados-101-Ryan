
import csv
from pathlib import Path

LAKEHOUSE = Path(__file__).parent.parent
BRONZE_SAIDA = LAKEHOUSE / "bronze" / "saida"
SAIDA = Path(__file__).parent / "saida"

CATEGORIAS_VALIDAS = {"Eletrônicos", "Livros", "Roupas", "Alimentos", "Brinquedos"}
ESTADOS_VALIDOS = {"SP", "RJ", "MG", "RS", "BA", "PR", "PE", "CE", "SC", "GO"}


def ler_csv(caminho: Path) -> list[dict]:
    with open(caminho, newline="", encoding="utf-8") as arquivo:
        return list(csv.DictReader(arquivo))


def salvar_csv(registros: list[dict], caminho_saida: Path, colunas: list[str]) -> None:
    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    with open(caminho_saida, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=colunas)
        escritor.writeheader()
        for registro in registros:
            escritor.writerow({coluna: registro.get(coluna, "") for coluna in colunas})


def limpar_clientes(bronze: list[dict]) -> list[dict]:
    clientes: dict[int, dict] = {}
    for registro in bronze:
        try:
            id_cliente = int(registro["id_cliente"])
        except (ValueError, TypeError):
            continue

        email = registro.get("email", "").strip().lower()
        if "@" not in email:
            continue 

        estado = registro.get("estado", "").strip().upper()
        if estado not in ESTADOS_VALIDOS:
            continue 

        clientes[id_cliente] = {
            "id_cliente": id_cliente,
            "nome": registro.get("nome", "").strip(),
            "email": email,
            "cidade": registro.get("cidade", "").strip(),
            "estado": estado,
            "data_cadastro": registro.get("data_cadastro", "").strip(),
        }
    return list(clientes.values())

    raise NotImplementedError("Implemente limpar_clientes()")


def limpar_produtos(bronze: list[dict]) -> list[dict]:
    produtos: dict[int, dict] = {}
    for registro in bronze:
        try:
            id_produto = int(registro["id_produto"])
        except (ValueError, TypeError):
            continue

        preco_str = registro.get("preco", "").replace(",", ".").strip()
        try:
            preco = float(preco_str)
        except ValueError:
            continue

        categoria = registro.get("categoria", "").strip().capitalize()
        if categoria not in CATEGORIAS_VALIDAS:
            continue

        ativo_str = registro.get("ativo", "").strip().lower()
        if ativo_str in {"sim", "1"}:
            a = 1
        else:
            a = 0

        if id_produto not in produtos:  
            produtos[id_produto] = {
                "id_produto": id_produto,
                "nome": registro.get("nome", "").strip(),
                "categoria": categoria,
                "preco": preco,
                "ativo": a,
            }
    return list(produtos.values())

    raise NotImplementedError("Implemente limpar_produtos()")


def limpar_vendas(bronze: list[dict], ids_clientes_validos: set[int], ids_produtos_validos: set[int]) -> list[dict]:
  vendas: dict[int, dict] = {}
  for registro in bronze:
    try:
      id_venda = int(registro["id_venda"].strip())
      id_cliente = int(registro["id_cliente"].strip())
      id_produto = int(registro["id_produto"].strip())
      quantidade = int(registro["quantidade"].strip())
      valor_total = float(registro["valor_total"].replace(",", ".").strip())
      data_venda = registro["data_venda"].strip()
    except (ValueError, TypeError):
      continue

    if quantidade <= 0 or valor_total == "":
      continue

    if id_cliente not in ids_clientes_validos or id_produto not in ids_produtos_validos:
      continue
    try:
      if "/" in data_venda:
        dia, mes, ano = map(int, data_venda.split("/"))
        data_venda = f"{ano:04d}-{mes:02d}-{dia:02d}"
      else:
        ano, mes, dia = map(int, data_venda.split("-"))
        data_venda = f"{ano:04d}-{mes:02d}-{dia:02d}"
    except (ValueError, TypeError):
      continue

    try:
      if id_venda not in vendas:
        vendas[id_venda] = {
          "id_venda": id_venda,
          "id_cliente": id_cliente,
          "id_produto": id_produto,
          "quantidade": quantidade,
          "data_venda": data_venda,
          "valor_total": valor_total
        }
    except KeyError:
      continue
    return list(vendas.values())
    
    raise NotImplementedError("Implemente limpar_vendas()")


def main() -> None:
    clientes_bronze = ler_csv(BRONZE_SAIDA / "clientes_bronze.csv")
    produtos_bronze = ler_csv(BRONZE_SAIDA / "produtos_bronze.csv")
    vendas_bronze = ler_csv(BRONZE_SAIDA / "vendas_bronze.csv")

    clientes = limpar_clientes(clientes_bronze)
    produtos = limpar_produtos(produtos_bronze)

    ids_clientes_validos = {c["id_cliente"] for c in clientes}
    ids_produtos_validos = {p["id_produto"] for p in produtos}

    vendas = limpar_vendas(vendas_bronze, ids_clientes_validos, ids_produtos_validos)

    salvar_csv(clientes, SAIDA / "clientes_silver.csv", ["id_cliente", "nome", "email", "cidade", "estado", "data_cadastro"])
    salvar_csv(produtos, SAIDA / "produtos_silver.csv", ["id_produto", "nome", "categoria", "preco", "ativo"])
    salvar_csv(vendas, SAIDA / "vendas_silver.csv", ["id_venda", "id_cliente", "id_produto", "quantidade", "data_venda", "valor_total"])

    print(f"clientes_silver.csv: {len(clientes)} linhas")
    print(f"produtos_silver.csv: {len(produtos)} linhas")
    print(f"vendas_silver.csv:   {len(vendas)} linhas")
    print("\nAgora rode: python lakehouse/silver/verificar_silver.py")


if __name__ == "__main__":
    main()
