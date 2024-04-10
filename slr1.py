
import argparse
import pickle
import subprocess
from YaPar_reader.SLR_simulater import SLR_simulate
from YaPar_reader.yapar_reader import yaPar_reader
from tools.Reader import reader    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compile a program')
    parser.add_argument('-oScan', help='Output scan file', default=None)
    args = parser.parse_args()
    with open(".\out\yaPar.pkl", 'rb') as yaparFile:
        tableSLR = pickle.load(yaparFile)
        
    content = reader(args.oScan)
    SLR_simulate(content, tableSLR)
    
    