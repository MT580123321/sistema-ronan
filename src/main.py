from produto import Produto
from mesa import Mesa
from pedido import Pedido
from comanda import Comanda

print("INICIO")

# Produtos
picanha = Produto("Picanha", 100, 10)
cerveja = Produto("Cerveja", 10, 50)
refrigerante = Produto("Refrigerante", 8, 30)

cardapio = [picanha, cerveja, refrigerante]


print("\n--- CARDÁPIO ---")
for i, produto in enumerate(cardapio):
    print(i, "-", produto.nome, "R$", produto.preco)

# Mesas
mesa1 = Mesa(1)
mesa2 = Mesa(2)

# Comandas
comanda1 = Comanda(mesa1)
comanda2 = Comanda(mesa2)

opcao = int(input("Escolha o produto: "))
quantidade = int(input("Quantidade: "))

mesa_escolhida = int(input("Escolha a mesa (1 ou 2): "))
if mesa_escolhida == 1:
    comanda = comanda1
elif mesa_escolhida == 2:
    comanda = comanda2
else:
    print("Mesa inválida")
    exit()
produto_escolhido = cardapio[opcao]
comanda.adicionar_pedido(Pedido(produto_escolhido, quantidade))


# Fechamento
while True:
    print("\n--- MENU ---")
    print("1 - Adicionar pedido")
    print("2 - Fechar mesa")
    print("3 - Ver relatório")
    print("0 - Sair")

    opcao_menu = input("Escolha: ")

    # 👉 ADICIONAR PEDIDO
    if opcao_menu == "1":
        print("\n--- CARDÁPIO ---")
        for i, produto in enumerate(cardapio):
            print(i, "-", produto.nome, "R$", produto.preco)

        opcao = int(input("Escolha o produto: "))
        quantidade = int(input("Quantidade: "))
        mesa_escolhida = int(input("Escolha a mesa (1 ou 2): "))

        if mesa_escolhida == 1:
            comanda = comanda1
        elif mesa_escolhida == 2:
            comanda = comanda2
        else:
            print("Mesa inválida")
            continue

        produto_escolhido = cardapio[opcao]
        comanda.adicionar_pedido(Pedido(produto_escolhido, quantidade))

    # 👉 FECHAR MESA
    elif opcao_menu == "2":
        mesa_escolhida = int(input("Qual mesa fechar (1 ou 2): "))

        if mesa_escolhida == 1:
            total = comanda1.fechar()
            print("Mesa 1 fechada. Total:", total)
        elif mesa_escolhida == 2:
            total = comanda2.fechar()
            print("Mesa 2 fechada. Total:", total)
        else:
            print("Mesa inválida")

    # 👉 RELATÓRIO
    elif opcao_menu == "3":
        print("\n--- RELATÓRIO ---")
        print("Mesa 1:", comanda1.total())
        print("Mesa 2:", comanda2.total())
        print("Total do dia:", comanda1.total() + comanda2.total())

    # 👉 SAIR
    elif opcao_menu == "0":
        print("Encerrando sistema...")
        break

    else:
        print("Opção inválida")