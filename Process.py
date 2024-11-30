from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import sys
import threading
import time

class Player:
    def __init__(self, id, addr, all_addr, auto = False, announce = False):
        self.id = id                        # Identificador
        self.token = False                  # Token 
        self.next_process = 0               # Próximo processo
        self.announce = announce            # Determina se irá printar movimentos do token
        self.leader_addr = None             # Indica o endereço do líder
        self.clock = 0                      # Contador do processo
        self.all_addr = all_addr            # Lista de todos os endereços
        self.addr = addr                    # Endereço do processo
        self.auto = auto                    # Determina se irá fazer a jogada automaticamente
        self.status = 'On'                  # Indica se um processo está ativo ou inativo
        self.partner = None                 # Indica qual processo é seu companheiro de equipe.
        self.all_players = None             # Lista com todos os jogadores

    # =============================  Token Ring  =================================

    def receive_token(self): # Recebe o token 

        if self.status == 'On':

            self.token = True
            if self.announce:
                print(f"Jogador {self.id} recebeu o token.")
            
            if self.auto:
                self.make_move()

            print("Deu certo!")
            return 'ACK'
        
        if self.status == 'Off':

            return 'NACK'

    def make_move(self): # Tenta fazer uma jogada
        if self.status == 'On': # Verifica se o processo está ativo

            if self.token:  # Verifica se possui a token
                print(f"Jogador {self.id} realizou sua jogada.")
                self.update_clock()
                self.send_event()
                self.token = False
                self.pass_token()
                return 'ACK'
            else:
                print(f"Espere por sua vez, Jogador {self.id}!")
                return 'ACK'

    def pass_token(self):
        with xmlrpc.client.ServerProxy(self.next_process.addr) as proxy:    # Tenta passar o token para o próximo
            if self.announce:
                print(f"Jogador {self.id} tanta passar o token.")
                print("")
            if proxy.receive_token() == 'NACK':                             # Se não consegue, avisa o líder
                print(f"Jogador {self.id} não consegue pessar o token.")
                print(f"Jogador {self.id} avisa ao líder")

                with xmlrpc.client.ServerProxy(self.leader_addr) as proxy:
                    if proxy.restore_token(self.next_process.id,self.next_process.partner.addr) == 'NACK':
                        print(f"Líder não respondeu. Processo {self.id} iniciando eleição...")
                        self.call_election()

                        with xmlrpc.client.ServerProxy(self.leader_addr) as proxy:
                            proxy.restore_token(self.next_process.id,self.next_process.partner.addr)

    # =============================  Lamport  =================================
    def update_clock(self):
        self.clock += 1

    def receive_event(self,sender_id,received_clock):
        if self.status == 'On':
            self.clock = max(self.clock,received_clock) + 1
            print(f"Jogador {self.id} recebeu o evento do jogador {sender_id}")
            return 'ACK'
        else:
            print(f"Jogador {self.id} não recebeu o evento do jogador {sender_id}")
            return 'NACK'

    def send_event(self):
        for addr in self.all_addr:
            if addr != self.addr:
                with xmlrpc.client.ServerProxy(addr) as proxy:
                    proxy.receive_event(self.id, self.clock)

    # =========================== Eleição =================================
    
    def update_leader(self,leader):
        if self.status == 'On':
            self.leader_addr = leader
            return 'ACK'
        else:
            return 'NACK'
        
    def announce_lidership(self):
        print(f"Processo {self.id} escolhido como líder.")
        print(f"Anunciando aos outros processos...")

        for addr in self.all_addr:
            if addr != self.addr:
                with xmlrpc.client.ServerProxy(addr) as proxy:
                    proxy.update_leader(self.addr)

    def restore_token(self,failed_process_id,failed_process_partner):
        if self.status == 'On':
            with xmlrpc.client.ServerProxy(failed_process_partner) as proxy:    # Tenta passar o token para o próximo
                print(f"Líder tenta passar o token para o parceiro do Processo {failed_process_id}")
                print("")
                if proxy.receive_token() == 'NACK':
                    print("Um time inteiro está desconectado. Encerrando a partida...")
                    sys.exit(0)
                else:
                    return 'ACK'
            
        else:
            return 'NACK'

    def check_online(self):
        if self.status == 'On':
            return 'ACK'
        else:
            return 'NACK'

    def call_election(self):
        print(f"Processo {self.id} enviando mensagem de eleição...")
        for process in self.all_players:
            if process.id > self.id:
                with xmlrpc.client.ServerProxy(process.addr) as proxy:
                        if proxy.check_online() == 'ACK':
                            print(f"Processo {process.id} respondeu!")
                            proxy.call_election()
                            return False
        print('Nenhum outro processo com id maior respondeu.')
        self.announce_lidership()
        return 'ACK'
                            

