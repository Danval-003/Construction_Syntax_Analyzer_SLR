from Reader import *
from infix_converter import *
from Tree_ import *
from AFD_direct import *
import string
import os
import importlib.util
from Draw_diagrams import draw_AF


def prepareAFN(expressions: Dict[str, List[str]]) -> State:
    initState: State or None = None
    cont = 0
    for token, regex in expressions.items():
        parsed: List[List[str or int]] = transformsChar(regex)
        accepted: List[List[str or int]] = validate(parsed)
        alphabets: List[Set[int]] = extract_alphabet(accepted)
        formatted: List[List[str or int]] = format_regex(accepted)
        postfix: List[str or int] = translate_to_postfix(formatted)
        for i in range(len(postfix)):
            tree = make_direct_tree(postfix[i])
            direct = make_direct_AFD(tree[0], tree[1], alphabets[i], token)
            minimize = minimizeAFD(direct[2], alphabets[i], id_=string.ascii_lowercase[cont])
            if initState is None:
                initState = minimize[1]
            else:
                initState.combine_States(minimize[1])

            cont += 1

    return initState


def translateToCode(initState: State) -> str:
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
        if len(state.token)>0:
            code += f"{i}.addToken( '{state.getToken()}')\n"
        for tran, states in state.transitions.items():
            for st in states:
                code += f"{i}.add_transition({tran}, {st.value})\n"
        code += '\n'

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
        if len(state.token)>0:
            code += f"{i}.addToken( '{state.getToken()}')\n"
        for tran, states in state.transitions.items():
            for st in states:
                code += f"{i}.add_transition({tran}, {st.value})\n"
        code += '\n'

    code = f"from Classes_ import State\n\n" + code

    return code


def import_module(file,regex):
    if os.path.isfile(file):
        import_module = file.split('.')[0]
        spec = importlib.util.spec_from_file_location(import_module, file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        a0 = getattr(module, 'a0', None)
    else:
        a0 = prepareAFN(regex)
        code = translateToCode(a0)
        with open(file, 'w') as fileW:
            fileW.write(code)

    return a0

