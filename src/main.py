from produto import Produto
            numero_mesa = int(input("Número da mesa: "))

            comanda = buscar_comanda(numero_mesa)

            # cria somente se não existir
            if comanda is None:
                mesa = Mesa(numero_mesa)
                comanda = Comanda(mesa)
                lista_comandas.append(comanda)

            print("\nCardápio:")

            for i, produto in enumerate(cardapio):
                print(
                    f"{i+1} - {produto.nome} "
                    f"(R$ {produto.preco}) "
                    f"| Estoque: {produto.estoque}"
                )

            escolha = int(input("Escolha o produto: ")) - 1
            quantidade = int(input("Quantidade: "))

            if escolha < 0 or escolha >= len(cardapio):
                print("Produto inválido!")
                continue

            produto = cardapio[escolha]

            pedido = Pedido(produto, quantidade)
            comanda.adicionar_item(pedido)

            salvar_dados(lista_comandas)

            print("Pedido adicionado com sucesso!")

        except ValueError:
            print("Digite apenas números!")

        except Exception as erro:
            print(f"Erro: {erro}")


    # FECHAR MESA
    elif opcao == "2":
        try:
            numero = int(input("Número da mesa para fechar: "))

            comanda = buscar_comanda(numero)

            if comanda:
                print(f"Total da mesa: R$ {comanda.calcular_total():.2f}")
                lista_comandas.remove(comanda)

                salvar_dados(lista_comandas)

                print("Mesa fechada com sucesso!")

            else:
                print("Mesa não encontrada!")

        except ValueError:
            print("Digite apenas números!")


    # RELATÓRIO
    elif opcao == "3":
        ver_relatorio(lista_comandas)


    # SAIR
    elif opcao == "0":
        salvar_dados(lista_comandas)
        print("Saindo do sistema...")
        break


    else:
        print("Opção inválida!")
