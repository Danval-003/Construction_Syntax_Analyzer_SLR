from typing import *


class Node:
    def __init__(self, value: str or int, left: 'Node' or None = None, right: 'Node' or None = None,
                 id_: int or None = None) \
            -> None:
        self.value: str or int = value
        self.left: 'Node' or None = left
        self.right: 'Node' or None = right
        self.id_: int or None = id_
        self.is_nullable: bool = False
        self.first_pos: Set[int] = set()
        self.last_pos: Set[int] = set()
        self.isLeft: bool = False
        self.follow_pos: Set[str] = set()

    def getId(self) -> str:
        return str(id(self))


class FormatPointer:

    def __init__(self):
        self.stack: List[str or 'FormatPointer'] = []
        self.father: 'FormatPointer' or None = None
        self.actual: 'FormatPointer' = self

    def push(self, value):
        self.actual.stack.append(value)

    def inGroup(self) -> 'FormatPointer' or None:
        if id(self.actual) == id(self):
            new = FormatPointer()
            new.father = self
            self.actual.stack.append(new)
            self.actual = new
            return new
        else:
            self.actual = self.actual.inGroup()

    def __str__(self):
        result = "("
        for i in self.stack:
            if i is FormatPointer:
                result += i.__str__()
            else:
                result += str(i)
        return result + ")"

    def outGroup(self):
        result = self.actual.__str__()
        self.actual = self.actual.father
        self.actual.actual = self.actual
        self.actual.stack.pop()
        self.actual.stack.append(result)

    def plus(self):
        last = self.actual.stack.pop()
        self.actual.stack.append('(' + last + '.' + last + '*)')

    def interrogation(self):
        last = self.actual.stack.pop()
        self.actual.stack.append("(" + last + "|ε)")


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

    def combine_States(self, state: 'State') -> None:
        for transition in state.transitions:
            if transition in self.transitions:
                self.transitions[transition] = self.transitions[transition].union(state.transitions[transition])
            else:
                self.transitions[transition] = state.transitions[transition]

        if state.isFinalState:
            self.isFinalState = True

        self.token = self.token.union(state.token)

    def getId(self) -> str:
        return str(id(self))

    def getStates(self, transition_value) -> Set['State']:
        return self.transitions[transition_value] if transition_value in self.transitions else set()

    def __eq__(self, other):
        """Define la igualdad entre dos instancias de la clase."""
        if isinstance(other, State):
            return (self.value, id(self)) == (other.value, id(self))
        return False

    def __hash__(self):
        """Define el valor de hash de la instancia."""
        return hash((self.value, id(self)))

    def getEpsilonClean(self):
        states: Set['State'] = self.getStates(ord('ε'))
        not_explorer: Set['State'] = set()

        for state in states:
            not_explorer = not_explorer.union(state.getStates(ord('ε')))

        not_explorer = not_explorer - states

        while len(not_explorer) > 0:
            states = states.union(not_explorer)
            copy = not_explorer.copy()
            not_explorer = set()
            for state in copy:
                not_explorer = not_explorer.union(state.getStates(ord('ε')))
            not_explorer = not_explorer - states

        return states.union({self})

    def delState(self, state: 'State'):
        for transition in self.transitions:
            if state in self.transitions[transition]:
                self.transitions[transition].remove(state)

    def addToken(self, token: str):
        self.token.add(token)

    def getToken(self) -> str or None:
        return str(list(self.token)[0]) if len(self.token) > 0 else None

    def numberTransitions(self) -> int:
        return self.numTrans

