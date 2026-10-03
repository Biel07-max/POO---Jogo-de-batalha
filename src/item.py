class Item:

    def __init__(self, nome, valor):
        self.nome = nome
        self.valor = valor

    def usar(self, personagem):
        raise NotImplementedError("Cada item deve implementar seu próprio efeito.")