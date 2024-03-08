from prepareAFD import *
import ErroManagerReaders as err
from varDefinitios import *
from Draw_diagrams import *
from Simulator import *

regexInSet = {
    'IN_SET': ["\[([^a[]]|a|' ')*\]"],
    'IN_GROUP': ["\(([^\n \t]|'[\n \t]'|' '|\"(_| )+\"|[a-z])+\)"],
    'OPERATOR': ['\|', '\?', '\*', '^', '\+', '\#'],
    'SYMBOL': ["'[a-zA-Z0-9]'", "'[+*?|# ]'", "'''", "'[\n \t]'", "' '", "\_", "'[^a-zA-Z0-9']'"],
    'STRING': ['"(_| )+"']
}

if __name__ == "__main__":
    machine = prepareAFN( regexInSet)
    sim = exclusiveSim(machine, "digits(.digits)?('E'['+''-']?digits)?")
    print(sim)

