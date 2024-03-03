from Colors import *
from typing import *
from Classes_ import State
import time
import ErroManagerReaders as err


def Simulator(states: Dict[str, State], string: str, expression=""):
    print(f"{BOLD}{YELLOW}Simulating the string [{string}] in the automaton{RESET}")
    print(f"{BOLD}{YELLOW}Automaton: {expression}{RESET}")

    pathDict: Dict[str, List[State]] = dict()

    def simulation(initState: State):
        paths: List[List[State]] = [[initState]]

        for ch in string:
            char = ord(ch)
            newPaths: List[List[State]] = []

            for path in paths:
                evalState: State = path[-1]

                for st in evalState.getStates(char):
                    newPath = path.copy()
                    newPath.append(st)
                    newPaths.append(newPath)

                for st_e in evalState.getEpsilonClean() - {evalState}:
                    for st in st_e.getStates(char):
                        newPath = path.copy()
                        newPath.append(st)
                        newPaths.append(newPath)

            paths = newPaths

        for path in paths:
            evalState: State = path[-1]

            if evalState.isFinalState:
                return True, path

            for st_e in evalState.getEpsilonClean():
                if st_e.isFinalState:
                    finalPath = path.copy()
                    finalPath.append(st_e)
                    return True, finalPath

        return False, []

    simulationResult = True

    start = time.perf_counter()
    for key in states:
        result, simulationPaths = simulation(states[key])
        simulationResult = simulationResult and result
        pathDict[key] = simulationPaths
        print(f"{BOLD}Simulation for {key}: {GREEN + 'Excellent!' if result else RED + 'Bad result'}{RESET}")
        if not result:
            break
    end = time.perf_counter()

    if simulationResult:
        print(f"{BOLD}{GREEN}The string was accepted{RESET}")
    else:
        print(f"{BOLD}{RED}The string was not accepted{RESET}")

    print(f"{BOLD}{YELLOW}Time elapsed: {end - start} seconds{RESET}")

    return simulationResult, pathDict


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

            for st_e in evalState.getEpsilonClean() - {evalState}:
                for st in st_e.getStates(char):
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

    for line, token in listTextTuple:
        if token == 1:
            err.generalError(line, 'Token no reconocido')

    return listTextTuple
