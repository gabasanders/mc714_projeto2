
import xmlrpc.client


def first_leader(processes):

    id_max = 0

    for process in processes:
        if process.id > id_max:
            id_max = process.id
            leader = process
    
    print(f"Processo {leader.id} escolhido como líder.")
    print(f"Anunciando aos outros processos...")
    leader.announce_lidership()
    
    return leader

