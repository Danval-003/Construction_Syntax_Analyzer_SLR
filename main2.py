from prepareAFD import *
from Draw_diagrams import *
from Simulator import *

contents = reader('slr-1.yal')

z = prepareAFN({'HOLA': ["[a-b]([a-b]|[0-2])*"]})

draw_AF(z, legend=f'AFD minimized direct {contents[0]}', expression='default', direct=True, name='AFD_min_direct')


