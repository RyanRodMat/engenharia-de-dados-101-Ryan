
import csv
from collections import defaultdict
from pathlib import Path

LAKEHOUSE = Path(__file__).parent.parent
SILVER_SAIDA = LAKEHOUSE / "silver" / "saida"
SAIDA = Path(__file__).parent / "saida"


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


def calcular_resumo_por_categoria(vendas: list[dict], produtos: list[dict]) -> list[dict]: #essa aq foi difícil deu erro umas 3 vezes
    produto_para_categoria = {
        produto["id_produto"]: produto["categoria"]
        for produto in produtos
    }

    resumo_por_categoria = defaultdict(
        lambda: {
            "quantidade_vendida": 0,
            "valor_total": 0.0
        }
    )

    for venda in vendas:
        id_produto = venda["id_produto"]
        categoria = produto_para_categoria[id_produto]

        resumo_por_categoria[categoria]["quantidade_vendida"] += int(
            venda["quantidade"]
        )
        resumo_por_categoria[categoria]["valor_total"] += float(
            venda["valor_total"]
        )

    resultado = []

    for categoria, dados in resumo_por_categoria.items():
        resultado.append({
            "categoria": categoria,
            "quantidade_vendida": dados["quantidade_vendida"],
            "valor_total": dados["valor_total"]
        })

    return resultado




def calcular_vendas_por_mes(vendas: list[dict]) -> list[dict]:
    vendas_por_mes = defaultdict(lambda: {"quantidade_vendas": 0, "valor_total": 0.0})
    for venda in vendas:
        mes = venda["data_venda"][:7]  
        vendas_por_mes[mes]["quantidade_vendas"] += 1
        vendas_por_mes[mes]["valor_total"] += float(venda["valor_total"])

    resultado = []
    for mes, dados in vendas_por_mes.items():
        resultado.append({
            "mes": mes,
            "quantidade_vendas": dados["quantidade_vendas"],
            "valor_total": dados["valor_total"]
        })
    return resultado


def calcular_top_clientes(vendas: list[dict], clientes: list[dict], top_n: int = 10) -> list[dict]:
    top_clientes = defaultdict(lambda: {"nome": "", "valor_total": 0.0})
    for cliente in clientes:
        top_clientes[cliente["id_cliente"]]["nome"] = cliente["nome"]
    for venda in vendas:
        id_cliente = venda["id_cliente"]
        top_clientes[id_cliente]["valor_total"] += float(venda["valor_total"])
    resultado = sorted(#mao estava conseguindo fazer e precisei da ajuda do amigo claudinho, mas acho que entendi o conceito
        [{"id_cliente": id_cliente, "nome": dados["nome"], "valor_total": dados["valor_total"]}
         for id_cliente, dados in top_clientes.items()],
        key=lambda x: x["valor_total"],
        reverse=True
    )
    return resultado[:top_n]


def calcular_resumo_geral(vendas: list[dict]) -> list[dict]:
    total_vendas = len(vendas)
    valor_total_geral = sum(float(venda["valor_total"]) for venda in vendas)
    ticket_medio = round(valor_total_geral / total_vendas, 2) if total_vendas > 0 else 0.0
    return [{
        "total_vendas": total_vendas,
        "valor_total_geral": valor_total_geral,
        "ticket_medio": ticket_medio
    }]



def main() -> None:
    vendas = ler_csv(SILVER_SAIDA / "vendas_silver.csv")
    clientes = ler_csv(SILVER_SAIDA / "clientes_silver.csv")
    produtos = ler_csv(SILVER_SAIDA / "produtos_silver.csv")

    resumo_categoria = calcular_resumo_por_categoria(vendas, produtos)
    vendas_por_mes = calcular_vendas_por_mes(vendas)
    top_clientes = calcular_top_clientes(vendas, clientes)
    resumo_geral = calcular_resumo_geral(vendas)

    salvar_csv(resumo_categoria, SAIDA / "resumo_vendas_categoria.csv", ["categoria", "quantidade_vendida", "valor_total"])
    salvar_csv(vendas_por_mes, SAIDA / "vendas_por_mes.csv", ["mes", "quantidade_vendas", "valor_total"])
    salvar_csv(top_clientes, SAIDA / "top_clientes.csv", ["id_cliente", "nome", "valor_total"])
    salvar_csv(resumo_geral, SAIDA / "resumo_geral.csv", ["total_vendas", "valor_total_geral", "ticket_medio"])

    print(f"resumo_vendas_categoria.csv: {len(resumo_categoria)} linhas")
    print(f"vendas_por_mes.csv:          {len(vendas_por_mes)} linhas")
    print(f"top_clientes.csv:            {len(top_clientes)} linhas")
    print(f"resumo_geral.csv:            {len(resumo_geral)} linha")
    print("\nAgora rode: python lakehouse/gold/verificar_gold.py")


if __name__ == "__main__":
    main()
