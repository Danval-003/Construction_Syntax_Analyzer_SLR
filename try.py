from Classes_ import State

a1 = State('a1')
a0 = State('a0')
a0.add_transition(92, a1)

a1.isFinalState = True
a1.addToken('HEADER')

