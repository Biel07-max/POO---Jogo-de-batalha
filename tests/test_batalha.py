import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from batalha import Batalha
from guerreiro import Guerreiro
from mago import Mago
from inimigo import Inimigo
from item import PocaoDeVida


def rodar(batalha, entradas):
    """Executa a batalha com entradas simuladas e devolve (resultado, saída)."""
    saida = io.StringIO()
    with patch("builtins.input", side_effect=entradas), redirect_stdout(saida):
        resultado = batalha.iniciar()
    return resultado, saida.getvalue()


class TestBatalha(unittest.TestCase):

    def setUp(self):
        self.jogador = Guerreiro("Arthur")  # vida 120, ataque 20, defesa 15

    def test_vitoria_em_um_golpe(self):
        inimigo = Inimigo("Fraco", vida=10, ataque=50, defesa=5)
        resultado, saida = rodar(Batalha(self.jogador, inimigo), ["1"])
        self.assertEqual(resultado, "vitoria")
        self.assertFalse(inimigo.esta_vivo())
        self.assertIn("VITÓRIA", saida)

    def test_inimigo_morto_nao_contra_ataca(self):
        inimigo = Inimigo("Fraco", vida=10, ataque=50, defesa=5)
        rodar(Batalha(self.jogador, inimigo), ["1"])
        self.assertEqual(self.jogador.vida, 120)

    def test_inimigo_ataca_apos_o_jogador(self):
        inimigo = Inimigo("Duro", vida=1000, ataque=25, defesa=5)
        rodar(Batalha(self.jogador, inimigo), ["1", "3"])
        self.assertEqual(inimigo.vida, 985)      # 20 - 5
        self.assertEqual(self.jogador.vida, 110)  # 25 - 15

    def test_derrota(self):
        inimigo = Inimigo("Brutal", vida=1000, ataque=500, defesa=5)
        resultado, saida = rodar(Batalha(self.jogador, inimigo), ["1"])
        self.assertEqual(resultado, "derrota")
        self.assertFalse(self.jogador.esta_vivo())
        self.assertIn("DERROTA", saida)

    def test_fuga(self):
        inimigo = Inimigo("Duro", vida=1000, ataque=25, defesa=5)
        resultado, saida = rodar(Batalha(self.jogador, inimigo), ["3"])
        self.assertEqual(resultado, "fuga")
        self.assertEqual(self.jogador.vida, 120)  # inimigo não atacou
        self.assertIn("fugiu", saida)

    def test_opcao_invalida_nao_gasta_turno(self):
        inimigo = Inimigo("Duro", vida=1000, ataque=25, defesa=5)
        resultado, saida = rodar(Batalha(self.jogador, inimigo), ["9", "3"])
        self.assertEqual(resultado, "fuga")
        self.assertEqual(self.jogador.vida, 120)
        self.assertIn("Opção inválida", saida)

    def test_usar_pocao_cura_e_consome_item(self):
        inimigo = Inimigo("Duro", vida=1000, ataque=20, defesa=5)  # dano 5 no jogador
        self.jogador.vida = 50
        self.jogador.adicionar_item(PocaoDeVida())

        rodar(Batalha(self.jogador, inimigo), ["2", "1", "3"])

        self.assertEqual(self.jogador.inventario, [])
        self.assertEqual(self.jogador.vida, 50 + 40 - 5)  # cura e depois leva o golpe

    def test_usar_item_sem_inventario_nao_gasta_turno(self):
        inimigo = Inimigo("Duro", vida=1000, ataque=25, defesa=5)
        resultado, saida = rodar(Batalha(self.jogador, inimigo), ["2", "3"])
        self.assertEqual(resultado, "fuga")
        self.assertEqual(self.jogador.vida, 120)
        self.assertIn("não possui itens", saida)

    def test_voltar_do_inventario_mantem_item_e_turno(self):
        inimigo = Inimigo("Duro", vida=1000, ataque=25, defesa=5)
        self.jogador.adicionar_item(PocaoDeVida())
        rodar(Batalha(self.jogador, inimigo), ["2", "0", "3"])
        self.assertEqual(len(self.jogador.inventario), 1)
        self.assertEqual(self.jogador.vida, 120)

    def test_magia_do_mago_na_batalha(self):
        mago = Mago("Merlin")
        inimigo = Inimigo("Duro", vida=1000, ataque=10, defesa=5)
        rodar(Batalha(mago, inimigo), ["4", "3"])
        self.assertEqual(mago.mana, 80)
        self.assertEqual(inimigo.vida, 960)  # 45 - 5

    def test_magia_sem_mana_nao_gasta_turno(self):
        mago = Mago("Merlin")
        mago.mana = 0
        inimigo = Inimigo("Duro", vida=1000, ataque=50, defesa=5)
        rodar(Batalha(mago, inimigo), ["4", "3"])
        self.assertEqual(mago.vida, 80)
        self.assertEqual(inimigo.vida, 1000)

    def test_opcao_4_invalida_para_quem_nao_tem_magia(self):
        inimigo = Inimigo("Duro", vida=1000, ataque=25, defesa=5)
        _, saida = rodar(Batalha(self.jogador, inimigo), ["4", "3"])
        self.assertIn("Opção inválida", saida)


if __name__ == "__main__":
    unittest.main()