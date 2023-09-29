from rsa import newkeys
from os import path, makedirs, system


class RegisterProbe:
    probe_list = []
    data_collected_probes = []
    probe_locals = []
    signature_collected_probes = []

    def __init__(self):
        pass

    def generate_keys(self):
        system('cls')
        probe_name = str(input("Nome da sonda: "))
        if path.exists(f"{probe_name}"):
            system('cls')
            print(f"\n\033[0;31mJa existe uma sonda\033[m {probe_name}, \033[0;31m, "
                  f"por favor selecione novamente.\033[m\n")
        else:
            print('Gerando chaves...')
            key = newkeys(2048)
            public_key = key[0]
            private_key = key[1]
            folder_path = path.join(probe_name)
            makedirs(folder_path)
            private_key_file = path.join(folder_path, f"{probe_name}.private.pem")
            public_key_file = path.join(folder_path, f"{probe_name}.public.pem")
            with open(private_key_file, "wb") as private_file:
                private_file.write(private_key.save_pkcs1(format='PEM'))
            with open(public_key_file, "wb") as public_file:
                public_file.write(public_key.save_pkcs1(format='PEM'))
            self.probe_list.append(probe_name)
            system('cls')
            print(f"\033[0;32mChave pública e privada salvas em /{folder_path}\n\033[m")

    def select_probe(self, lista):
        if len(lista) < 1:
            print("\n\033[0;31mNenhuma sonda cadastrada.\033[m\n")
            return False, ''
        else:
            system('cls')
            print('SELECIONE UMA SONDA\n'
                  '=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*\n')
            for i, probe in enumerate(lista):
                if isinstance(probe, tuple):
                    print(f'{i} - {probe[0].title()}')
                else:
                    print(f'{i} - {probe.title()}')
            try:
                while True:
                    option = int(input("\n>> "))
                    if option > len(lista) - 1 or option < 0:
                        print("\n\033[0;31mDigite uma opção válida.\033[m\n")
                    else:
                        break
                return True, option
            except ValueError:
                print("\n\033[0;31mDigite uma opção válida.\033[m\n")
                return False, ''
