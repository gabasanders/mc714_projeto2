from Eleicao import *
from Process import Player
from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
from socketserver import ThreadingMixIn
import threading
import time

# Servidor com suporte a múltiplas threads
class ThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

# Inicia o servidor de um jogador
def init_server(player, host, port):
    server = ThreadedXMLRPCServer((host, port), allow_none=True)
    server.register_instance(player)
    print(f"Servidor do Jogador {player.id} rodando em {host}:{port}")
    server.serve_forever()



def auto():

    addr =["http://localhost:8000","http://localhost:8001","http://localhost:8002","http://localhost:8003"]

    # Adiciona jogadores
    p1 = Player(1, addr= addr[0], next_address=addr[1], all_addr=addr, announce= True,auto=True)
    p2 = Player(2, addr= addr[1], next_address=addr[2], all_addr=addr, announce= True,auto=True)
    p3 = Player(3, addr= addr[2], next_address=addr[3], all_addr=addr, announce= True,auto=True)
    p4 = Player(4, addr= addr[3], next_address=addr[0], all_addr=addr, announce= True,auto=True)

    players = [p1,p2,p3,p4]

    # Iniciar servidores RPC em threads separadas
    t1 = threading.Thread(target=init_server, args=(p1, "localhost", 8000))
    t2 = threading.Thread(target=init_server, args=(p2, "localhost", 8001))
    t3 = threading.Thread(target=init_server, args=(p3, "localhost", 8002))
    t4 = threading.Thread(target=init_server, args=(p4, "localhost", 8003)) 

    t1.start()
    t2.start()
    t3.start()
    t4.start()

    # Elege o primeiro lider
    leader = first_leader(players)

    # Passa a token para o lider
    with xmlrpc.client.ServerProxy(leader.addr) as proxy:
        proxy.receive_token()

def manual():
    
    addr =["http://localhost:8000","http://localhost:8001","http://localhost:8002","http://localhost:8003"]

    # Adiciona jogadores
    p1 = Player(1, addr= addr[0], next_address=addr[1], all_addr=addr, announce= True)
    p2 = Player(2, addr= addr[1], next_address=addr[2], all_addr=addr, announce= True)
    p3 = Player(3, addr= addr[2], next_address=addr[3], all_addr=addr, announce= True)
    p4 = Player(4, addr= addr[3], next_address=addr[0], all_addr=addr, announce= True)

    players = [p1,p2,p3,p4]

    # Iniciar servidores RPC em threads separadas
    t1 = threading.Thread(target=init_server, args=(p1, "localhost", 8000))
    t2 = threading.Thread(target=init_server, args=(p2, "localhost", 8001))
    t3 = threading.Thread(target=init_server, args=(p3, "localhost", 8002))
    t4 = threading.Thread(target=init_server, args=(p4, "localhost", 8003)) 

    t1.start()
    t2.start()
    t3.start()
    t4.start()


    # Elege o primeiro lider
    time.sleep(3)
    leader = first_leader(players)

    # Passa a token para o lider, que inicia a partida
    with xmlrpc.client.ServerProxy(leader.addr) as proxy:
        proxy.receive_token()

    print("Para movimentar o jogador i, digite: mi (Ex.: m1 faz o jogador 1 tentar se mover)")
    print("Para parar o processo i, digite: pi (Ex.: p1 para o processo i)")

    while True:

        entrada = input()

        if entrada[0] == 'm':
            players[int(entrada[1])].make_move()

        if entrada[0] == 'p':
            players[int(entrada[1])].status = 'Off'
            
            

        

if __name__ == "__main__":

    print("Defina o modo que deseja executar: Automático (1) ou Manual? (2)")
    modo = input()

    if modo == '1':
        auto()
    else:
        manual()

