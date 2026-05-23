import json

def salvar(dados, arquivo):
    with open(arquivo, "w") as f:
        json.dump(dados, f)

def carregar(arquivo):
    try:
        with open(arquivo, "r") as f:
            return json.load(f)
    except:
        return []
