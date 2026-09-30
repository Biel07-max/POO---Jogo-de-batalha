from abc import ABC, abstractmethod


class Personagem(ABC):

    def __init__(self, nome, vida, ataque, defesa):
        self.nome = nome
        self.vida = vida
        self.vida_maxima = vida
        self.ataque = ataque
        self.defesa = defesa
        self.inventario = []

    def esta_vivo(self):
        return self.vida > 0

    def receber_dano(self, dano, ignorar_defesa=False):
        """Aplica o dano (reduzido pela defesa) e retorna o dano realmente sofrido.

        - Dano final = dano - defesa, com mínimo de 1 (todo golpe machuca).
        - Se ignorar_defesa=True, a defesa não é considerada.
        - A vida nunca fica abaixo de 0.
        """
        if ignorar_defesa:
            dano_final = dano
        else:
            dano_final = max(1, dano - self.defesa)

        dano_final = max(0, dano_final)
        self.vida = max(0, self.vida - dano_final)

        print(f"{self.nome} recebeu {dano_final} de dano! (Vida: {self.vida})")
        return dano_final

    def curar(self, quantidade):
        """Recupera vida sem ultrapassar a vida máxima. Retorna quanto curou."""
        vida_antes = self.vida
        self.vida = min(self.vida_maxima, self.vida + quantidade)
        return self.vida - vida_antes

    def adicionar_item(self, item):
        self.inventario.append(item)

    @abstractmethod
    def atacar(self, alvo):
        pass

    def mostrar_status(self):
        print(
            f"{self.nome} | "
            f"Vida: {self.vida} | "
            f"Ataque: {self.ataque} | "
            f"Defesa: {self.defesa}"
        )