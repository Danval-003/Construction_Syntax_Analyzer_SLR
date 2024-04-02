from typing import Dict, List, Set, Tuple
from Machines_gen_usage.Classes_ import Node, State


def make_direct_AFD(tree: Node, nodes: Dict[str or int, Node], alphaSet: Set[int], token: str = ''):
    alpha = list(alphaSet)

    states: Dict[Tuple[int or str, ...], State] = {tuple(tree.first_pos): State('q0')}
    toEvaluate: List[Tuple[int, ...]] = [tuple(tree.first_pos)]
    total_states: Dict[str, State] = dict()
    initSta: Tuple[int, ...] = tuple(tree.first_pos)
    total_states['q0'] = states[initSta]
    finalState: str = ''
    for state in nodes:
        if nodes[state].value == '#':
            finalState = state
            break
    gen = 1

    while len(toEvaluate) > 0:
        actualState: Tuple[int, ...] = toEvaluate.pop(0)

        for letter in alpha:
            nextState_st: Set[int] = set()
            for state in actualState:
                if nodes[state].value == letter:
                    nextState_st = nextState_st.union(nodes[state].follow_pos)

            if len(nextState_st) <= 0:
                continue
            nextState: Tuple[int, ...] = tuple(nextState_st)
            if nextState not in states:
                states[nextState] = State('q' + str(gen))
                total_states['q' + str(gen)] = states[nextState]
                if finalState in nextState_st:
                    states[nextState].isFinalState = True
                toEvaluate.append(nextState)
                gen += 1
            states[actualState].add_transition(letter, states[nextState])

    for state in states:
        if finalState in state:
            states[state].isFinalState = True
            states[state].token.add(token)

    return states, states[initSta], total_states


def minimizeAFD(states2: Dict[str or int, State], alpha: Set[int or str], id_:str = 'Q'):
    initSt = states2['q0']
    initState = tuple([states2[x] for x in states2 if not states2[x].isFinalState])
    finalState = tuple([states2[x] for x in states2 if states2[x].isFinalState])
    minimized_states: Dict[str, Tuple[State, ...]] = {id_+'0': initState, id_+'1': finalState}

    not_toDo = True
    while not_toDo:
        evaluated = 1
        new_minimized_states: Dict[str, Tuple[State, ...]] = dict()
        for subStates in minimized_states:
            transitionsDict: Dict[str, Set[State]] = dict()
            for minState in minimized_states[subStates]:
                transitions: List[Tuple[str, str]] = []
                for letter in alpha:
                    if len(minState.getStates(letter)) <= 0:
                        pass
                    else:
                        newState = minState.getStates(letter).copy().pop()
                        for subStates2 in minimized_states:
                            if newState in minimized_states[subStates2]:
                                transition: Tuple[str, str] = (subStates2, letter)
                                transitions.append(transition)

                tupleTransitions: str = str(transitions)
                if tupleTransitions in transitionsDict:
                    transitionsDict[tupleTransitions].add(minState)
                else:
                    transitionsDict[tupleTransitions] = {minState}

            for transition_ in transitionsDict:
                if initSt in transitionsDict[transition_]:
                    new_minimized_states[id_ + str(0)] = tuple(transitionsDict[transition_])
                    continue
                new_minimized_states[id_ + str(evaluated)] = tuple(transitionsDict[transition_])
                evaluated += 1

        if len(new_minimized_states) == len(minimized_states):
            not_toDo = False
        else:
            minimized_states = new_minimized_states


    newMin_States: Dict[str, State] = dict()
    initial = ''
    for subStates in minimized_states:
        index = subStates

        if states2['q0'] in minimized_states[subStates]:
            initial = index
        newMin_States[index] = State(index)

        for minState in minimized_states[subStates]:
            if minState.isFinalState:
                newMin_States[index].isFinalState = True
                newMin_States[index].token = minState.token
                break

    for subStates in minimized_states:
        index = subStates
        tryState: State = tuple(minimized_states[subStates])[0]
        newMinState: State = newMin_States[index]

        for letter in alpha:
            if len(tryState.getStates(letter)) <= 0:
                continue

            tranState = tryState.getStates(letter).copy().pop()
            for subStates2 in minimized_states:
                if tranState in minimized_states[subStates2]:
                    newMinState.add_transition(letter, newMin_States[subStates2])
                    break

    newMin_States[initial].value = id_+'0'

    return newMin_States, newMin_States[initial]