from func.main_menu import MainMenu
from func.register_probe import RegisterProbe
from func.send_public_key import SendPublicKey
from func.probe_data import ProbeData
from func.generate_signature import GenerateSignature
from func.check_public_key import CheckPublicKey
from func.send_data import SendData
from func.delete_probe import DeleteProbe
from os import system

if __name__ == "__main__":
    system('cls')
    rp = RegisterProbe()
    dp = DeleteProbe()
    sp = SendPublicKey()
    pb = ProbeData()
    gs = GenerateSignature()
    ck = CheckPublicKey()
    sd = SendData()
    while True:
        try:
            option = MainMenu.select_option()
            if option == 1:
                rp.generate_keys()
            elif option == 2:
                probe_index = rp.select_probe(rp.probe_list)
                if probe_index[0]:
                    temp = sp.sp_main(probe_index[1])
                    if temp[0]:
                        system('cls')
                        print(f"\033[0;32mChaves da sonda \033[m{temp[1]} \033[0;32menviadas com sucesso\033[m\n")
                    else:
                        system('cls')
                        print("\033[0;31mNenhuma sonda encontrada.\033[m\n")
                else:
                    system('cls')
                    print("\033[0;31mNenhuma sonda cadastrada.\033[m\n")
            elif option == 3:
                probe_index = rp.select_probe(rp.probe_list)
                if probe_index[0]:
                    temp = pb.probe_data(probe_index[1])
                    if temp[0]:
                        system('cls')
                        print(f"\033[0;32mDados coletados com sucesso.\033[m\n")
                    else:
                        system('cls')
                        print("\n\033[0;31mErro ao coletar dados.\033[m\n")
                else:
                    system('cls')
                    print("\033[0;31mNenhuma sonda cadastrada.\033[m\n")
            elif option == 4:
                probe_index = rp.select_probe(rp.data_collected_probes)
                if probe_index[0]:
                    temp = gs.generate_signature(probe_index[1])
                    if temp[0]:
                        system('cls')
                        print(f"\033[0;32mAssinatura gerada com sucesso\033[m\n")
                    else:
                        system('cls')
                        print("\033[0;31mNenhuma sonda encontrada.\033[m\n")
                else:
                    system('cls')
                    print("\033[0;31mNenhum dado foi coletado.\033[m\n")
            elif option == 5:
                probe_index = rp.select_probe(rp.signature_collected_probes)
                if probe_index[0]:
                    try:
                        temp = ck.check_public_keys(probe_index[1])
                        if temp[0]:
                            temp = sd.send_data(probe_index[1])
                            if temp[0]:
                                system('cls')
                                print(f"\033[0;32mDados enviados com sucesso!\033[m\n")
                            else:
                                system('cls')
                                print("\033[0;31mErro ao enviar dados.\033[m\n")
                        else:
                            system('cls')
                            print("\033[0;31mAs chaves não coincidem.\033[m\n")
                    except Exception as e:
                        system('cls')
                        print(e)
                else:
                    system('cls')
                    print("\033[0;31mNenhuma sonda encontrada.\033[m\n")
            elif option == 6:
                probe_index = rp.select_probe(rp.probe_list)
                if probe_index[0]:
                    temp = dp.delete_probe(probe_index[1])
                    if temp[0]:
                        system('cls')
                        print(f"\033[0;32mSonda\033[m {temp[1]} \033[0;32mdeletada com sucesso\033[m\n")
                    else:
                        system('cls')
                        print("\033[0;31mErro ao deletar sonda.\033[m\n")
                else:
                    system('cls')
                    print("\033[0;31mNenhuma sonda encontrada.\033[m\n")
            elif option == 7:
                system('cls')
                break
            else:
                system('cls')
                print("\033[0;31mDigite uma opção válida.\033[m\n")
        except IndexError:
            system('cls')
            print("\033[0;31mDigite uma opção válida.\033[m\n")
