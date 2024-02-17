from Simulator import *
from prepareAFD import *
import ErroManagerReaders as err
from varDefinitios import *
from Draw_diagrams import *

if __name__ == '__main__':
    """Read the file and return its contents"""
    contents: str = reader('slr-1.yal').replace(r'\t', '\t').replace(r'\n', '\n').replace(r'\r', '\r').replace(r'\v',
                                                                                                               '\v').replace(
        r'\f', '\f').replace('\\s', r'\s')
    regex = {
        'COMMENTARY': ['\(\*([^)]| )*\*\)'],
        'RULES': ['rule *tokens *='],
        'DECLARATIONS': ["let [a-z]+ = *([^=]|['[]*|?.]|' ')+"],
        'TOKENS': ["([a-z]|'[^a]')+ +\{ *return *[A-Z]+ *\}|([a-z])+", "\| ([a-z]|'[^a]')+ +\{ *return *[A-Z]+ *\}"]
    }

    machine = import_module("yalexReader.py", regex)

    regex = {
        'VARIABLE': ['let [a-z]+ ='],
        'VALUE': [" *([^=]|['[]*|?.]|' ')+"]
    }

    machineDecl = import_module("declarationReader.py", regex)

    principalRead = exclusiveSim(machine, contents)

    dictResult, error = err.erroPrincipalReader(principalRead)

    if error:
        print('Errores en el archivo')
    else:
        listVar: List[Tuple[str, str]] = []
        for text in dictResult['DECLARATIONS']:
            variableAttributes = exclusiveSim(machineDecl, text)
            nameVar = ''
            valueVar = ''
            for var in variableAttributes:
                if var[1] == 'VARIABLE':
                    nameVar = var[0].replace('let', ' ', 1).replace('=', '').strip()
                else:
                    valueVar = var[0].strip()
            listVar.append((nameVar, valueVar))

        dVar = defVariables(listVar)

        tokens = []

        for text in dictResult['TOKENS']:
            if text[0] == '|':
                tokens.append(text.replace('|', '', 1).strip())
            else:
                tokens.append(text)

        defToken = defTokens(dVar, tokens)

        draw_AF(defToken, legend=f'AFD minimized direct', expression='default')
