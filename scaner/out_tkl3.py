from typing import *


import argparse
parser = argparse.ArgumentParser(description='Simulate a machine')
parser.add_argument('source', help='Source file')

parser.add_argument('-o', help='Output file', default='a.out')
fileOut = parser.parse_args().o
with open(fileOut, 'w') as archivo:
    # Escribe datos en el archivo
    archivo.write("")


class State:
    def __init__(self, value: str) -> None:
        self.value: str = value
        self.transitions: Dict[str or int, Set['State']] = {}
        self.isFinalState: bool = False
        self.numTrans: int = 0

    def add_transition(self, value: str or int, state: 'State') -> None:
        if value in self.transitions:
            self.transitions[value].add(state)
        else:
            self.transitions[value] = {state}

        self.numTrans += 1

    def getStates(self, transition_value) -> Set['State']:
        return self.transitions[transition_value] if transition_value in self.transitions else set()

    def __eq__(self, other):
        if isinstance(other, State):
            return (self.value, id(self)) == (other.value, id(self))
        return False

    def __hash__(self):
        return hash((self.value, id(self)))

    def getToken(self) -> str or None:
        return str(list(self.token)[0]) if len(self.token) > 0 else None

    def numberTransitions(self) -> int:
        return self.numTrans
        



f1 = State('f1')
e1 = State('e1')
d1 = State('d1')
c1 = State('c1')
b6 = State('b6')
b1 = State('b1')
b5 = State('b5')
b2 = State('b2')
b3 = State('b3')
b4 = State('b4')
a1 = State('a1')
a0 = State('a0')
a0.add_transition(32, a1)
a0.add_transition(9, a1)
a0.add_transition(10, a1)
a0.add_transition(48, b4)
a0.add_transition(49, b4)
a0.add_transition(50, b4)
a0.add_transition(51, b4)
a0.add_transition(52, b4)
a0.add_transition(53, b4)
a0.add_transition(54, b4)
a0.add_transition(55, b4)
a0.add_transition(56, b4)
a0.add_transition(57, b4)
a0.add_transition(43, c1)
a0.add_transition(42, d1)
a0.add_transition(40, e1)
a0.add_transition(41, f1)

a1.isFinalState = True


def tk_a1(): 
	with open(fileOut, 'a') as archivo:
	    # Escribe datos en el archivo
	    archivo.write("WHITESPACE ")


a1.token = tk_a1
a1.add_transition(32, a1)
a1.add_transition(9, a1)
a1.add_transition(10, a1)

b4.isFinalState = True


def tk_b4(): 
	with open(fileOut, 'a') as archivo:
	    # Escribe datos en el archivo
	    archivo.write("NUMBER ")


b4.token = tk_b4
b4.add_transition(69, b3)
b4.add_transition(46, b1)
b4.add_transition(48, b4)
b4.add_transition(49, b4)
b4.add_transition(50, b4)
b4.add_transition(51, b4)
b4.add_transition(52, b4)
b4.add_transition(53, b4)
b4.add_transition(54, b4)
b4.add_transition(55, b4)
b4.add_transition(56, b4)
b4.add_transition(57, b4)

b3.add_transition(43, b2)
b3.add_transition(45, b2)
b3.add_transition(48, b5)
b3.add_transition(49, b5)
b3.add_transition(50, b5)
b3.add_transition(51, b5)
b3.add_transition(52, b5)
b3.add_transition(53, b5)
b3.add_transition(54, b5)
b3.add_transition(55, b5)
b3.add_transition(56, b5)
b3.add_transition(57, b5)

b2.add_transition(48, b5)
b2.add_transition(49, b5)
b2.add_transition(50, b5)
b2.add_transition(51, b5)
b2.add_transition(52, b5)
b2.add_transition(53, b5)
b2.add_transition(54, b5)
b2.add_transition(55, b5)
b2.add_transition(56, b5)
b2.add_transition(57, b5)

b5.isFinalState = True


def tk_b5(): 
	with open(fileOut, 'a') as archivo:
	    # Escribe datos en el archivo
	    archivo.write("NUMBER ")


b5.token = tk_b5
b5.add_transition(48, b5)
b5.add_transition(49, b5)
b5.add_transition(50, b5)
b5.add_transition(51, b5)
b5.add_transition(52, b5)
b5.add_transition(53, b5)
b5.add_transition(54, b5)
b5.add_transition(55, b5)
b5.add_transition(56, b5)
b5.add_transition(57, b5)

b1.add_transition(48, b6)
b1.add_transition(49, b6)
b1.add_transition(50, b6)
b1.add_transition(51, b6)
b1.add_transition(52, b6)
b1.add_transition(53, b6)
b1.add_transition(54, b6)
b1.add_transition(55, b6)
b1.add_transition(56, b6)
b1.add_transition(57, b6)

b6.isFinalState = True


def tk_b6(): 
	with open(fileOut, 'a') as archivo:
	    # Escribe datos en el archivo
	    archivo.write("NUMBER ")


b6.token = tk_b6
b6.add_transition(69, b3)
b6.add_transition(48, b6)
b6.add_transition(49, b6)
b6.add_transition(50, b6)
b6.add_transition(51, b6)
b6.add_transition(52, b6)
b6.add_transition(53, b6)
b6.add_transition(54, b6)
b6.add_transition(55, b6)
b6.add_transition(56, b6)
b6.add_transition(57, b6)

c1.isFinalState = True


def tk_c1(): 
	with open(fileOut, 'a') as archivo:
	    # Escribe datos en el archivo
	    archivo.write("PLUS ")


c1.token = tk_c1

d1.isFinalState = True


def tk_d1(): 
	with open(fileOut, 'a') as archivo:
	    # Escribe datos en el archivo
	    archivo.write("TIMES ")


d1.token = tk_d1

e1.isFinalState = True


def tk_e1(): 
	with open(fileOut, 'a') as archivo:
	    # Escribe datos en el archivo
	    archivo.write("LPAREN ")


e1.token = tk_e1

f1.isFinalState = True


def tk_f1(): 
	with open(fileOut, 'a') as archivo:
	    # Escribe datos en el archivo
	    archivo.write("RPAREN ")


f1.token = tk_f1


args = parser.parse_args()
fileToRead = args.source
def exclusiveSim(initState: State, string: str):
    string += ' '
    paths: List[List[State]] = [[initState]]
    listTextTuple: List[Tuple[str, str or int]] = []
    lastPathAccepted: List[Tuple[int, List, int]] = []

    chIndex = 0
    lasChIndex = 0

    while chIndex < len(string):
        ch = string[chIndex]
        char = ord(ch)
        newPaths: List[List[State]] = []

        for path in paths:
            evalState: State = path[-1]

            for st in evalState.getStates(char):
                newPath = path.copy()
                newPath.append(st)
                newPaths.append(newPath)

        if len(newPaths) == 0:
            if len(lastPathAccepted) == 0:
                textToAccept = string[lasChIndex:chIndex + 1]
                listTextTuple.append((textToAccept, 0 if len(textToAccept) == 0 or textToAccept == ' ' else 1))
                chIndex += 1
                lasChIndex = chIndex
                paths = [[initState]]
                continue

            lastChar, lastStateAccepted, _ = lastPathAccepted[0]
            textToAccept = string[lasChIndex:lastChar + 1]
            listTextTuple.append((textToAccept, lastStateAccepted[-1].token))
            lasChIndex = lastChar + 1
            chIndex = lastChar + 1
            paths = [[initState]]
            lastPathAccepted = []
            continue

        newLastPathAccepted = []

        for path in newPaths:
            if path[-1].isFinalState:
                newLastPathAccepted.append(
                    (chIndex, path, path[-1].value))

        if len(newLastPathAccepted) > 0:
            lastPathAccepted = sorted(newLastPathAccepted, key=lambda x: x[2])

        paths = newPaths
        chIndex += 1

    return listTextTuple


CYAN = '\033[96m'
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
WHITE = '\033[97m'
RESET = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
REVERSE = '\033[7m'


if __name__ == '__main__':
    with open(fileToRead, 'r') as file:
        contents = file.read()

    print(YELLOW, 'Resultado:', RESET)
    tokens = exclusiveSim(a0, contents)
    for message, token in tokens:
        if token != 1 and token != 0:
            print(GREEN, message, RESET, '->')
            token()
        elif token == 1:
            print(RED, 'ERROR IN LINE:', message, RESET)
        