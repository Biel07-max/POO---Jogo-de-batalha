from src.item import Item


class PocaoDeVida(Item):

    def __init__(self, cura=40):
        super().__init__(nome="Poção de Vida", valor=50)
        self.cura = cura

    def usar(self, personagem):
        curado = personagem.curar(self.cura)
        print(
            f"{personagem.nome} usou {self.nome} e recuperou {curado} de vida! "
            f"(Vida: {personagem.vida})"
        )
        return curado