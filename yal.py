import argparse
from yalexRead.yalex_reader import *


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compile a program')
    parser.add_argument('source', help='Source file')
    parser.add_argument('-o', help='Output file', default='')
    args = parser.parse_args()
    content = reader(args.source)
    ev = eval_Text(content)
    for tk, m in ev:
        if tk == 1:
            raise Exception('Error in', m)

    if getTotal() == 0:
        raise Exception('No tokens found')

    codes = create_mach(False, args.o)

    for files in codes:
        print('- File:', files)



