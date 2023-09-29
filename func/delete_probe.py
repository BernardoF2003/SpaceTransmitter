from os import system
from func.register_probe import RegisterProbe


class DeleteProbe(RegisterProbe):
    def __init__(self):
        pass

    def delete_probe(self, probe_index: int):
        try:
            system('cls')
            system(f'rmdir /s /q {self.probe_list[probe_index]}')
            temp = self.probe_list[probe_index]
            self.probe_list.remove(temp)
            for i in reversed(range(len(self.probe_locals))):
                if self.probe_locals[i][1] == temp:
                    del self.probe_locals[i]
            for i in reversed(range(len(self.data_collected_probes))):
                if self.data_collected_probes[i][0] == temp:
                    del self.data_collected_probes[i]
            for i in reversed(range(len(self.signature_collected_probes))):
                if self.signature_collected_probes[i][0] == temp:
                    del self.signature_collected_probes[i]
            return True, temp
        except ValueError or IndexError:
            print("\n\033[0;31mDigite uma opção válida.\033[m\n")
            return False, ''
        except TypeError:
            return False, ''
