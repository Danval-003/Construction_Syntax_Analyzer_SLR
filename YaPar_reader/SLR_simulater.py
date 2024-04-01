import pandas as pd

from YaPar_reader.yapar_reader import yaPar_reader
from Machines_gen_usage.Classes_ import LRO_S, Grammar_Element, Production_Item
from typing import *
import tabulate


def SLR_simulate(content, reader: 'yaPar_reader'):
    contentTokens: List[Grammar_Element] = []
    for element in content.split(' '):
        el = element.strip()
        if el == '':
            continue
        tk = reader.obtainGrammarElement(el)
        if tk is None:
            raise Exception('Token not found in', element)
        contentTokens.append(tk)

    contentTokens.append(reader.obtainGrammarElement('$'))

    if reader.LR0 is None:
        raise Exception('LR0 not found')

    stateStack: List[LRO_S] = [reader.LR0]
    df_stack = {}

    while True:
        stateOn = stateStack[-1]
        actualToken = contentTokens[0]
        action, desc = reader.obtainAction(stateOn.numState, actualToken.value)
        df_stack['State'] = [str(st.numState) for st in stateStack]
        df_stack['Input'] = [str(tk) for tk in contentTokens]
        df_stack['Action'] = [desc]
        print(tabulate.tabulate(df_stack, headers='keys', tablefmt='psql'))

        if pd.isna(action) or action is None:
            raise Exception('Action not found in', stateOn.numState, actualToken.value)
        if action[0] == 'S':
            stateStack.append(action[1])
            contentTokens.pop(0)
        elif action[0] == 'R':
            production: Production_Item = action[1]

            for _ in range(len(production.Result)):
                stateStack.pop()

            stateOn = stateStack[-1]
            A = production.NonTerminal
            newAction, desc = reader.obtainAction(stateOn.numState, A.value)
            if newAction is None or pd.isna(newAction):
                raise Exception('Action not found in', stateOn.numState, A.value)
            stateStack.append(newAction[1])
        elif action[0] == 'A':
            break

    print('Accepted')

    return True
