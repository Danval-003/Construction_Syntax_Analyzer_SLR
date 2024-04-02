import pandas as pd
import tabulate

from Machines_gen_usage.Classes_ import Grammar_Element, Production_Item, LRO_S, SLR_Table
from Machines_gen_usage.Simulator import exclusiveSim
from Machines_gen_usage.prepareAFD import *
from Machines_gen_usage.Draw_diagrams import draw_LR0


class yaPar_reader:
    def __init__(self, content):
        self.action_table2 = None
        self.table_printG: pd.DataFrame = pd.DataFrame()
        self.organize_list = None
        self.content = content
        self.error = False
        self.tokens: Dict[str, Grammar_Element] = dict()
        self.productions: Dict[str, Grammar_Element] = dict()
        self.FirstState = None
        self.predictive_table = None
        self.goto_table: pd.DataFrame = pd.DataFrame()
        self.table_printG2: pd.DataFrame = pd.DataFrame()
        self.action_table: pd.DataFrame = pd.DataFrame()
        self.firstProduct: 'Production_Item' or None = None
        self.symbols: Set[Grammar_Element] = set()
        self.lr0_states: Dict[int, LRO_S] = dict()
        self.LR0: LRO_S or None = None
        self.prsDict: Dict[int, Production_Item] = {}
        self.prod_list_toPrint = ''

    def organize(self):
        organize_machine = import_module('yaPar_reader.py',
                                         {
                                             'TK_SECTION': ['%token ([A-Z]| )+', 'IGNORE ([A-Z]| )+'],
                                             'PRODUCTION': ['[a-z]+:([a-zA-Z]| |\n|\|)+;'],
                                             'COMMENT': ['//.*\n', '/\*([^*/]|[^/]\*[^/]|[^*]/[^*])*\*/']
                                         })

        self.organize_list = exclusiveSim(organize_machine, self.content)
        prs = {}
        for message, tk in self.organize_list:
            if tk == 1:
                self.error = True
                break
            if tk == 'TK_SECTION':
                if '%token' in message:
                    message = message.replace('%token', '').strip()
                    message = message.split(' ')
                    for m in message:
                        self.tokens[m] = Grammar_Element(m, terminal=True)
                        self.symbols = self.symbols.union({self.tokens[m]})
                elif 'IGNORE' in message:
                    message2 = message.replace('IGNORE', '').strip()
                    message2 = message2.split(' ')
                    for m in message2:
                        if m in self.tokens:
                            self.tokens[m].ignore = True
                        else:
                            raise Exception('Token not found in', message)
                continue
            if tk == 'PRODUCTION':
                message2 = message.split(':')
                prName = message2[0]
                if prName in self.productions:
                    raise Exception('Production already exists', message)
                self.productions[message2[0]] = Grammar_Element(message2[0])
                self.symbols = self.symbols.union({self.productions[message2[0]]})
                if self.FirstState is None:
                    self.FirstState = self.productions[message2[0]]
                message2 = message2[1][:-1].strip().split('|')
                prs[prName] = message2

        count_prod = 2
        for key in self.productions:
            for pr in prs[key]:
                pr = pr.strip().split(' ')
                production = []
                for p in pr:
                    if p in self.tokens:
                        production.append(self.tokens[p])
                    elif p in self.productions:
                        production.append(self.productions[p])
                    else:
                        raise Exception('Token not found in definition to production', key, p)

                self.prsDict[count_prod] = self.productions[key].transition_to(production, count_prod)
                count_prod += 1

        newInit = Grammar_Element(self.FirstState.value + "\'")
        lastState: Grammar_Element = Grammar_Element('$', terminal=True)
        self.tokens['$'] = lastState
        self.firstProduct = newInit.transition_to([self.FirstState, lastState], 1)
        self.prsDict[1] = self.firstProduct
        self.FirstState = newInit
        self.productions[newInit.value] = newInit

        self.FirstState.calculateFirst()
        self.FirstState.calculateFollow()
        self.FirstState.resetFirstFollow()
        for val in self.productions.values():
            val.resetFirstFollow()
            val.calculateFirst()
            val.calculateFollow()

        # Organize the content
        return self.content

    def LROrganize(self):
        count = 1
        initState = LRO_S(self.firstProduct.closureCalc(), 0)
        self.lr0_states[0] = initState
        toEvaluate: List[LRO_S] = [initState]
        lrsStates: Dict[LRO_S, LRO_S] = {initState: initState}

        while len(toEvaluate) > 0:
            state = toEvaluate.pop(0)
            for symbol in self.symbols:
                newState = set()
                for item in state.state:
                    passItem, newItem = item.passPoint(symbol)
                    if passItem:
                        closureNewItem = newItem.closureCalc()
                        for i in closureNewItem:
                            newState.add(i)

                if len(newState) != 0:
                    newLR0 = LRO_S(newState, count)
                    if newLR0 not in lrsStates:
                        lrsStates[newLR0] = newLR0
                        toEvaluate.append(newLR0)
                        self.lr0_states[count] = newLR0
                        count += 1
                    else:
                        newLR0 = lrsStates[newLR0]
                    state.transitions[symbol] = newLR0

        self.LR0 = initState

        return initState

    def graphLRO(self):
        if self.LR0 is None:
            self.LR0 = self.LROrganize()

        draw_LR0(self.LR0, 'AF', 'default')
        draw_LR0(self.LR0, 'AF', 'default', useNum=True)

    def obtainGrammarElement(self, value):
        if value in self.tokens:
            return self.tokens[value]
        return None

    def getItem(self, value):
        if value in self.prsDict:
            return self.prsDict[value]
        return None

    def getSLRTable(self):
        self.action_table = pd.DataFrame(columns=[str(x.value).strip() for x in self.symbols] + ['$'],
                                         index=[str(x) for x in range(len(self.lr0_states))])
        self.action_table2 = self.action_table.copy()
        self.table_printG = self.action_table.copy()

        print('States LR0')

        for num, state in self.lr0_states.items():
            for item in state.non_completed_Ter:
                term = item.poitElement()
                if term.value == '$':
                    self.action_table.at[str(num), '$'] = ('A', [])
                    self.action_table2.at[str(num), '$'] = ('A', [])
                    self.table_printG.at[str(num), '$'] = "Accept!"
                    continue
                self.action_table.at[str(num), str(term.value)] = ('S', state.transitions[term])
                self.action_table2.at[str(num), str(term.value)] = ('S', state.transitions[term].numState)
                self.table_printG.at[str(num), str(term.value)] = 'S' + str(state.transitions[term].numState)

            for item in state.non_completed_NonTer:
                nonTerm = item.poitElement()
                self.action_table.at[str(num), str(nonTerm.value).strip()] = ('Goto', state.transitions[nonTerm])
                self.action_table2.at[str(num), str(nonTerm.value).strip()] = (
                    'Goto', state.transitions[nonTerm].numState)
                self.table_printG.at[str(num), str(nonTerm.value).strip()] = state.transitions[nonTerm].numState

            for item in state.complete:
                if item.original == self.firstProduct:
                    continue

                first = item.NonTerminal.follow
                for f in first:
                    self.action_table.at[str(num), str(f)] = ('R', self.prsDict[item.count])
                    self.action_table2.at[str(num), str(f)] = ('R', (self.prsDict[item.count].NonTerminal.value,
                                                                     len(self.prsDict[item.count].Result)))
                    self.table_printG.at[str(num), str(f)] = 'R' + str(item.count)

        print('table')
        print(tabulate.tabulate(self.table_printG, headers='keys', tablefmt='psql'))
        toIgnore: Set[str] = {elem.value for elem in self.tokens.values() if elem.ignore}
        for key in sorted(self.prsDict.keys()):
            item = self.prsDict[key]
            print(key, str(item), str(item.count))
            self.prod_list_toPrint += str(key) + ' ' + str(item) + '\n'
        return SLR_Table(self.action_table2, self.table_printG, set(self.tokens.keys()), self.LR0.numState, toIgnore,
                         product_list_toPrint=self.prod_list_toPrint)

    def obtainAction(self, state, symbol):
        return self.action_table.at[str(state), str(symbol)], self.table_printG.at[str(state), str(symbol)]
