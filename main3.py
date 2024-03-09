from prepareAFD import *
import ErroManagerReaders as err
from varDefinitios import *
from Draw_diagrams import *
from Simulator import *

regexInSet = {
    'HEADER': ["(\\\\)"]
}

if __name__ == "__main__":
    machine = import_module( 'try.py', regexInSet)
    draw_AF(machine, 'AFD', 'try', True, 'AFD', True)
    sim = exclusiveSim(machine, "\\")
    print(sim)

