from os import system
from datetime import datetime
from func.register_probe import RegisterProbe


class ProbeData(RegisterProbe):

    def __init__(self):
        pass

    def probe_data(self, probe_index: int):
        system('cls')
        print('INSIRA OS DADOS DA SONDA\n'
              '=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*\n')
        probe_local = str(input('Local: '))
        formatted_probe_local = probe_local.replace(" ", "")
        while True:
            try:
                probe_temperature = int(input('Temperatura (°C): '))
            except ValueError:
                print("\n\033[0;31mDigite um valor numérico.\033[m\n")
            else:
                break
        while True:
            try:
                alpha_radiation = int(input('Radiação Alpha: '))
            except ValueError:
                print("\n\033[0;31mDigite um valor numérico.\033[m\n")
            else:
                break
        while True:
            try:
                beta_radiation = int(input('Radiação Beta: '))
            except ValueError:
                print("\n\033[0;31mDigite um valor numérico.\033[m\n")
            else:
                break
        while True:
            try:
                gamma_radiation = int(input('Radiação Gama: '))
            except ValueError:
                print("\n\033[0;31mDigite um valor numérico.\033[m\n")
            else:
                break
        today_date = datetime.today().strftime('%d.%m')
        with open(f'{self.probe_list[probe_index]}/{formatted_probe_local}{today_date}.txt', 'w') as file:
            file.write(f'local: {probe_local}\n'
                       f'temperatura: {probe_temperature}\n'
                       f'radiacao_alfa: {alpha_radiation}\n'
                       f'raidacao_beta: {beta_radiation}\n'
                       f'radiacao_gama: {gamma_radiation}')
        self.data_collected_probes.append((self.probe_list[probe_index], today_date))
        self.probe_locals.append((formatted_probe_local, self.probe_list[probe_index]))
        return True, ''
