import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compile a program')
    parser.add_argument('source', help='Source file')
    parser.add_argument('-o', help='Output file', default='a.out')
    args = parser.parse_args()
    print(args.source)
    print(args.o)