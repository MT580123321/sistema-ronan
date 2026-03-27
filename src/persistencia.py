import json

ARQUIVO = "dados.json"

def salvar_dados(comandas):
    dados = []

    for comanda in comandas:
        dados_comanda = {
            "mesa": comanda.mesa.numero,
            "itens": []
        }

        for item in comanda.itens:
            dados_comanda["itens"].append({
                "produto": item.produto.nome,
                "preco": item.produto.preco,
                "quantidade": item.quantidade
            })

        dados.append(dados_comanda)

    with open(ARQUIVO, "w") as f:
        json.dump(dados, f, indent=4)


def carregar_dados():
    try:
        with open(ARQUIVO, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []