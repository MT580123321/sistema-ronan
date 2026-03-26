class Comanda:
    def __init__(self, mesa):
        self.mesa = mesa
        self.pedidos = []
        self.ativa = True

    def adicionar_pedido(self, pedido):
        if not self.ativa:
            raise Exception("Comanda fechada")
        self.pedidos.append(pedido)

    def total(self):
        return sum(p.subtotal() for p in self.pedidos)

    def fechar(self):
        self.ativa = False
        return self.total()
    def limpar(self):
        self.pedidos = []
        self.ativa = True