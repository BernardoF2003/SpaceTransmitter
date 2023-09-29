import socket
import threading
import errno
from time import sleep
from os import remove, system
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from func.register_probe import RegisterProbe


class CheckPublicKey(RegisterProbe):

    def __init__(self):
        pass

    def check_public_keys(self, probe_index: int):

        def send_public_key(probe):
            server_ip = '127.0.0.1'
            server_port = 23784
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((server_ip, server_port))
            print(f'Conectado a {server_ip}:{server_port}')
            sleep(1.5)
            with open(f'{probe}/{probe}.public.pem', 'rb') as file:
                while True:
                    data = file.read(4096)
                    if not data:
                        break
                    client_socket.send(data)
            client_socket.shutdown(socket.SHUT_WR)
            client_socket.close()

        def compare_public_key(probe):
            try:
                server_ip = "127.0.0.1"
                server_port = 23784
                server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_socket.bind((server_ip, server_port))
                server_socket.listen(1)
                server_socket.settimeout(10)
                try:
                    client_socket, client_address = server_socket.accept()
                except socket.timeout:
                    print("Timeout: No client connection received.")
                    return
                with open(f'server/{probe}/temp.public.pem', "wb") as file:
                    while True:
                        try:
                            data = client_socket.recv(4096)
                            if not data:
                                break
                            file.write(data)
                        except socket.error as e:
                            if e.errno == errno.EWOULDBLOCK:
                                print("Socket timeout: No data received.")
                                sleep(1)
                            else:
                                print(f"Socket error: {str(e)}")
                                sleep(1)
                            break
                client_socket.shutdown(socket.SHUT_WR)
                client_socket.close()
            except FileNotFoundError:
                pass

        try:
            system('cls')
            probe_name = self.signature_collected_probes[probe_index][0]
            server_thread = threading.Thread(target=send_public_key, args=(probe_name,))
            client_thread = threading.Thread(target=compare_public_key, args=(probe_name,))
            server_thread.start()
            client_thread.start()
            server_thread.join()
            client_thread.join()

            def load_public_key(file_path):
                with open(file_path, 'rb') as file:
                    public_key_pem = file.read()
                public_key = serialization.load_pem_public_key(public_key_pem, backend=default_backend())
                return public_key

            def compare_public_keys(client_file, server_file):
                public_key1 = load_public_key(client_file)
                public_key2 = load_public_key(server_file)
                if public_key1 == public_key2:
                    return True
                else:
                    return False

            file1 = f'server/{probe_name}/temp.public.pem'
            file2 = f'server/{probe_name}/{probe_name}.public.pem'
            print('Verificando chaves publicas...')
            sleep(1.2)
            if compare_public_keys(file1, file2):
                print("Chaves verificadas!")
                sleep(0.5)
                remove(file1)
                return True, ''
            else:
                remove(file1)
                return False, ''
        except TypeError:
            return False, ''
        except FileNotFoundError:
            return False, ''
