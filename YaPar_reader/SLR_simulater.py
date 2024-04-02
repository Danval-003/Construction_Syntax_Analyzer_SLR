import pandas as pd

from YaPar_reader.yapar_reader import yaPar_reader
from Machines_gen_usage.Classes_ import LRO_S, Grammar_Element, Production_Item, SLR_Table
from typing import *
import tabulate


def SLR_simulate(content:str, reader: 'SLR_Table'):
    contentTokens: List[str] = []
    for element in content.split(' '):
        el = element.strip()
        if el == '':
            continue
        tk = reader.obtainGrammarElement(el)
        if tk == 1:
            raise Exception('Token not found in', element)
        if tk == 2:
            continue
        contentTokens.append(el)

    contentTokens.append('$')

    stateStack: List[int] = [reader.firstState]
    df_stack = {}

    while True:
        stateOn = stateStack[-1]
        actualToken = contentTokens[0]
        action, desc = reader.obtainAction(stateOn, actualToken)
        df_stack['State'] = [str(st) for st in stateStack]
        df_stack['Input'] = [str(tk) for tk in contentTokens]
        df_stack['Action'] = [desc if not pd.isna(desc) else 'Error!']
        print(tabulate.tabulate(df_stack, headers='keys', tablefmt='psql'))

        if pd.isna(action) or action is None:
            print('\033[91m', 'Reject!', '\033[0m')
            raise Exception('Error!, not accepted')
        if action[0] == 'S':
            stateStack.append(action[1])
            contentTokens.pop(0)
        elif action[0] == 'R':
            prod: Tuple[str, int] = action[1]

            for _ in range(prod[1]):
                stateStack.pop()

            stateOn = stateStack[-1]
            A = prod[0]
            newAction, desc = reader.obtainAction(stateOn, A)
            if newAction is None or pd.isna(newAction):
                raise Exception('Action not found in', stateOn, A)
            stateStack.append(newAction[1])
        elif action[0] == 'A':
            break

    print('\033[92m','Accepted!', '\033[0m')

    return True
