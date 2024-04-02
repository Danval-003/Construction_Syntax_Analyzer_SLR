import argparse
import pickle
import subprocess
from YaPar_reader.SLR_simulater import SLR_simulate
from YaPar_reader.yapar_reader import yaPar_reader
from tools.Reader import reader

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compile a program')
    parser.add_argument('source', help='Source file')
    parser.add_argument('-scan', help='Scan file', default=None)
    parser.add_argument('-oScan', help='Output scan file', default=None)
    parser.add_argument('-yapar', help='Yapar object file', default=None)
    args = parser.parse_args()

    if args.scan is None or args.oScan is None or args.yapar is None:
        raise Exception('You must provide the scan, output scan and yapar object files')

    readTokensCommand = ['python', args.scan, args.source, '-o', args.oScan]
    subprocess.run(readTokensCommand)
    # reader.graphLRO()
    with open(args.yapar, 'rb') as yaparFile:
        tableSLR = pickle.load(yaparFile)

    print('Producciones:')
    print(tableSLR.product_list_toPrint)

    content = reader(args.oScan)
    print(args.oScan, content)

    SLR_simulate(content, tableSLR)




