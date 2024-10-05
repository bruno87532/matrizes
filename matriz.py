import os
import sys
from prettytable import PrettyTable  # Para formatar a tabela

class Lanche:
    def __init__(self, nome, ingredientes, valores, mercado):
        self.nome = nome
        self.ingredientes = ingredientes
        self.valores = valores
        self.mercado = mercado

    def custo_total(self):
        return sum(self.valores)

    def custo_com_margem(self):
        return self.custo_total() * 1.7


class LancheRepository:
    FILENAME = "lanches.txt"

    @staticmethod
    def insere_lanche(lanche: Lanche):
        with open(LancheRepository.FILENAME, "a", encoding="utf-8") as arquivo:
            ingredientes_str = ",".join(lanche.ingredientes)
            valores_str = ",".join(map(str, lanche.valores))
            linha = f"{lanche.nome}|{ingredientes_str}|{valores_str}|{lanche.mercado}\n"
            arquivo.write(linha)

    @staticmethod
    def le_lanches():
        if not os.path.exists(LancheRepository.FILENAME):
            return []
        lanches_lidos = []
        with open(LancheRepository.FILENAME, "r", encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()
            for linha in linhas:
                nome, ingredientes_str, valores_str, mercado = linha.strip().split("|")
                ingredientes = ingredientes_str.split(",")
                valores = list(map(float, valores_str.split(",")))
                lanche = Lanche(nome, ingredientes, valores, mercado)
                lanches_lidos.append(lanche)
        return lanches_lidos


class Menu:
    def __init__(self):
        self.lanches = LancheRepository.le_lanches()

    def exibir_menu(self):
        print("\n=== Menu ===")
        print("1. Inserir novo lanche")
        print("2. Mostrar lanches")
        print("3. Sair")

    def obter_opcao(self):
        opcao = input("Escolha uma opção: ")
        return opcao

    def validar_nome(self, nome):
        if not nome.strip():
            print("O nome do lanche não pode estar vazio.")
            return False
        return True

    def validar_ingredientes(self, ingredientes):
        if not ingredientes or all(ing.strip() == "" for ing in ingredientes):
            print("É necessário fornecer pelo menos um ingrediente.")
            return False
        return True

    def validar_valores(self, valores):
        try:
            valores_float = [float(valor) for valor in valores]
            return valores_float
        except ValueError:
            print("Os valores devem ser números válidos.")
            return None

    def validar_mercado(self, mercado):
        if not mercado.strip():
            print("O nome do mercado não pode estar vazio.")
            return False
        return True

    def cadastrar_lanche(self):
        nome = input("Digite o nome do lanche: ")
        if not self.validar_nome(nome):
            return
        
        ingredientes = input("Digite os ingredientes separados por vírgula: ").split(",")
        if not self.validar_ingredientes(ingredientes):
            return
        
        valores = input("Digite os valores dos ingredientes separados por vírgula: ").split(",")
        valores_float = self.validar_valores(valores)
        if valores_float is None:
            return
        
        mercado = input("Digite o nome do mercado: ")
        if not self.validar_mercado(mercado):
            return
        
        lanche = Lanche(nome, ingredientes, valores_float, mercado)
        LancheRepository.insere_lanche(lanche)
        self.lanches.append(lanche)
        print("Lanche cadastrado com sucesso!")

    def mostrar_lanches(self):
        if not self.lanches:
            print("Nenhum lanche cadastrado.")
            return

        # Exibir detalhes dos lanches
        tabela = PrettyTable()
        tabela.field_names = ["Nome", "Ingredientes", "Valores", "Mercado"]
        for lanche in self.lanches:
            ingredientes_str = ", ".join(lanche.ingredientes)
            valores_str = ", ".join(map(str, lanche.valores))
            tabela.add_row([lanche.nome, ingredientes_str, valores_str, lanche.mercado])
        print(tabela)

        # Exibir custo total de cada lanche
        tabela_custo = PrettyTable()
        tabela_custo.field_names = ["Nome", "Custo Total"]
        for lanche in self.lanches:
            tabela_custo.add_row([lanche.nome, lanche.custo_total()])
        print("\nCusto Total dos Lanches:")
        print(tabela_custo)

        # Exibir custo total com margem de lucro
        tabela_margem = PrettyTable()
        tabela_margem.field_names = ["Nome", "Custo com Margem"]
        for lanche in self.lanches:
            tabela_margem.add_row([lanche.nome, lanche.custo_com_margem()])
        print("\nCusto Total com Margem de Lucro:")
        print(tabela_margem)

    def executar(self):
        while True:
            self.exibir_menu()
            opcao = self.obter_opcao()
            if opcao == "1":
                self.cadastrar_lanche()
            elif opcao == "2":
                self.mostrar_lanches()
            elif opcao == "3":
                print("Saindo...")
                sys.exit()
            else:
                print("Opção inválida!")


# Execução da aplicação
if __name__ == "__main__":
    menu = Menu()
    menu.executar()
