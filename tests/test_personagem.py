import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from personagem import Personagem
from guerreiro import Guerreiro
from mago import Mago
from arqueiro import Arqueiro
from inimigo import Inimigo
from orc import Orc
from dragao import Dragao
from pocao import PocaoDeVida


class PersonagemFake(Personagem):
    def atacar(self, alvo):
        return alvo.receber_dano(self.ataque)


class TestBase(unittest.TestCase):
    def setUp(self):
        # silencia os prints durante os testes
        self._out = redirect_stdout(io.StringIO())
        self._out.__enter__()

    def tearDown(self):
        self._out.__exit__(None, None, None)


class TestPersonagem(TestBase):

    def setUp(self):
        super().setUp()
        self.p = PersonagemFake("Teste", vida=100, ataque=20, defesa=10)

    def test_personagem_e_abstrato(self):
        with self.assertRaises(TypeError):
            Personagem("X", 10, 1, 1)

    def test_esta_vivo(self):
        self.assertTrue(self.p.esta_vivo())
        self.p.vida = 0
        self.assertFalse(self.p.esta_vivo())

    def test_dano_reduzido_pela_defesa(self):
        dano = self.p.receber_dano(30)
        self.assertEqual(dano, 20)
        self.assertEqual(self.p.vida, 80)

    def test_dano_minimo_e_1(self):
        dano = self.p.receber_dano(5)  # menor que a defesa
        self.assertEqual(dano, 1)
        self.assertEqual(self.p.vida, 99)

    def test_vida_nunca_fica_negativa(self):
        self.p.receber_dano(1000)
        self.assertEqual(self.p.vida, 0)
        self.assertFalse(self.p.esta_vivo())

    def test_ignorar_defesa(self):
        dano = self.p.receber_dano(30, ignorar_defesa=True)
        self.assertEqual(dano, 30)
        self.assertEqual(self.p.vida, 70)

    def test_curar_nao_passa_da_vida_maxima(self):
        self.p.vida = 90
        curado = self.p.curar(50)
        self.assertEqual(curado, 10)
        self.assertEqual(self.p.vida, 100)


class TestClasses(TestBase):

    def test_guerreiro_ataca(self):
        g = Guerreiro("Arthur")
        alvo = Inimigo("Alvo", 100, 1, 5)
        g.atacar(alvo)
        self.assertEqual(alvo.vida, 85)  # 20 - 5 = 15

    def test_inimigo_ataca(self):
        i = Inimigo("Goblin", 100, 15, 5)
        g = Guerreiro("Arthur")
        i.atacar(g)
        # ataque 15 contra defesa 15 => dano mínimo de 1
        self.assertEqual(g.vida, 119)

    def test_mago_ataque_normal(self):
        m = Mago("Merlin")
        alvo = Inimigo("Alvo", 100, 1, 5)
        m.atacar(alvo)
        self.assertEqual(alvo.vida, 90)  # 15 - 5 = 10

    def test_mago_magia_consome_mana_e_causa_dano(self):
        m = Mago("Merlin")
        alvo = Inimigo("Alvo", 100, 1, 5)
        m.usar_magia(alvo)
        self.assertEqual(m.mana, 80)
        self.assertEqual(alvo.vida, 60)  # 45 - 5 = 40

    def test_mago_sem_mana(self):
        m = Mago("Merlin")
        m.mana = 10
        alvo = Inimigo("Alvo", 100, 1, 5)
        m.usar_magia(alvo)
        self.assertEqual(m.mana, 10)
        self.assertEqual(alvo.vida, 100)

    @patch("arqueiro.random.random", return_value=0.99)
    def test_arqueiro_tiro_normal(self, _):
        a = Arqueiro("Robin")
        alvo = Inimigo("Alvo", 100, 1, 5)
        a.atacar(alvo)
        self.assertEqual(alvo.vida, 80)  # 25 - 5
        self.assertEqual(a.flechas, 9)

    @patch("arqueiro.random.random", return_value=0.0)
    def test_arqueiro_critico(self, _):
        a = Arqueiro("Robin")
        alvo = Inimigo("Alvo", 100, 1, 5)
        a.atacar(alvo)
        self.assertEqual(alvo.vida, 55)  # 50 - 5

    def test_arqueiro_sem_flechas(self):
        a = Arqueiro("Robin")
        a.flechas = 0
        alvo = Inimigo("Alvo", 100, 1, 5)
        a.atacar(alvo)
        self.assertEqual(alvo.vida, 97)  # 25//3 = 8 - 5 = 3
        self.assertEqual(a.flechas, 0)

    def test_orc_golpe_furioso_no_terceiro_ataque(self):
        orc = Orc()
        alvo = Inimigo("Alvo", 1000, 1, 0)
        orc.atacar(alvo)
        orc.atacar(alvo)
        self.assertEqual(alvo.vida, 1000 - 22 * 2)
        orc.atacar(alvo)  # golpe furioso: 44
        self.assertEqual(alvo.vida, 1000 - 22 * 2 - 44)

    def test_dragao_fogo_ignora_defesa(self):
        d = Dragao()
        g = Guerreiro("Arthur")  # defesa 15
        d.atacar(g)  # 35 - 15 = 20
        d.atacar(g)  # 20
        self.assertEqual(g.vida, 80)
        d.atacar(g)  # fogo: 52 ignorando defesa
        self.assertEqual(g.vida, 28)

    def test_pocao_de_vida(self):
        g = Guerreiro("Arthur")
        g.vida = 50
        PocaoDeVida().usar(g)
        self.assertEqual(g.vida, 90)

    def test_pocao_nao_ultrapassa_vida_maxima(self):
        g = Guerreiro("Arthur")
        g.vida = 110
        PocaoDeVida().usar(g)
        self.assertEqual(g.vida, 120)


if __name__ == "__main__":
    unittest.main()