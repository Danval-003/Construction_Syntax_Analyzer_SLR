from typing import *
from Machines_gen_usage.CharsSet import *


def reader(filename: str) -> str:
    contents = []
    """Reads a file and returns its contents"""
    with open(filename, 'r', encoding='utf-8') as archivo:
        line = archivo.readlines()
        for i in line:
            contents.append(str(i[:-1]+' \n ' if i[-1] == '\n' or i[-1] == '' else i))

    return ''.join(contents)


def transformsChar(contents: List[str]) -> List[List[str or int]]:
    """Transforms the characters into their respective values"""
    transformed = []
    escaped = False

    def evalSet(content):
        if content[-1] == r'\\':
            return set(), False
        totalSet = set()
        negation = content[0] == '^'
        i = 1 if negation else 0
        negSet = set()
        while i < len(content) - 2:
            chLast = content[i]
            ch = content[i + 1]
            chNext = content[i + 2]

            if chLast == '\\':
                i += 1
                continue

            if chLast == '-':
                return set(), False

            if chLast != '' or chLast != ' ':
                if ch == '-':
                    if chLast != '' and chNext != '' and ch != '' and chNext != '':
                        if ord(chLast) > ord(chNext):
                            return set(), False

                        obSet = set(obtainSet(chLast, chNext))
                        if not negation:
                            totalSet = totalSet.union(obSet)
                        else:
                            negSet = negSet.union(obSet)
                        i += 3
                        continue
                    else:
                        return set(), False
                else:
                    if not negation:
                        totalSet.add(chLast)
                    else:
                        negSet.add(chLast)
            i += 1

        if len(content) - 1 == i:
            totalSet.add(content[i])
        elif len(content) - 2 == i:
            if content[i + 1] == '-' and content[i + 1] == r'\\':
                return set(), False
            if content[i] != ' ':
                totalSet.add(content[i])
            if content[i + 1] != ' ':
                totalSet.add(content[i + 1])

        if negation:
            negSet = negSet.union(totalSet)
            totalSet = set(globalChars()).difference(negSet)

        return totalSet, True

    for line in contents:
        transformed.append([])
        balance = 0
        onQua = ''
        charIndex = 0
        seted = set()
        isDiff = False
        Error = False
        while charIndex < len(line):
            if line[charIndex] in '[' and not escaped:
                balance = 1
                inSet = ''
                setted = set()
                funtion = False
                c_in = 0
                for b_in in range(charIndex + 1, len(line)):
                    c_in += 1
                    if line[b_in] == ']':
                        balance -= 1
                        if balance == 0:
                            setted, funtion = evalSet(inSet)
                            break
                    elif line[b_in] == '[':
                        balance += 1
                    inSet += line[b_in]
                if not funtion or balance != 0:
                    break

                if isDiff:
                    setted = seted.difference(setted)
                    isDiff = False

                if charIndex + c_in + 1 < len(line):
                    if line[charIndex + c_in + 1] == '#':
                        isDiff = True
                        charIndex = charIndex + c_in + 2
                        seted = setted
                        continue

                if len(setted) > 0:
                    transformed[-1].append('(')
                    for element in setted:
                        transformed[-1].append(ord(element))
                        transformed[-1].append('|')
                    transformed[-1].pop()
                    transformed[-1].append(')')
                charIndex = charIndex + c_in + 1
                continue

            if line[charIndex] == '\\':
                if not escaped:
                    escaped = True
                    charIndex += 1
                    continue
                else:
                    transformed[-1].append(ord(line[charIndex]))
                    escaped = False
                    charIndex += 1
                    continue

            if line[charIndex] in '_' and not escaped:
                transformed[-1].append('(')
                for chrI in globalChars():
                    transformed[-1].append(ord(chrI))
                    transformed[-1].append('|')
                transformed[-1].pop()
                transformed[-1].append(')')
                charIndex += 1
                continue

            if line[charIndex] == '#' and not escaped:
                charIndex += 1
                continue

            if line[charIndex] in '({*|?+)}' and not escaped:
                transformed[-1].append(line[charIndex])
                charIndex += 1
                continue

            transformed[-1].append(ord(line[charIndex]))

            escaped = False
            charIndex += 1
        if isDiff:
            if len(setted) > 0:
                transformed[-1].append('(')
                for element in setted:
                    transformed[-1].append(ord(element))
                    transformed[-1].append('|')
                transformed[-1].pop()
                transformed[-1].append(')')

    return transformed


def validate(contents: List[List[str or int]]) -> List[List[str or int]]:
    """Validates the contents of the file are correct expressions"""
    counterparty = {
        '(': ')',
        '[': ']',
        '{': '}',
        ')': '(',
        ']': '[',
        '}': '{',
    }

    accepted = []

    '''Validate the expressions are balanced'''
    for line in contents:
        pila_regex = []
        test = True
        for character in line:
            if str(character) in '([{':
                pila_regex.append(character)
            elif str(character) in ')]}':
                if pila_regex:
                    if counterparty[pila_regex[-1]] == character:
                        pila_regex.pop()
                    else:
                        test = False
                        break
                else:
                    test = False
                    break

        if len(pila_regex) == 0 and test:
            accepted.append(line)

    return accepted
