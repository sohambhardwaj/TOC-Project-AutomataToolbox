from graphviz import Digraph

def plotdfa(data):
    fa = Digraph(format = 'png')
    fa.attr(rankdir='LR')

    fa.attr('node', shape = 'doublecircle')
    for fst in data['finalStates']:
        fa.node(str(fst))
    
    fa.attr('node', shape = 'circle')
    for startnode in data['transition'].keys():
        for nodes in data['transition'][startnode]:
            if len(str(data['transition'][startnode][nodes]))==0 and len(str(startnode))==0 :
                fa.attr('node',shape='circle')
                fa.node('ϕ')
                fa.edge('ϕ','ϕ', label = nodes)
            elif len(str(data['transition'][startnode][nodes]))==0:
                fa.attr('node',shape='circle')
                fa.node('ϕ')
                fa.edge(str(startnode),'ϕ', label = nodes)
            else:
                fa.edge(str(startnode),str(data['transition'][startnode][nodes]), label = nodes)


    fa.attr('node', shape = 'point')
    fa.edge('',str(data['states'][0]))
    fa.render(filename='static/out', view=0, cleanup=1)