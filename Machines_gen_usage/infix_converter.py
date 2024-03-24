from typing import *


def is_operator(token):
    operators = "|?.+*^"
    return token in operators


def precedence(operator: str) -> int:
    return {
        '(': 1, ')': 1, '[': 1, ']': 1, '{': 1, '}': 1,
        '|': 2, '.': 3, '?': 4, '*': 4, '+': 4, '^': 5, '∗': 4,
    }.get(operator, -1)


def counterSymbol(character: str) -> str:
    return {
        '(': ')',
        '[': ']',
        '{': '}',
        ')': '(',
        ']': '[',
        '}': '{',
    }.get(character, ' ')


def is_binary(token):
    operators = "^|"
    return token in operators


def extract_alphabet(content: List[List[str or int]]) -> List[Set[int]]:
    """Extracts the alphabet from the regular expressions"""
    alphabet: List[Set[int] or None] = []

    for expression in content:
        setAlpha = set()
        for exp_ in expression:
            if isinstance(exp_, int):
                if exp_ != ord('ε'):
                    setAlpha.add(exp_)
        alphabet.append(setAlpha)
    return alphabet


def format_regex(content: List[List[str or int]]) -> List[List[str or int]]:
    """Formats the regular expressions to be used in the program"""
    formatted: List[List[str or int] or None] = []

    def format_(expression_: List[str or int]) -> List[str or int]:
        result = []
        balance = 0
        toRecursion = []

        if len(expression_) == 0:
            return []

        expression_.append('')

        for chIndex in range(len(expression_) - 1):
            ch = expression_[chIndex]
            chNext = expression_[chIndex + 1]
            if str(ch) in '([{':
                balance += 1
            elif str(ch) in ')]}':
                balance -= 1
                if balance == 0:
                    toRecursion = toRecursion[1:]
                    postRecursion = ['('] + format_(toRecursion)
                    postRecursion.append(')')
                    result.append(postRecursion)
                    toRecursion = []
                    if str(chNext) not in ')]}+|*' and str(chNext) != '' and str(chNext) != '|' and len(result) > 0:
                        if result[-1] != '.':
                            result.append('.')
                elif str(chNext) not in ')]}+|*' and str(chNext) != '' and str(chNext) != '|' and len(result) > 0:
                    if toRecursion[-1] == '.':
                        toRecursion.pop()
                    if toRecursion[-1] == '.':
                        toRecursion.pop()
                    if toRecursion[-1] == '.':
                        toRecursion.pop()
                    toRecursion.append(')')
                    toRecursion.append('.')
                else:
                    toRecursion.append(ch)
                continue

            if balance != 0:
                toRecursion.append(ch)
            else:
                if str(ch) == '*':
                    last = result.pop()
                    last = last if last != '.' else result.pop()
                    last = last if last != '.' else result.pop()
                    last = last if isinstance(last, list) else [last]
                    kleen = ['('] + last + ['*', ')']
                    result.append(kleen)
                    if isinstance(chNext, int) or str(chNext) in '([{':
                        result.append('.')
                elif str(ch) == '+':
                    last = result.pop()
                    last = last if last != '.' else result.pop()
                    last = last if last != '.' else result.pop()
                    last = last if isinstance(last, list) else [last]
                    plus = ['('] + last + ['.'] + last + ['*', ')']
                    result.append(plus)
                    if isinstance(chNext, int) or str(chNext) in '([{':
                        result.append('.')
                elif str(ch) == '?':
                    last = result.pop()
                    last = last if last != '.' else result.pop()
                    last = last if last != '.' else result.pop()
                    last = last if isinstance(last, list) else [last]
                    interrogation = ['(', last, '|', ord('ε'), ')']
                    result.append(interrogation)
                    if isinstance(chNext, int) or str(chNext) in '([{':
                        result.append('.')
                elif str(ch) == '|':
                    if result[-1] == '|' or result[-1] == '.':
                        result.pop()
                    if result[-1] == '.':
                        result.pop()
                    result.append('|')
                else:
                    result.append(ch)
                    if (isinstance(chNext, int) or str(chNext) in '([{') and str(chNext) != '|+*])}' and str(ch) != '|':
                        result.append('.')

        result = result[:-1] if result[-1] == '.' else result

        notListed = []

        def notListed_(result_):
            for elem_ in result_:
                if isinstance(elem_, list):
                    notListed_(elem_)
                else:
                    notListed.append(elem_)

        for i in result.copy():
            if isinstance(i, list):
                notListed_(i)
            else:
                notListed.append(i)

        notListed = notListed if notListed[-1] != '' else notListed[:-1]

        return notListed

    for expression in content:
        elem = []
        for element in expression:
            if isinstance(element, int):
                elem.append(element)
            else:
                if element in '([{':
                    elem.append('(')
                elif element in ')]}':
                    elem.append(')')
                else:
                    elem.append(element)

        new_el = format_(elem)

        formatted.append(new_el)

    new_formatted = []
    for elem in formatted:
        last = ''
        lastted = ''
        elem_ = []
        for ch in elem:
            if last == '.' and ch == '.' and lastted == '.':
                elem_.pop()
                continue

            if last == '|' and ch == '|' and lastted == '|':
                elem_.pop()
                continue

            if last == '.' and ch == '.':
                continue

            if last == '|' and ch == '|':
                continue
            lastted = last
            last = ch
            elem_.append(ch)
        new_formatted.append(elem_)


    return new_formatted


def translate_to_postfix(content: List[List[str]]) -> List[List[str or int]]:
    """Converts regulars expressions from infix to postfix notation whit shutting yard algorithm"""
    postfix_format: List[str or int] = []

    def infix_to_postfix(regex: List[str or int]) -> List[str or int]:
        queue: List[str or int] = []
        stack: List[str or int] = []

        for token in regex:
            if token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    queue.append(stack.pop())
                stack.pop()
            elif is_operator(str(token)):
                while stack and precedence(stack[-1]) >= precedence(token):
                    queue.append(stack.pop())
                stack.append(token)
            else:
                queue.append(token)

        return queue + stack[::-1]

    for expression in content:
        postfix_format.append(infix_to_postfix(expression))

    return postfix_format
