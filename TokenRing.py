from  Election import *

def init_token_ring(processes):

    print("Inicializando Token Ring")

    n = len(processes)

    for i in range(n):      # Define os sucessores de cada processo
        if i == n - 1:
            processes[i].next_process = processes[0]
            print(f"Processo {processes[i].id} --> Processo {processes[0].id}")
        else:
            processes[i].next_process = processes[i+1]
            print(f"Processo {processes[i].id} --> Processo {processes[i+1].id}")

    print(" ")
    
    # Define o líder
    leader = first_leader(processes)

    # Passa a token para o lider, que inicia a partida
    with xmlrpc.client.ServerProxy(leader.addr) as proxy:
        proxy.receive_token()
    
    return 