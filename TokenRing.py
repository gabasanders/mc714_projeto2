class TokenRing:
    def __init__(self,processes) -> None:
        self.processes = processes
        processes[0].token = 1


    def passToken(self,id):
        self.processes[id].token = 0

        if id == len(self.processes) - 1:
            self.processes[0].token = 1
        else:
            self.processes[id + 1].token = 1