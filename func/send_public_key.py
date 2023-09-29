import socket
import threading
from func.register_probe import RegisterProbe
from os import system, makedirs
import errno
from time import sleep


class SendPublicKey(RegisterProbe):
    def __init__(self):
        pass

    def sp_main(self, probe_index: int):

        def send_public_key(probe):
            server_ip = '127.0.0.1'
            server_port = 23784
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((server_ip, server_port))
            with open(f'{probe}/{probe}.public.pem', 'rb') as file:
                while True:
                    data = file.read(4096)
                    if not data:
                        break
                    client_socket.send(data)
            print("Chave pública enviada com sucesso.")
            sleep(1)
            client_socket.shutdown(socket.SHUT_WR)
            client_socket.close()

        def receive_public_key(probe):
            server_ip = "127.0.0.1"
            server_port = 23784
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((server_ip, server_port))
            server_socket.listen(1)
            print(f"Conectado a {server_ip}:{server_port}")
            sleep(1)
            server_socket.settimeout(10)
            try:
                client_socket, client_address = server_socket.accept()
            except socket.timeout:
                print("Timeout: No client connection received.")
                sleep(1)
                return
            directory = f'server/{probe}'
            makedirs(directory, exist_ok=True)
            with open(f'{directory}/{probe}.public.pem', "wb") as file:
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
            print(f"Chave pública recebida e armazenada em {directory}/{probe_name}.public.pem")
            sleep(2.2)
            client_socket.shutdown(socket.SHUT_WR)
            client_socket.close()
        try:
            probe_name = self.probe_list[probe_index]
            system('cls')
            server_thread = threading.Thread(target=send_public_key, args=(probe_name,))
            client_thread = threading.Thread(target=receive_public_key, args=(probe_name,))
            server_thread.start()
            client_thread.start()
            server_thread.join()
            client_thread.join()
            return True, probe_name
        except TypeError:
            return False, ''
