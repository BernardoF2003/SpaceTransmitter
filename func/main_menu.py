from os import system


class MainMenu:
    def __init__(self):
        pass

    @staticmethod
    def select_option() -> int:
        try:
            print("                 Menu Principal       "
                  "\n\n*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*"
                  "\n\n1 - Cadastrar Sonda e Gerar Par de Chaves"
                  "\n2 - Enviar Chave da Sonda"
                  "\n3 - Coletar Dados da Sonda"
                  "\n4 - Gerar Assinatura dos dados Coletados"
                  "\n5 - Enviar para a terra os dados"
                  "\n6 - Apagar sonda"
                  "\n7 - Sair")
            option = int(input("\n>> "))
            return option
        except ValueError:
            system('cls')
            print("\033[0;31mDigite uma opção válida.\033[m\n")
