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


m1 = State('m1')
l1 = State('l1')
k1 = State('k1')
j1 = State('j1')
i1 = State('i1')
h1 = State('h1')
g1 = State('g1')
f1 = State('f1')
e2 = State('e2')
e1 = State('e1')
d1 = State('d1')
c6 = State('c6')
c1 = State('c1')
c5 = State('c5')
c2 = State('c2')
c3 = State('c3')
c4 = State('c4')
b1 = State('b1')
a1 = State('a1')
a0 = State('a0')
a0.add_transition(32, a1)
a0.add_transition(9, a1)
a0.add_transition(10, a1)
a0.add_transition(65, b1)
a0.add_transition(66, b1)
a0.add_transition(67, b1)
a0.add_transition(68, b1)
a0.add_transition(69, b1)
a0.add_transition(70, b1)
a0.add_transition(71, b1)
a0.add_transition(72, b1)
a0.add_transition(73, b1)
a0.add_transition(74, b1)
a0.add_transition(75, b1)
a0.add_transition(76, b1)
a0.add_transition(77, b1)
a0.add_transition(78, b1)
a0.add_transition(79, b1)
a0.add_transition(80, b1)
a0.add_transition(81, b1)
a0.add_transition(82, b1)
a0.add_transition(83, b1)
a0.add_transition(84, b1)
a0.add_transition(85, b1)
a0.add_transition(86, b1)
a0.add_transition(87, b1)
a0.add_transition(88, b1)
a0.add_transition(89, b1)
a0.add_transition(90, b1)
a0.add_transition(97, b1)
a0.add_transition(98, b1)
a0.add_transition(99, b1)
a0.add_transition(100, b1)
a0.add_transition(101, b1)
a0.add_transition(102, b1)
a0.add_transition(103, b1)
a0.add_transition(104, b1)
a0.add_transition(105, b1)
a0.add_transition(106, b1)
a0.add_transition(107, b1)
a0.add_transition(108, b1)
a0.add_transition(109, b1)
a0.add_transition(110, b1)
a0.add_transition(111, b1)
a0.add_transition(112, b1)
a0.add_transition(113, b1)
a0.add_transition(114, b1)
a0.add_transition(115, b1)
a0.add_transition(116, b1)
a0.add_transition(117, b1)
a0.add_transition(118, b1)
a0.add_transition(119, b1)
a0.add_transition(120, b1)
a0.add_transition(121, b1)
a0.add_transition(122, b1)
a0.add_transition(48, c4)
a0.add_transition(49, c4)
a0.add_transition(50, c4)
a0.add_transition(51, c4)
a0.add_transition(52, c4)
a0.add_transition(53, c4)
a0.add_transition(54, c4)
a0.add_transition(55, c4)
a0.add_transition(56, c4)
a0.add_transition(57, c4)
a0.add_transition(59, d1)
a0.add_transition(58, e1)
a0.add_transition(60, f1)
a0.add_transition(61, g1)
a0.add_transition(43, h1)
a0.add_transition(45, i1)
a0.add_transition(42, j1)
a0.add_transition(47, k1)
a0.add_transition(40, l1)
a0.add_transition(41, m1)

a1.isFinalState = True
a1.addToken('ws')
a1.add_transition(32, a1)
a1.add_transition(9, a1)
a1.add_transition(10, a1)

b1.isFinalState = True
b1.addToken('ID')
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
b1.add_transition(65, b1)
b1.add_transition(66, b1)
b1.add_transition(67, b1)
b1.add_transition(68, b1)
b1.add_transition(69, b1)
b1.add_transition(70, b1)
b1.add_transition(71, b1)
b1.add_transition(72, b1)
b1.add_transition(73, b1)
b1.add_transition(74, b1)
b1.add_transition(75, b1)
b1.add_transition(76, b1)
b1.add_transition(77, b1)
b1.add_transition(78, b1)
b1.add_transition(79, b1)
b1.add_transition(80, b1)
b1.add_transition(81, b1)
b1.add_transition(82, b1)
b1.add_transition(83, b1)
b1.add_transition(84, b1)
b1.add_transition(85, b1)
b1.add_transition(86, b1)
b1.add_transition(87, b1)
b1.add_transition(88, b1)
b1.add_transition(89, b1)
b1.add_transition(90, b1)
b1.add_transition(95, b1)
b1.add_transition(97, b1)
b1.add_transition(98, b1)
b1.add_transition(99, b1)
b1.add_transition(100, b1)
b1.add_transition(101, b1)
b1.add_transition(102, b1)
b1.add_transition(103, b1)
b1.add_transition(104, b1)
b1.add_transition(105, b1)
b1.add_transition(106, b1)
b1.add_transition(107, b1)
b1.add_transition(108, b1)
b1.add_transition(109, b1)
b1.add_transition(110, b1)
b1.add_transition(111, b1)
b1.add_transition(112, b1)
b1.add_transition(113, b1)
b1.add_transition(114, b1)
b1.add_transition(115, b1)
b1.add_transition(116, b1)
b1.add_transition(117, b1)
b1.add_transition(118, b1)
b1.add_transition(119, b1)
b1.add_transition(120, b1)
b1.add_transition(121, b1)
b1.add_transition(122, b1)

c4.isFinalState = True
c4.addToken('NUMBER')
c4.add_transition(69, c3)
c4.add_transition(46, c1)
c4.add_transition(48, c4)
c4.add_transition(49, c4)
c4.add_transition(50, c4)
c4.add_transition(51, c4)
c4.add_transition(52, c4)
c4.add_transition(53, c4)
c4.add_transition(54, c4)
c4.add_transition(55, c4)
c4.add_transition(56, c4)
c4.add_transition(57, c4)

c3.add_transition(43, c2)
c3.add_transition(45, c2)
c3.add_transition(48, c5)
c3.add_transition(49, c5)
c3.add_transition(50, c5)
c3.add_transition(51, c5)
c3.add_transition(52, c5)
c3.add_transition(53, c5)
c3.add_transition(54, c5)
c3.add_transition(55, c5)
c3.add_transition(56, c5)
c3.add_transition(57, c5)

c2.add_transition(48, c5)
c2.add_transition(49, c5)
c2.add_transition(50, c5)
c2.add_transition(51, c5)
c2.add_transition(52, c5)
c2.add_transition(53, c5)
c2.add_transition(54, c5)
c2.add_transition(55, c5)
c2.add_transition(56, c5)
c2.add_transition(57, c5)

c5.isFinalState = True
c5.addToken('NUMBER')
c5.add_transition(48, c5)
c5.add_transition(49, c5)
c5.add_transition(50, c5)
c5.add_transition(51, c5)
c5.add_transition(52, c5)
c5.add_transition(53, c5)
c5.add_transition(54, c5)
c5.add_transition(55, c5)
c5.add_transition(56, c5)
c5.add_transition(57, c5)

c1.add_transition(48, c6)
c1.add_transition(49, c6)
c1.add_transition(50, c6)
c1.add_transition(51, c6)
c1.add_transition(52, c6)
c1.add_transition(53, c6)
c1.add_transition(54, c6)
c1.add_transition(55, c6)
c1.add_transition(56, c6)
c1.add_transition(57, c6)

c6.isFinalState = True
c6.addToken('NUMBER')
c6.add_transition(69, c3)
c6.add_transition(48, c6)
c6.add_transition(49, c6)
c6.add_transition(50, c6)
c6.add_transition(51, c6)
c6.add_transition(52, c6)
c6.add_transition(53, c6)
c6.add_transition(54, c6)
c6.add_transition(55, c6)
c6.add_transition(56, c6)
c6.add_transition(57, c6)

d1.isFinalState = True
d1.addToken('SEMICOLON')

e1.add_transition(61, e2)

e2.isFinalState = True
e2.addToken('ASSIGNOP')

f1.isFinalState = True
f1.addToken('LT')

g1.isFinalState = True
g1.addToken('EQ')

h1.isFinalState = True
h1.addToken('PLUS')

i1.isFinalState = True
i1.addToken('MINUS')

j1.isFinalState = True
j1.addToken('TIMES')

k1.isFinalState = True
k1.addToken('DIV')

l1.isFinalState = True
l1.addToken('LPAREN')

m1.isFinalState = True
m1.addToken('RPAREN')


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
        