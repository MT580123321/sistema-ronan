class Pedido:
    def __init__(self, produto, quantidade):
        if produto.estoque < quantidade:
            raise Exception("Estoque insuficiente")

        self.produto = produto
        self.quantidade = quantidade

        # desconta do estoque
        produto.estoque -= quantidade

    def subtotal(self):
        return self.produto.preco * self.quantidade