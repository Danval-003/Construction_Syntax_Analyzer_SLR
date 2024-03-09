from Reader import *
from infix_converter import *
from Tree_ import *
from AFD_direct import *
import string
import os
import importlib.util
from Draw_diagrams import draw_AF, draw_tree
import threading
from queue import Queue


def create_mach(token, regex, count, resultQueue: Queue, TreeQueue: Queue):
    print(f'Creating machine for {token}')
    parsed: List[List[str or int]] = transformsChar(regex)
    accepted: List[List[str or int]] = validate(parsed)
    alphabets: List[Set[int]] = extract_alphabet(accepted)
    formatted: List[List[str or int]] = format_regex(accepted)
    postfix: List[str or int] = translate_to_postfix(formatted)
    tree = make_direct_tree(postfix[0], token=token)
    TreeQueue.put(tree)
    direct = make_direct_AFD(tree[0], tree[1], alphabets[0], token)
    minimize = minimizeAFD(direct[2], alphabets[0], id_=string.ascii_lowercase[count])
    resultQueue.put(minimize[1])


def prepareAFN(expressions: Dict[str, List[str]], showTree = False) -> State:
    initState: State or None = None
    cont = 0
    threads: List[threading.Thread] = []
    resultQueue = Queue()
    TreeQueue = Queue()
    for token, regex in expressions.items():
        for i in range(len(regex)):
            t = threading.Thread(target=create_mach, args=(token, [regex[i]], cont, resultQueue, TreeQueue))
            threads.append(t)
            t.start()
            cont += 1

    for t in threads:
        t.join()

    while not resultQueue.empty():
        mach = resultQueue.get()
        if initState is None:
            initState = mach
        else:
            initState.combine_States(mach)

    iniTreeNode:Node = Node('Root')
    while not TreeQueue.empty():
        leftTree = TreeQueue.get()
        if iniTreeNode.left is None:
            iniTreeNode.left = leftTree[2]
            if iniTreeNode.right is None and not TreeQueue.empty():
                iniTreeNode.right = TreeQueue.get()[2]
                if TreeQueue.empty():
                    break
                newInitNode = Node('Root')
                newInitNode.left = iniTreeNode
                iniTreeNode = newInitNode
            continue
        else:
            iniTreeNode.right = leftTree[2]
            if TreeQueue.empty():
                break
            newInitNode = Node('Root')
            newInitNode.left = iniTreeNode
            iniTreeNode = newInitNode

    if showTree:
        draw_tree(iniTreeNode, 'default', useNum=True)
    initState.value = 'a0'
    return initState


def translateToCode(initState: State, isOut: bool = False) -> str:
    code = ''
    setStates: Dict[str, State] = {initState.value: initState}

    def addState(state: State):
        for tran, states in state.transitions.items():
            for st in states:
                if st.value not in setStates:
                    setStates[st.value] = st
                    addState(st)

    addState(initState)

    for i, state in setStates.items():
        code = f"{i} = State('{i}')\n" + code
        if state.isFinalState:
            code += f"{i}.isFinalState = True\n"
        if len(state.token) > 0:
            code += f"""\n\ndef tk_{i}(): \n"""
            for j in state.token:
                code += f"\t{j}\n"

            code += f"\n\n{i}.token = tk_{i}\n"
        for tran, states in state.transitions.items():
            for st in states:
                code += f"{i}.add_transition({tran}, {st.value})\n"
        code += '\n'



    if isOut:
        code = """
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
        
        
\n\n""" + code

        code = f"from typing import *\n\n" + code


        code += r"""
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
    print(CYAN, 'Cual es el mensaje a evaluar?', RESET)

    fileToRead = input()

    with open(fileToRead, 'r') as file:
        contents = file.read()

    print(YELLOW, 'Resultado:', RESET)
    tokens = exclusiveSim(a0, contents)
    for message, token in tokens:
        if token != 1 and token != 0:
            token()
        elif token == 1:
            print(RED, 'ERROR IN LINE:', message, RESET)
        """
    else:
        code = f"from Classes_ import State\n\n" + code
    return code


def statesTotla(initState: State) -> str:
    code = ''
    setStates: Dict[str, State] = {initState.value: initState}

    def addState(state: State):
        for tran, states in state.transitions.items():
            for st in states:
                if st.value not in setStates:
                    setStates[st.value] = st
                    addState(st)

    addState(initState)

    for i, state in setStates.items():
        code = f"{i} = State('{i}')\n" + code
        if state.isFinalState:
            code += f"{i}.isFinalState = True\n"
        if len(state.token) > 0:
            code += f"{i}.addToken( '{state.getToken()}')\n"
        for tran, states in state.transitions.items():
            for st in states:
                code += f"{i}.add_transition({tran}, {st.value})\n"
        code += '\n'
    else:

        code = f"from typing import *\nfrom Classes_ import State\n\n" + code

    return code


def import_module(file, regex, showTree=False):
    if os.path.isfile(file):
        import_module = file.split('.')[0]
        spec = importlib.util.spec_from_file_location(import_module, file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        a0 = getattr(module, 'a0', None)
    else:
        a0 = prepareAFN(regex, showTree=showTree)
        code = translateToCode(a0)
        with open(file, 'w') as fileW:
            fileW.write(code)

    return a0
