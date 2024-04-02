import argparse

from YaPar_reader.SLR_simulater import SLR_simulate
from YaPar_reader.yapar_reader import yaPar_reader
from tools import *
import pickle

if __name__ == '__main__':
    content = reader('.\examples\slr-4.yalp')
    reader2 = yaPar_reader(content)
    reader2.organize()
    reader2.LROrganize()
    # reader.graphLRO()
    tableSlr = reader2.getSLRTable()
    otherContent = reader('./out/tokens4.txt')
    SLR_simulate(otherContent, tableSlr)
