from .inimigo import Inimigo


class Orc(Inimigo):
    """A cada 3º ataque, desfere um Golpe Furioso (dano dobrado)."""

    def __init__(self, nome="Orc"):
        super().__init__(nome=nome, vida=150, ataque=22, defesa=10)
        self.turnos = 0

    def atacar(self, alvo):
        self.turnos += 1

        if self.turnos % 3 == 0:
            print(f"{self.nome} ruge e desfere um GOLPE FURIOSO!")
            return alvo.receber_dano(self.ataque * 2)

        return super().atacar(alvo)