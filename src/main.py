from produto import Produto
from mesa import Mesa
from pedido import Pedido
from comanda import Comanda

# LISTA DE COMANDAS
lista_comandas = []

# PRODUTOS FIXOS
cardapio = [
    Produto("Picanha", 100,10),
    Produto("Cerveja", 10,10),
    Produto("Refrigerante", 8,10)
]

# FUNÇÃO RELATÓRIO
def ver_relatorio(comandas):
    if not comandas:
        print("\nNenhuma comanda encontrada!")
        return

    print("\n--- RELATÓRIO ---")

    for comanda in comandas:
        print(f"\nMesa: {comanda.mesa.numero}")
        total = 0

        for item in comanda.itens:
            subtotal = item.produto.preco * item.quantidade
            total += subtotal

            print(f"- {item.produto.nome} | Qtd: {item.quantidade} | R$ {subtotal}")

        print(f"Total da mesa: R$ {total}")


# MENU
while True:
    print("\n--- MENU ---")
    print("1 - Adicionar pedido")
    print("2 - Fechar mesa")
    print("3 - Ver relatório")
    print("0 - Sair")

    opcao = input("Escolha: ")

    # ADICIONAR PEDIDO
    if opcao == "1":
        numero_mesa = int(input("Número da mesa: "))
        mesa = Mesa(numero_mesa)

        # CRIA COMANDA
        comanda = Comanda(mesa)

        print("\nCardápio:")
        for i, p in enumerate(cardapio):
            print(f"{i+1} - {p.nome} (R$ {p.preco})")

        escolha = int(input("Escolha o produto: ")) - 1
        quantidade = int(input("Quantidade: "))

        produto = cardapio[escolha]

        pedido = Pedido(produto, quantidade)
        comanda.adicionar_item(pedido)

        lista_comandas.append(comanda)

        print("Pedido adicionado com sucesso!")

    # FECHAR MESA
    elif opcao == "2":
        numero = int(input("Número da mesa para fechar: "))

        for comanda in lista_comandas:
            if comanda.mesa.numero == numero:
                print(f"Fechando mesa {numero}...")
                lista_comandas.remove(comanda)
                print("Mesa fechada!")
                break
        else:
            print("Mesa não encontrada!")

    # RELATÓRIO (AGORA FUNCIONA)
    elif opcao == "3":
        ver_relatorio(lista_comandas)

    # SAIR
    elif opcao == "0":
        print("Saindo...")
        break

    else:
        print("Opção inválida!")