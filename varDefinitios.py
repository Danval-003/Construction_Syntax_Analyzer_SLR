from typing import *
from prepareAFD import import_module
from Simulator import exclusiveSim
from prepareAFD import prepareAFN


def defVariables(listVar: List[Tuple[str, str]]):
    regex = {
        'IN_SET': ["\[([^a]|a|' ')*\]"],
        'IN_GROUP': ["\( *(\(([^a()]|a|\?|\+|\*|\+|.|\|)\))*\)"],
        'OPERATOR': ['\|', '\?', '\*', '^', '\+'],
        'SYMBOL': ["'[a-zA-Z0-9]'|[^+*?()|]|."],
    }

    regexInSet = {
        'IND': ["'[^']'|' '"],
        'OPER': ["-"],
        'GROUP': ['"[^a]+"']
    }

    machine = import_module("varDefMachine.py", regex)
    machineSet = import_module("varDefMachineSET.py", regexInSet)
    dictVar = {}

    def inOperator(regexComponent):
        operation = ''
        for comp, type in regexComponent:
            if type == 'OPERATOR':
                operation += comp.replace("'", '')
                continue
            if type == 'IN_SET':
                notInSet = comp[1:-1]
                regexCo = exclusiveSim(machineSet, notInSet)
                operation += '['
                for compCo, typeCo in regexCo:
                    if typeCo == 'IND':
                        operation += compCo.replace("'", '')
                    if typeCo == 'OPER':
                        operation += compCo
                    if typeCo == 'GROUP':
                        operation += compCo.replace('"', '')
                operation += ']'
                continue
            if type == 'IN_GROUP':
                notInGroup = comp[1:-1]
                regexCo = exclusiveSim(machine, notInGroup)
                operation += '('
                operation += inOperator(regexCo)
                operation += ')'
            if type == 'SYMBOL':
                operation += comp.replace("'", '')
            if type not in regex and type != 0:
                operation += dictVar[comp]

        return operation

    for var in listVar:
        regexNew = {var[0]: [var[0]]}
        newMachine = prepareAFN(regexNew)

        rC = exclusiveSim(machine, var[1])
        op = inOperator(rC)
        dictVar[var[0]] = op

        machine.combine_States(newMachine)

    return dictVar


def defTokens(dictVar: Dict[str, str], tokens: List[str]):
    regex = {
        'RETURN': ['\{ *return *[A-Z][A-Z]* *\}'],
        'TOKEN': ["[a-z][a-z]*"],
        'SYMBOL': ["'([^a]|a)'", '"([^a]|a)+"'],
    }

    machine = import_module("tokenMachine.py", regex)
    #draw_AF(machine, legend=f'AFD minimized direct', expression='default', direct=True, name='AFD_min_direct')
    tk = {}
    for token in tokens:
        rC = exclusiveSim(machine, token)
        tokenName = ''
        regexDescription = ''
        for comp, type in rC:
            if type == 'TOKEN':
                if tokenName == '':
                    tokenName = comp
                regexDescription += dictVar[comp]
            if type == 'RETURN':
                tokenName = comp[comp.find('return')+6:comp.find('}')]
            if type == 'SYMBOL':
                rD = comp[1:-1]
                if rD in '{[(+*?|)}]':
                    regexDescription += '\\'
                regexDescription += rD
        tk[tokenName.strip()] = [regexDescription]

    print(tk)

    maxMachine = prepareAFN(tk)

    return maxMachine

