class Batalha:

    def __init__(self, jogador, inimigo):
        self.jogador = jogador
        self.inimigo = inimigo

    def iniciar(self):
        """Executa a batalha e retorna 'vitoria', 'derrota' ou 'fuga'."""

        print("=" * 40)
        print("        INÍCIO DA BATALHA")
        print("=" * 40)

        tem_magia = hasattr(self.jogador, "usar_magia")

        while self.jogador.esta_vivo() and self.inimigo.esta_vivo():

            print("\n--- STATUS ---")
            self.jogador.mostrar_status()
            self.inimigo.mostrar_status()

            print("\n--- AÇÕES ---")
            print("1 - Atacar")
            print("2 - Usar item")
            print("3 - Fugir")
            if tem_magia:
                print("4 - Usar magia")

            opcao = input("Escolha uma opção: ").strip()

            if opcao == "1":
                self.jogador.atacar(self.inimigo)

            elif opcao == "2":
                if not self._usar_item():
                    continue  # ação cancelada/inválida não gasta o turno

            elif opcao == "3":
                print("Você fugiu da batalha!")
                return "fuga"

            elif opcao == "4" and tem_magia:
                if self.jogador.mana < self.jogador.CUSTO_MAGIA:
                    self.jogador.usar_magia(self.inimigo)  # só avisa
                    continue
                self.jogador.usar_magia(self.inimigo)

            else:
                print("Opção inválida.")
                continue

            # Turno do inimigo (somente se ainda estiver vivo)
            if self.inimigo.esta_vivo():
                print()
                self.inimigo.atacar(self.jogador)

        return self._verificar_vencedor()

    def _usar_item(self):
        """Mostra o inventário e usa o item escolhido. Retorna True se gastou o turno."""
        inventario = self.jogador.inventario

        if not inventario:
            print("Você não possui itens.")
            return False

        print("\n--- INVENTÁRIO ---")
        for i, item in enumerate(inventario, start=1):
            print(f"{i} - {item.nome}")
        print("0 - Voltar")

        escolha = input("Escolha um item: ").strip()

        if not escolha.isdigit() or not (1 <= int(escolha) <= len(inventario)):
            print("Item cancelado ou inválido.")
            return False

        item = inventario.pop(int(escolha) - 1)
        item.usar(self.jogador)
        return True

    def _verificar_vencedor(self):
        print("\n" + "=" * 40)
        if self.jogador.esta_vivo():
            print(f"VITÓRIA! {self.inimigo.nome} foi derrotado!")
            resultado = "vitoria"
        else:
            print(f"DERROTA... {self.jogador.nome} caiu em batalha.")
            resultado = "derrota"
        print("=" * 40)
        return resultado