import json

<<<<<<< HEAD
def salvar(dados, arquivo):
    with open(arquivo, "w") as f:
        json.dump(dados, f)

def carregar(arquivo):
    try:
        with open(arquivo, "r") as f:
            return json.load(f)
    except:
=======
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

    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)



def carregar_dados():
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)

    except FileNotFoundError:
>>>>>>> 2537dd920b42e569adafa6a79089b16ecda7162b
        return []
