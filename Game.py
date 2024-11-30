from Election import *
from TokenRing import *
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

def config_game(players):

    # Prepara o ambiente do jogo
    init_token_ring(players)

    # Define as duplas
    players[0].partner = players[2]
    players[1].partner = players[3]
    players[2].partner = players[0]
    players[3].partner = players[1]

    # Avisa todos os jogadores de todos os outros jogadores
    for player in players:
        player.all_players = players

def auto():

    addr =["http://localhost:8000","http://localhost:8001","http://localhost:8002","http://localhost:8003"]

    # Adiciona jogadores
    p0 = Player(0, addr= addr[0], all_addr=addr, announce= True,auto=True)
    p1 = Player(1, addr= addr[1], all_addr=addr, announce= True,auto=True)
    p2 = Player(2, addr= addr[2], all_addr=addr, announce= True,auto=True)
    p3 = Player(3, addr= addr[3], all_addr=addr, announce= True,auto=True)

    players = [p0,p1,p2,p3]

    # Iniciar servidores RPC em threads separadas
    t0 = threading.Thread(target=init_server, args=(p0, "localhost", 8000))
    t1 = threading.Thread(target=init_server, args=(p1, "localhost", 8001))
    t2 = threading.Thread(target=init_server, args=(p2, "localhost", 8002))
    t3 = threading.Thread(target=init_server, args=(p3, "localhost", 8003)) 

    t0.start()
    t1.start()
    t2.start()
    t3.start()

    config_game(players)

def manual():
    
    addr =["http://localhost:8000","http://localhost:8001","http://localhost:8002","http://localhost:8003"]

    # Adiciona jogadores
    p0 = Player(0, addr= addr[0], all_addr=addr, announce= True)
    p1 = Player(1, addr= addr[1], all_addr=addr, announce= True)
    p2 = Player(2, addr= addr[2], all_addr=addr, announce= True)
    p3 = Player(3, addr= addr[3], all_addr=addr, announce= True)

    players = [p0,p1,p2,p3]

    # Iniciar servidores RPC em threads separadas
    t0 = threading.Thread(target=init_server, args=(p0, "localhost", 8000))
    t1 = threading.Thread(target=init_server, args=(p1, "localhost", 8001))
    t2 = threading.Thread(target=init_server, args=(p2, "localhost", 8002))
    t3 = threading.Thread(target=init_server, args=(p3, "localhost", 8003)) 

    t0.start()
    t1.start()
    t2.start()
    t3.start()

    config_game(players)

    print("COMANDOS:")
    print("     mi: jogador i faz um movimento")
    print("     pi: para o processo i")

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

