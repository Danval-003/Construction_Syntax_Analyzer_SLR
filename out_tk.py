from typing import *


class State:
    def __init__(self, value: str) -> None:
        self.value: str = value
        self.transitions: Dict[str or int, Set['State']] = {}
        self.isFinalState: bool = False
        self.token: Set[str] = set()
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

    def addToken(self, tk: str):
        self.token.add(tk)

    def getToken(self) -> str or None:
        return str(list(self.token)[0]) if len(self.token) > 0 else None

    def numberTransitions(self) -> int:
        return self.numTrans


f4 = State('f4')
f3 = State('f3')
f2 = State('f2')
f1 = State('f1')
e2 = State('e2')
e1 = State('e1')
b1 = State('b1')
c3 = State('c3')
c2 = State('c2')
c1 = State('c1')
d1 = State('d1')
a1 = State('a1')
a0 = State('a0')
a0.add_transition(32, a1)
a0.add_transition(9, a1)
a0.add_transition(10, a1)
a0.add_transition(48, d1)
a0.add_transition(48, c1)
a0.add_transition(48, b1)
a0.add_transition(49, d1)
a0.add_transition(49, c1)
a0.add_transition(49, b1)
a0.add_transition(50, d1)
a0.add_transition(50, c1)
a0.add_transition(50, b1)
a0.add_transition(51, d1)
a0.add_transition(51, c1)
a0.add_transition(51, b1)
a0.add_transition(52, d1)
a0.add_transition(52, c1)
a0.add_transition(52, b1)
a0.add_transition(53, d1)
a0.add_transition(53, c1)
a0.add_transition(53, b1)
a0.add_transition(54, d1)
a0.add_transition(54, c1)
a0.add_transition(54, b1)
a0.add_transition(55, d1)
a0.add_transition(55, c1)
a0.add_transition(55, b1)
a0.add_transition(56, d1)
a0.add_transition(56, c1)
a0.add_transition(56, b1)
a0.add_transition(57, d1)
a0.add_transition(57, c1)
a0.add_transition(57, b1)
a0.add_transition(65, d1)
a0.add_transition(66, d1)
a0.add_transition(67, d1)
a0.add_transition(68, d1)
a0.add_transition(69, d1)
a0.add_transition(70, d1)
a0.add_transition(73, e1)
a0.add_transition(84, f1)

a1.isFinalState = True
a1.addToken('ws')

d1.isFinalState = True
d1.addToken('HEXADECIMAL')
d1.add_transition(65, d1)
d1.add_transition(66, d1)
d1.add_transition(67, d1)
d1.add_transition(68, d1)
d1.add_transition(69, d1)
d1.add_transition(70, d1)
d1.add_transition(48, d1)
d1.add_transition(49, d1)
d1.add_transition(50, d1)
d1.add_transition(51, d1)
d1.add_transition(52, d1)
d1.add_transition(53, d1)
d1.add_transition(54, d1)
d1.add_transition(55, d1)
d1.add_transition(56, d1)
d1.add_transition(57, d1)

c1.add_transition(46, c2)
c1.add_transition(48, c1)
c1.add_transition(49, c1)
c1.add_transition(50, c1)
c1.add_transition(51, c1)
c1.add_transition(52, c1)
c1.add_transition(53, c1)
c1.add_transition(54, c1)
c1.add_transition(55, c1)
c1.add_transition(56, c1)
c1.add_transition(57, c1)

c2.add_transition(48, c3)
c2.add_transition(49, c3)
c2.add_transition(50, c3)
c2.add_transition(51, c3)
c2.add_transition(52, c3)
c2.add_transition(53, c3)
c2.add_transition(54, c3)
c2.add_transition(55, c3)
c2.add_transition(56, c3)
c2.add_transition(57, c3)

c3.isFinalState = True
c3.addToken('FLOAT')
c3.add_transition(48, c3)
c3.add_transition(49, c3)
c3.add_transition(50, c3)
c3.add_transition(51, c3)
c3.add_transition(52, c3)
c3.add_transition(53, c3)
c3.add_transition(54, c3)
c3.add_transition(55, c3)
c3.add_transition(56, c3)
c3.add_transition(57, c3)

b1.isFinalState = True
b1.addToken('INT')
b1.add_transition(48, b1)
b1.add_transition(49, b1)
b1.add_transition(50, b1)
b1.add_transition(51, b1)
b1.add_transition(52, b1)
b1.add_transition(53, b1)
b1.add_transition(54, b1)
b1.add_transition(55, b1)
b1.add_transition(56, b1)
b1.add_transition(57, b1)

e1.add_transition(70, e2)

e2.isFinalState = True
e2.addToken('IF')

f1.add_transition(72, f2)

f2.add_transition(69, f3)

f3.add_transition(78, f4)

f4.isFinalState = True
f4.addToken('THEN')


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
            listTextTuple.append((textToAccept, lastStateAccepted[-1].getToken()))
            lasChIndex = lastChar + 1
            chIndex = lastChar + 1
            paths = [[initState]]
            lastPathAccepted = []
            continue

        newLastPathAccepted = []

        for path in newPaths:
            if path[-1].isFinalState:
                newLastPathAccepted.append(
                    (chIndex, path, sum([path[i].numberTransitions() for i in range(len(path))])))

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
    print(CYAN, 'Cual es el mensaje a evaluar?', RESET)

    fileToRead = input()

    with open(fileToRead, 'r') as file:
        contents = file.read()

    print(YELLOW, 'Resultado:', RESET)
    tokens = exclusiveSim(a0, contents)
    for message, token in tokens:
        if token != 1 and token != 0:
            print(CYAN, 'TEXT:', WHITE, message, CYAN, ' -> ', RESET, GREEN, token, RESET)
        elif token == 1:
            print(RED, 'ERROR IN LINE:', message, RESET)
        