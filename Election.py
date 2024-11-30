
import xmlrpc.client

def first_leader(processes):

    print(f"Definindo líder...")
    id_max = 0

    for process in processes:
        if process.id > id_max:
            id_max = process.id
            leader = process
    
    leader.announce_lidership()
    
    return leader



