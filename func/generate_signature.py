from func.register_probe import RegisterProbe
from cryptography.fernet import Fernet


class GenerateSignature(RegisterProbe):

    def __init__(self):
        pass

    def generate_signature(self, probe_index: int):
        try:
            probe_name = self.data_collected_probes[probe_index][0]
            date = self.data_collected_probes[probe_index][1]
            formatted_probe_local = self.probe_locals[probe_index]
            key = Fernet.generate_key()
            with open(f'{probe_name}/{formatted_probe_local[0]}{date}assinatura.txt', 'wb') as file:
                file.write(key)
            self.signature_collected_probes.append((probe_name, date))
            return True, ''
        except TypeError:
            return False, ''
