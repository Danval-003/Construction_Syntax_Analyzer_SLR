from Machines_gen_usage import Colors as cl


def erroPrincipalReader(response):
    dictTokens = dict()
    rules = False
    error = False
    count = 1
    for text, token in response:
        if token == 0:
            continue
        if token == 'RULES':
            rules = True
            count += 1
            continue
        if rules:
            if token == 'DECLARATIONS':
                print(cl.RED, 'Error declaracion despues de rules', cl.RESET)
                error = True
                break
        else:
            if token == 'NORMAL' or token == 'TOKENS':
                print(cl.RED, 'Error declaracion de tokens antes de rules', cl.RESET)
                error = True
                break
        if token == 1:
            print(cl.YELLOW, f'Error en la linea {count}: ' + text, cl.RESET)
            error = True
            break
        if token in dictTokens:
            dictTokens[token].append(text)
        else:
            dictTokens[token] = [text]
        count += 1

    if not rules:
        print(cl.RED, 'Error no se encontraron las reglas', cl.RESET)
        error = True
    if 'TOKENS' not in dictTokens:
        print(cl.RED, 'Error no se encontraron los tokens', cl.RESET)
        error = True

    return dictTokens, error


def generalError(line, type=''):
    print('Error en el archivo', line, type)
    return True
