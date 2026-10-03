from inimigo import Inimigo


class Dragao(Inimigo):
    """Chefe final. A cada 3º ataque cospe fogo, que ignora a defesa."""

    def __init__(self, nome="Dragão Ancião"):
        super().__init__(nome=nome, vida=300, ataque=35, defesa=20)
        self.turnos = 0

    def atacar(self, alvo):
        self.turnos += 1

        if self.turnos % 3 == 0:
            print(f"{self.nome} inspira fundo e cospe uma torrente de FOGO!")
            return alvo.receber_dano(int(self.ataque * 1.5), ignorar_defesa=True)

        print(f"{self.nome} ataca {alvo.nome} com as garras!")
        return alvo.receber_dano(self.ataque)