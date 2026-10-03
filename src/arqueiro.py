import random

from personagem import Personagem


class Arqueiro(Personagem):

    CHANCE_CRITICO = 0.3

    def __init__(self, nome):
        super().__init__(
            nome=nome,
            vida=90,
            ataque=25,
            defesa=8
        )

        self.flechas = 10

    def atacar(self, alvo):
        if self.flechas <= 0:
            print(f"{self.nome} está sem flechas e ataca com a adaga!")
            return alvo.receber_dano(self.ataque // 3)

        self.flechas -= 1
        dano = self.ataque

        if random.random() < self.CHANCE_CRITICO:
            dano *= 2
            print(f"ACERTO CRÍTICO! {self.nome} acerta {alvo.nome} em cheio!")
        else:
            print(f"{self.nome} dispara uma flecha em {alvo.nome}!")

        return alvo.receber_dano(dano)