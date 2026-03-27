class Comanda:
    def __init__(self, mesa):
        self.mesa = mesa
        self.itens = []

    def adicionar_item(self, pedido):
        self.itens.append(pedido)