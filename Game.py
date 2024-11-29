from TokenRing import TokenRing
from Process import ProcessClass

def makeMove(process):

    if process.token == 1:
        print("Success!")
        tr.passToken(process.id)
    else:
        print("Wait for your turn!")
        

p0 = ProcessClass(0)
p1 = ProcessClass(1)
processes = [p0,p1]

tr = TokenRing(processes)


makeMove(p1)
makeMove(p0)
makeMove(p0)
makeMove(p1)


