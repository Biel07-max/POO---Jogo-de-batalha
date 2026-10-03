from personagem import Personagem


class Mago(Personagem):

    CUSTO_MAGIA = 20

    def __init__(self, nome):
        super().__init__(
            nome=nome,
            vida=80,
            ataque=30,
            defesa=5
        )

        self.mana = 100

    def atacar(self, alvo):
        # Ataque normal: pancada de cajado, metade do poder mágico
        print(f"{self.nome} acerta {alvo.nome} com o cajado!")
        return alvo.receber_dano(self.ataque // 2)

    def usar_magia(self, alvo):
        if self.mana < self.CUSTO_MAGIA:
            print("O mago não possui mana suficiente.")
            return 0

        self.mana -= self.CUSTO_MAGIA
        print(
            f"{self.nome} lança uma bola de fogo em {alvo.nome}! "
            f"(Mana restante: {self.mana})"
        )
        # A magia dá 50% a mais de dano que o ataque base
        return alvo.receber_dano(int(self.ataque * 1.5))