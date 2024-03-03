from prepareAFD import *
from Draw_diagrams import *
from Simulator import *

contents = reader('slr-1.yal')

z = prepareAFN({
        'IN_SET': ["\[([^a]|a|' ')*\]"],
        'IN_GROUP': ["\( *([^a()]|a)+ *\)"],
        'OPERATOR': ['\|', '\?', '\*', '^', '\+'],
        'SYMBOL': ["'[a-zA-Z0-9]'|[^+*?() |]|."]
    })

xd = exclusiveSim(z, "digits(.digits)?('E'['+''-']?digits)?")

print(xd)
