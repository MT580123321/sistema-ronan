class Comanda:
<<<<<<< HEAD
    def __init__(self, cliente):
        self.cliente = cliente
        self.itens = []
=======

    def __init__(self, mesa):
        self.mesa = mesa
        self.itens = []

    def adicionar_item(self, pedido):
        self.itens.append(pedido)

    def calcular_total(self):

        total = 0

        for item in self.itens:
            total += item.subtotal()

        return total
>>>>>>> 2537dd920b42e569adafa6a79089b16ecda7162b
