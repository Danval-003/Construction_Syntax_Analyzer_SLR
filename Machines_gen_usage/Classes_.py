from typing import *
from typing import Tuple, List, Any


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


class Grammar_Element:
    def __init__(self, value: str, terminal: bool = False, epsilon: bool = False) -> None:
        self.value: str = value
        self.terminal: bool = terminal
        self.epsilon: bool = epsilon
        self.firstCalculated: List['Production_Item'] = []
        self.followCalculated: List['Production_Item'] = []

        if self.terminal:
            self.first: Set['Grammar_Element'] = {self}
        else:
            self.first: Set['Grammar_Element'] = set()

        self.follow: Set['Grammar_Element'] = set()
        self.transition: Set['Production_Item'] = set()
        self.ignore = False

    def __str__(self):
        return str(self.value)

    def transition_to(self, production: List['Grammar_Element']) -> 'Production_Item':
        if not self.epsilon:
            for elem in production:
                if elem.epsilon:
                    self.epsilon = self.epsilon and True
                    break
        product = Production_Item(self, production)
        self.transition.add(product)
        self.firstCalculated.append(product)
        self.followCalculated.append(product)
        return product

    def getResults(self) -> List[Tuple['Grammar_Element', ...]]:
        return [i.getResults() for i in self.transition]

    def calculateFirst(self):
        while len(self.firstCalculated) != 0:
            production = self.firstCalculated.pop()
            result, epsilon = production.getFirst()
            self.epsilon = self.epsilon or epsilon
            for elem in result:
                if elem.terminal:
                    self.first.add(elem)
                else:
                    elem.calculateFirst()
                    self.first = self.first.union(elem.first)

        return self.first

    def calculateFollow(self):
        while len(self.followCalculated) != 0:
            production = self.followCalculated.pop()
            pairs = production.getFollowPairs()
            for pair in pairs:
                elem, next_elem = pair
                if next_elem is None:
                    elem.follow = elem.follow.union(self.follow)
                else:
                    elem.follow = elem.follow.union(next_elem.first)
                    if next_elem.epsilon:
                        elem.follow = elem.follow.union(next_elem.follow)

                if not elem.terminal:
                    elem.calculateFollow()

        return self.follow

    def __eq__(self, other):
        """Define la igualdad entre dos instancias de la clase."""
        if isinstance(other, State):
            return (self.value, id(self)) == (other.value, id(self))
        return False

    def __hash__(self):
        """Define el valor de hash de la instancia."""
        return hash((self.value, id(self)))


class Production_Item:
    def __init__(self, NonTerminal: 'Grammar_Element',
                 Result: List['Grammar_Element'] or Tuple['Grammar_Element', ...], point: int = 0) -> None:
        self.NonTerminal: 'Grammar_Element' = NonTerminal
        self.Result: Tuple['Grammar_Element', ...] = tuple(Result)
        self.point: int = point
        self.final = False
        self.hasFinal = False
        self.firstBeta:Set[Grammar_Element] = set()
        self.followA = NonTerminal.follow

        for elem in Result:
            if elem.value == '$':
                self.hasFinal = True
                break

        beta = list(Result[point:])
        for elem in beta:
            if elem.terminal:
                self.firstBeta.add(elem)
                break
            else:
                self.firstBeta = self.firstBeta.union(elem.first)
            if elem.epsilon:
                self.final = True
            else:
                self.final = False
                break

    def getResults(self) -> Tuple['Grammar_Element', ...]:
        return self.Result

    def getFirst(self) -> tuple[list[Grammar_Element], bool]:
        first = []
        epsilon = False
        for elem in self.Result:
            first.append(elem)
            if elem.epsilon:
                epsilon = True
            else:
                epsilon = False
                break

        return first, epsilon

    def getFollowPairs(self) -> List[Tuple['Grammar_Element', 'Grammar_Element' or None]]:
        pairs = []
        for i in range(len(self.Result)):
            if i == len(self.Result) - 1:
                pairs.append((self.Result[i], None))
            else:
                pairs.append((self.Result[i], self.Result[i + 1]))
        return pairs

    def __eq__(self, other: 'Production_Item'):
        """Define la igualdad entre dos instancias de la clase."""
        if isinstance(other, Production_Item):
            return (self.NonTerminal, self.Result, self.point) == (other.NonTerminal, other.Result, other.point)
        return False

    def __hash__(self):
        """Define el valor de hash de la instancia."""
        return hash((self.NonTerminal, self.Result, self.point))

    def __str__(self):
        result = [i.value for i in self.Result]
        result.insert(self.point, '.')

        return f"{self.NonTerminal.value} -> {' '.join(result)}"

    def __lt__(self, other):
        if self.NonTerminal.value == other.NonTerminal.value:
            return len(self.Result) < len(other.Result)
        return self.NonTerminal.value < other.NonTerminal.value

    def passPoint(self, Element: 'Grammar_Element') -> Tuple[bool, 'Production_Item']:
        newProduction = Production_Item(self.NonTerminal, self.Result, self.point)
        if newProduction.point < len(newProduction.Result):
            if newProduction.Result[newProduction.point].value == Element.value:
                newProduction.point += 1
                if newProduction.point == len(newProduction.Result) - 1 and newProduction.hasFinal:
                    newProduction.final = True

                return True, newProduction
        return False, self

    def poitElement(self) -> Grammar_Element | None:
        if self.point < len(self.Result):
            return self.Result[self.point]
        return None

    def closureCalc(self) -> Set['Production_Item']:
        result = {self}

        while True:
            newResult = set()
            for production in result:
                elem = production.poitElement()
                if elem is not None and not elem.terminal:
                    for transition in elem.transition:
                        newProduction = Production_Item(transition.NonTerminal, transition.Result)
                        if newProduction not in result:
                            newResult.add(newProduction)
            if len(newResult) == 0:
                break
            result = result.union(newResult)

        return result


class LRO_S:
    def __init__(self, state: Set[Production_Item], numState: int = 0) -> None:
        self.state: Tuple[Production_Item, ...] = tuple(sorted(state))
        self.transitions: Dict[Grammar_Element, 'LRO_S'] = {}
        self.numState: int = numState
        self.isFinalState: bool = False

        for production in state:
            if production.final:
                self.isFinalState = True
                break

    def add_transition(self, value: Grammar_Element, state: 'LRO_S') -> None:
        if value in self.transitions:
            raise Exception('Transition already exists')
        else:
            self.transitions[value] = state

    def __eq__(self, other):
        """Define la igualdad entre dos instancias de la clase."""
        if isinstance(other, LRO_S):
            return self.state == other.state
        return False

    def __hash__(self):
        """Define el valor de hash de la instancia."""
        return hash(self.state)

    def __str__(self):
        return f"{self.numState}: " + ' '.join([i.__str__() for i in self.state])

