from Machines_gen_usage.prepareAFD import *
from Machines_gen_usage.Draw_diagrams import *
from Machines_gen_usage.Simulator import *

regex = {
    'COMMENTARY': ['\(\* *([^)]| )* *\*\)'],
    'RULES': ['rule *[a-z]+ *='],
    'DECLARATIONS': ["let +[a-z]+ += *\n*([^\"' {}\n\t]|'(_| |\\\\[sntv])'|\"([^\"]| )+\")+"],
    'TOKENS': ["\| *([^\"' {}\n\t]|'(_| |\\\\[sntv])'|\"([^\"]| )+\")+ +\{[^{}]+\}"],
    'FIRST': ["([^\"' {}\n\t]|'(_| |\\\\[sntv])'|\"([^\"]| )+\")+ +\{[^{}]+\}", "([a-z])+"],
    'HEADER': ["\{([^{}]|\\\\\{|\\\\\})+\}"]
}

machine = import_module("yalexReader2.py", regex)

dictVar = {}

total_machines = {}

lastMachine = ''
isFirst = False
findHeader = False

orderPy = []


def eval_Text(text):
    global lastMachine, isFirst, orderPy, findHeader
    clear()
    # Tu lógica de evaluación aquí
    # Se asume que `exclusiveSim` y `machine` están definidos
    evaluate_text = exclusiveSim(machine, text)[:-1]
    new_eval = []
    passRules = False

    for message, token in evaluate_text:
        if token != 1 and token != 0:
            if (token == 'TOKENS' or token == 'FIRST') and not passRules:
                new_eval.append((message, 1))
                continue
            elif token == 'RULES':
                passRules = True
            elif token == 'DECLARATIONS' and passRules:
                passRules = False
                isFirst = False

        if token != 1 and token != 0 and token not in ['COMMENTARY', 'HEADER']:
            findHeader = True

        if token == 'DECLARATIONS':
            n = Eval_declaration(message)
            for m, t in n:
                new_eval.append((m, t))
            continue

        if token == 'HEADER':
            if not findHeader:
                head = message[1:-1].split('\n')

                if '\{' in message or '\}' in message:
                    for h in head:
                        orderPy.append(h.replace('\{', '{').replace('\}', '}'))
                    sepToEscapePre = message.split('\{')
                    sepToEscape = []
                    for sep in sepToEscapePre:
                        sepToEscape += sep.split('\}')

                    for sep in sepToEscape:
                        new_eval.append((sep, 'HEADER'))
                        new_eval.append(('\\', "ESCAPED"))
                        new_eval.append(('{', "ESCAPED"))

                    new_eval.pop()
                    new_eval.pop()
                    continue
                orderPy += head
                new_eval.append((message, 'HEADER'))
                continue

            else:
                new_eval.append((message, 1))
            continue

        if token == 'TOKENS':
            n = Eval_tokens(message)
            for m, t in n:
                new_eval.append((m, t))
            continue

        if token == 'FIRST':
            if isFirst:
                new_eval.append((message, 1))
                continue
            else:
                isFirst = True
                n = Eval_tokens(message)
                for m, t in n:
                    new_eval.append((m, t))
                continue

            continue

        if token == 'RULES':
            function_name = message[message.find('rule') + 5:message.find('=')].strip()
            if function_name in total_machines:
                new_eval.append((message, 1))
                continue
            total_machines[function_name] = {}
            lastMachine = function_name
            isFirst = False

        new_eval.append((message, token))


    return [(message, token) for message, token in new_eval]


def Eval_declaration(declaration):
    dcl = declaration.split('=', 1)
    new_eval = []
    if len(dcl) != 2:
        return [(declaration, 1)]

    new_eval.append(('let', 'LET'))

    nameVar = dcl[0].replace('let', '', 1).strip()
    spaces = dcl[0].replace('let', '', 1).split(nameVar)

    new_eval.append((spaces[0], 0))
    new_eval.append((nameVar, 'VARIABLE'))
    new_eval.append((spaces[1], 0))
    new_eval.append(('=', 0))

    valueVar = dcl[1].strip()

    spaces = dcl[1].split(valueVar)
    if len(spaces) > 0:
        new_eval.append((spaces[0], 0))

    valEval, _ = eval_Value(nameVar, valueVar)
    for message, token in valEval:
        new_eval.append((message, token))

    return [(message, token) for message, token in new_eval]


regex = {
    'IN_SET': ["\[([^a[]]|a|' ')*\]"],
    'IN_GROUP': ["\(([^\n \t]|'[\n \t]'|' '|\"(_| )+\"|[a-z])+\)"],
    'OPERATOR': ['\|', '\?', '\*', '^', '\+', '\#'],
    'SYMBOL': ["'[a-zA-Z0-9]'", "'[+*?|# ]'", "'''", "'[\n \t]'", "' '", "\_", "'[^a-zA-Z0-9']'"],
    'STRING': ['"(_| )+"']
}

regexInSet = {
    'IND': ["'[a-zA-Z0-9]'|' '", "'[^ ']'", "'\\t'"],
    'OPER': ["-"],
    'GROUP': ['"[^a]+"']
}

machineValue = import_module("varDefMachine3.py", regex)
machineSet = import_module("varDefMachineSET2.py", regexInSet)
setSA = import_module("onlyProduct.py", {'IN_SET': ["\[([^a[]]|a|' ')*\]"]})


def clear():
    global dictVar
    global machineValue
    global machineSet
    global total_machines
    global findHeader
    global orderPy
    global isFirst
    isFirst = False
    orderPy = []
    findHeader = False
    total_machines = {}
    dictVar = {}
    machineValue = import_module("varDefMachine3.py", regex)
    machineSet = import_module("varDefMachineSET2.py", regexInSet)


def eval_Value(var, value, notDo=False):
    global dictVar
    global machineValue

    def group(val):
        new_eval = []
        global machineValue
        global machineSet
        global setSA
        ev = exclusiveSim(machineValue, val)[:-1]

        def divideGroup(text):
            develText = []
            balance = 0
            textNow = ''
            eval_t = ''
            for chr in text:
                if chr == '(':
                    balance += 1
                    if len(eval_t) > 0:
                        develText.append((eval_t, "EVAL"))
                        eval_t = ''
                elif chr == ')':
                    balance -= 1
                    if balance == 0:
                        textNow += chr
                        develText.append((textNow, 'GROUP'))
                        textNow = ''
                        continue

                if balance == 0:
                    eval_t += chr
                    continue
                textNow += chr

            if textNow != '':
                develText.append((textNow, 1))
            return develText


        if len(ev) == 0:
            return [(val, 1)], '', True

        operation = ''
        error = False

        for message, token in ev:
            if token != 1 and token != 0:
                if token == 'IN_GROUP':
                    divideG = divideGroup(message)
                    for mD, tD in divideG:
                        if tD != 1:
                            if tD == 'GROUP':
                                toGroup = mD[1:-1]
                                if len(toGroup) == 0:
                                    new_eval.append((message, 1))
                                    continue
                                n, o, e = group(toGroup)
                                if e:
                                    error = True
                                operation += '(' + o + ')'
                                new_eval.append(('(', 0))
                                for m, t in n:
                                    new_eval.append((m, t))
                                new_eval.append((')', 0))
                            else:
                                n, o, e = group(mD)
                                if e:
                                    error = True
                                operation += o
                                for m, t in n:
                                    new_eval.append((m, t))
                        else:
                            new_eval.append((mD, tD))
                    continue
                elif token == 'IN_SET':
                    toSet = message[1:-1]
                    inSet = exclusiveSim(machineSet, toSet)
                    if len(inSet) <= 1 or len(toSet) <= 1:
                        new_eval.append((message, 1))
                        continue
                    if inSet[-1][1] != 1:
                        inSet = inSet[:-1]
                    new_eval.append(('[', 0))
                    operation += '['
                    for m, t in inSet:
                        if t == 'IND' or t == 'GROUP':
                            sym = m[1:-1]
                            new_eval.append((m.replace('\n', r'\n').replace('\t', r'\t').replace('\v', r'\v'), t))
                            operation += sym
                            continue
                        if t == 1:
                            error = True
                        new_eval.append((m, t))
                        operation += m
                    operation += ']'
                    new_eval.append((']', 0))
                    continue
                elif token == 'SYMBOL':
                    if message[0] == "'":
                        sym = message[1:-1]
                    else:
                        sym = message
                    if sym in '+*?|_(){}[]#\\' and sym != '':
                        sym = '\\' + sym

                    operation += sym
                    new_eval.append((message.replace('\n', r'\n').replace('\t', r'\t').replace('\v', r'\v'), 'SYM'))
                    continue
                elif token == 'STRING':
                    sym = '('

                    for chr in message[1:-1]:
                        if chr in '+*?|_(){}[]#\\':
                            sym += '\\'
                        sym += chr
                    sym += ')'
                    operation += sym
                    new_eval.append((message.replace('\n', r'\n').replace('\t', r'\t').replace('\v', r'\v'), 'SYM'))
                    continue
                elif token == 1:
                    error = True
                elif token == 'OPERATOR':
                    operation += message
                elif token != 0:
                    new_op = dictVar[message]

                    evOp = exclusiveSim(setSA, new_op)[:-1]
                    if len(evOp) == 1:
                        if evOp[0][1] != 1 and evOp[0][1] != 0:
                            operation += evOp[0][0]
                            new_eval.append((message, 'VARIABLE'))
                            continue

                    operation += '('
                    operation += dictVar[message]
                    operation += ')'

                    new_eval.append((message, 'VARIABLE'))
                    continue

                new_eval.append((message, token))
            else:
                if token == 1:
                    error = True
                new_eval.append((message, token))

        return new_eval, operation, error

    new_ev, op, er = group(value.replace(r'\n', '\n').replace(r'\t', '\t').replace(r'\v', '\v'))

    if er:
        raise Exception('ERROR EN LA EXPRESION', value)
    else:
        if value != '' and not notDo:
            dictVar[var] = op
            rg = {var: [var]}
            newMachine = prepareAFN(rg)
            machineValue.combine_States(newMachine)

    return new_ev, op


def Eval_tokens(token):
    global total_machines
    global dictVar
    global lastMachine
    new_eval = []
    regex = {
        'RETURN': ['\{[^{}]+\}'],
        'TOKEN': ["([^\"' {}\n\t]|'(_| |\\\\[sntv])'|\"([^\"]| )+\")+"],
        'Unit': ['\|']
    }

    machineToken = import_module("tokenMachine2.py", regex)
    # draw_AF(machine, legend=f'AFD minimized direct', expression='default', direct=True, name='AFD_min_direct')
    tk = {}
    rC = exclusiveSim(machineToken, token)[:-1]
    tokenName = ''
    regexDescription = ''
    for comp, type in rC:
        if type == 'TOKEN':
            if tokenName == '':
                tokenName = "print('"+comp.strip().replace("'", '"')+"')"
            regexDescription += eval_Value(var='', value=comp, notDo=True)[1]

        if type == 'RETURN':
            tokenName = comp[1:-1]
            tkS = ''
            for line in tokenName.split('\n'):
                tkS += '\t'+line.rstrip()+'\n'
            tokenName = tkS


        new_eval.append((comp, type))

    tk[tokenName.strip()] = [regexDescription]
    total_machines[lastMachine].update(tk)

    return [(message, token) for message, token in new_eval]


def create_mach(draws_machine=True, defect_file:str = ''):
    global total_machines, orderPy
    if len(total_machines) == 0:
        return

    cout = 2

    code = ''
    headerC = ''

    for i in orderPy:
        headerC += i + "\n"

    codes = []

    for machine in total_machines:
        mach = prepareAFN(total_machines[machine], draws_machine)
        code += translateToCode(mach, True, headerC)
        fileName = "./scaner/out_" + str(machine) + ".py" if defect_file == '' else defect_file
        defect_file = ''
        with open(fileName, 'w', encoding='utf-8') as fileW:
            fileW.write(code)
        cout += 1
        codes.append(fileName)
        if draws_machine:
            draw_AF(mach, legend=machine, expression=machine, name='Machine', useNum=True)

    return codes


def getTotal():
    global total_machines
    return len(total_machines)
