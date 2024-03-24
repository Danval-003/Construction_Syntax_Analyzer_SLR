from YaPar_reader.yapar_reader import yaPar_reader
from tools import *

if __name__ == '__main__':
    content = reader('./examples/slr-1.yalp')
    reader = yaPar_reader(content)
    reader.organize()
    print(reader.tokens)
    print(reader.productions)
    reader.LROrganize()
    reader.getSLRTable()
