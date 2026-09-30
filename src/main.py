from .guerreiro import Guerreiro
from .inimigo import Inimigo
from .batalha import Batalha


def main():

    jogador = Guerreiro("Arthur")

    inimigo = Inimigo(
        nome="Goblin",
        vida=100,
        ataque=15,
        defesa=5
    )

    batalha = Batalha(jogador, inimigo)

    batalha.iniciar()


if __name__ == "__main__":
    main()
