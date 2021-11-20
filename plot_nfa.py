from graphviz import Digraph
def plotnfa(data):
    # print (data['transition'])
    fa = Digraph(format = 'png')
    fa.attr(rankdir='LR')
    fa.attr('node', shape = 'doublecircle')
    for x in data['finalStates']:
        fa.node(str(x))
    transition=[]
    for state in data['transition']:
        for path in data['transition'][state]:
            if len(data['transition'][state][path])!=0:
                for final in data['transition'][state][path]:
                    transition.append([state,path,final])
    print(transition)
    fa.attr('node', shape = 'circle')
    for trans in transition:
        fa.edge(str(trans[0]),str(trans[2]), label = trans[1])

    fa.attr('node', shape = 'point')
    fa.edge('',data['startState'])

    fa.render(filename='static/in', view=0, cleanup=1) 