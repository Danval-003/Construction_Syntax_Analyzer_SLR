from Machines_gen_usage.Draw_diagrams import *
from Machines_gen_usage.Simulator import *
from Machines_gen_usage.prepareAFD import *

regexInSet = {
    'HEADER': ["(\\\\)"]
}

if __name__ == "__main__":
    machine = import_module('try.py', regexInSet)
    draw_AF(machine, 'AFD', 'try', True, 'AFD', True)
    sim = exclusiveSim(machine, "\\")
    print(sim)

