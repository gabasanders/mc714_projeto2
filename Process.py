from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import threading
import time

class Player:
    def __init__(self, id, addr, next_address, all_addr, auto = False, announce = False):
        self.id = id                        #Identificador
        self.token = False                  # Token 
        self.next_address = next_address    # Endereço do próximo processo
        self.announce = announce            # Determina se irá printar movimentos do token
        self.leader = False                 # Indica se é o líder
        self.clock = 0                      # Contador do processo
        self.all_addr = all_addr            # Lista de todos os endereços
        self.addr = addr                    # Endereço do processo
        self.auto = auto                    # Determina se irá fazer a jogada automaticamente

    # =============================  Token Ring  =================================

    def receive_token(self): # Recebe o token 
        self.token = True
        if self.announce:
            print(f"Jogador {self.id} recebeu o token.")
        
        if self.auto:

            self.make_move()

    def make_move(self): # Tenta fazer uma jogada
        if self.token:
            print(f"Jogador {self.id} realizou sua jogada.")
            self.update_clock()
            self.send_event()
            self.token = False
            self.pass_token()
        else:
            print(f"Espere por sua vez, Jogador {self.id}!")

    def pass_token(self):
        with xmlrpc.client.ServerProxy(self.next_address) as proxy:
            if self.announce:
                print(f"Jogador {self.id} passando o token.")
                print("")
            proxy.receive_token()

    # =============================  Lamport  =================================

    def update_clock(self):
        self.clock += 1

    def receive_event(self,sender_id,received_clock):
        self.clock = max(self.clock,received_clock) + 1
        print(f"Jogador {self.id} recebeu o evento do jogador {sender_id}")

    def send_event(self):
        for addr in self.all_addr:
            if addr != self.addr:
                with xmlrpc.client.ServerProxy(addr) as proxy:
                    proxy.receive_event(self.id, self.clock)