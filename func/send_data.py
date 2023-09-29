import socket
import threading
from time import sleep
from os import remove
import errno
from cryptography.fernet import Fernet
from func.register_probe import RegisterProbe


class SendData(RegisterProbe):

    def __init__(self):
        pass

    def send_data(self, probe_index: int):

        def send_data_file(probe):
            server_ip = '127.0.0.1'
            server_port = 23784
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((server_ip, server_port))
            with open(f'{probe}/{formatted_probe_local[0]}{date}.txt', 'r') as data_file:
                while True:
                    data = data_file.read(1024)
                    if not data:
                        break
                with open(f'{probe}/{formatted_probe_local[0]}{date}assinatura.txt', 'rb') as key_file:
                    encryption_key = key_file.read(1024)
                fernet_key = Fernet(encryption_key)
                with open(f'{probe}/{formatted_probe_local[0]}{date}.txt', 'rb') as probe_file:
                    probe_data = probe_file.read()
                    encrypted_data = fernet_key.encrypt(probe_data)
                client_socket.send(encrypted_data)
            client_socket.shutdown(socket.SHUT_WR)
            client_socket.close()

        def receive_data(probe):
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
            with open(f'server/{probe}/{formatted_probe_local[0]}{date}.txt', "wb") as file:
                while True:
                    try:
                        data = client_socket.recv(1024)
                        if not data:
                            break
                        file.write(data)
                    except socket.error as e:
                        if e.errno == errno.EWOULDBLOCK:
                            print("Socket timeout: No data received.")
                        else:
                            print(f"Socket error: {str(e)}")
                        break
            client_socket.shutdown(socket.SHUT_WR)
            client_socket.close()

        try:
            probe_name = self.signature_collected_probes[probe_index][0]
            date = self.signature_collected_probes[probe_index][1]
            formatted_probe_local = self.probe_locals[probe_index]
            server_thread = threading.Thread(target=send_data_file, args=(probe_name,))
            client_thread = threading.Thread(target=receive_data, args=(probe_name,))
            server_thread.start()
            client_thread.start()
            server_thread.join()
            client_thread.join()

            def send_signature(probe):
                server_ip = '127.0.0.1'
                server_port = 23784
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((server_ip, server_port))
                with open(f'{probe}/{formatted_probe_local[0]}{date}assinatura.txt', 'rb') as file:
                    while True:
                        data = file.read(1024)
                        if not data:
                            break
                        client_socket.send(data)
                client_socket.shutdown(socket.SHUT_WR)
                client_socket.close()

            def receive_signature(probe):
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
                with open(f'server/{probe}/temp_assinatura.txt', "wb") as signature:
                    while True:
                        try:
                            data = client_socket.recv(1024)
                            if not data:
                                break
                            signature.write(data)
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

            try:
                probe_name = self.signature_collected_probes[probe_index][0]
                server_thread = threading.Thread(target=send_signature, args=(probe_name,))
                client_thread = threading.Thread(target=receive_signature, args=(probe_name,))
                server_thread.start()
                client_thread.start()
                server_thread.join()
                client_thread.join()
                with open(f'server/{probe_name}/temp_assinatura.txt', 'rb') as sent_key_file:
                    key = sent_key_file.read()
                with open(f'server/{probe_name}/{formatted_probe_local[0]}{date}.txt', 'rb') as encrypted_file:
                    encrypted_text = encrypted_file.read()
                    cipher_suite = Fernet(key)
                    decrypted_text = cipher_suite.decrypt(encrypted_text)
                with open(f'server/{probe_name}/{formatted_probe_local[0]}{date}.txt', 'wb') as decrypted_data_file:
                    decrypted_data_file.write(decrypted_text)
                remove(f'server/{probe_name}/temp_assinatura.txt')
                return True, ''
            except TypeError:
                probe_name = self.signature_collected_probes[probe_index][0]
                date = self.signature_collected_probes[probe_index][1]
                formatted_probe_local = self.probe_locals[probe_index]
                remove(f'server/{probe_name}/{formatted_probe_local[0]}{date}.txt')
                remove(f'server/{probe_name}/temp_assinatura.txt')
                return False, ''
        except TypeError:
            probe_name = self.signature_collected_probes[probe_index][0]
            date = self.signature_collected_probes[probe_index][1]
            formatted_probe_local = self.probe_locals[probe_index]
            remove(f'server/{probe_name}/{formatted_probe_local[0]}{date}.txt')
            return False, ''
