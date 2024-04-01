from Machines_gen_usage.Classes_ import *
import graphviz


def draw_tree(f_node: Node, expression='default', direct=False, useNum=False):
    dot = graphviz.Digraph(comment='Tree')

    def draw_node(node: Node):
        nonlocal useNum
        label = str(node.value) if isinstance(node.value, str) or useNum else chr(node.value)
        dot.node(node.getId(), label=label)
        if node.left is not None:
            dot.edge(node.getId(), node.left.getId())
            draw_node(node.left)
        if node.right is not None:
            dot.edge(node.getId(), node.right.getId())
            draw_node(node.right)

    draw_node(f_node)

    dot.render('Tree.gv', view=True, directory='./Tree/' + expression + '/' + ('Direct' if direct else 'Infix'))


def draw_AF(initState: State, legend: str = 'AF', expression='default', direct=False, name='AFN', useNum=False):
    dot: 'graphviz.graphs.Digraph' = graphviz.Digraph(comment='AFN')
    dot.attr(rankdir='LR')
    setStates = set()

    dot.attr(label=legend)

    def draw_state(state: 'State'):
        nonlocal useNum
        setStates.add(state.getId())
        dot.node(state.getId(), label=state.value, shape='doublecircle' if state.isFinalState else 'circle')
        for transition in state.transitions:
            for destiny in state.transitions[transition]:
                if destiny.getId() not in setStates:
                    draw_state(destiny)
                label = str(transition) if isinstance(transition, str) or useNum else chr(transition)
                dot.edge(state.getId(), destiny.getId(), label=label)

    draw_state(initState)

    dot.render(name + '.gv', view=True, directory='./machine/' + expression)


def draw_LR0(initState: LRO_S, legend: str = 'AF', expression='default', useNum=False):
    dot: 'graphviz.graphs.Digraph' = graphviz.Digraph(comment='LR0')
    dot.attr(rankdir='LR')
    setStates = set()
    dot.attr(label=legend)

    def draw_state(state: 'LRO_S'):
        nonlocal useNum
        setStates.add(state)
        name = str(state.numState) if useNum else str(state)
        dot.node(str(state.numState), label=name,
                 shape='doublecircle' if state.isFinalState else 'circle')
        for transition in state.transitions:
            destiny = state.transitions[transition]
            if destiny not in setStates:
                draw_state(destiny)
            dot.edge(str(state.numState), str(destiny.numState), label=transition.value)

    draw_state(initState)

    typeGraph = 'explicit' if useNum else 'implicit'

    dot.render('LR0_' + typeGraph + '.gv', view=True, directory='./LR0/' + expression)
