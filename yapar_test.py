from YaPar_reader.yapar_reader import yaPar_reader
from YaPar_reader.SLR_simulater import SLR_simulate
from tools import *

if __name__ == '__main__':
    content = reader('./examples/slr-1.yalp')
    contentTry = reader('./out/tokens.txt')
    reader = yaPar_reader(content)
    reader.organize()
    print(reader.tokens)
    print(reader.productions)
    reader.LROrganize()
    # reader.graphLRO()
    reader.getSLRTable()
    SLR_simulate(contentTry, reader)




