import json
def create_nfa(trans,allStates,ss,es,tp):
    print(trans)
    states=allStates.split()
    # print(states)
    startState=ss
    finalStates=es.split()
    # print(finalStates)
    terminals=tp.split()
    transition={}
    transition[startState]={}
    for path in terminals:
        transition[startState][path]=[]
    for state in states[1:]:
        transition[state]={}
        for path in terminals:
            transition[state][path]=[]
    for t in trans:
        if len(t)!=0:
            t=t.split()
            transition[t[0]][t[1]]=[x for x in t[2:]]
    nfa={
        "states":states,
        "startState":startState,
        "terminals":terminals,
        "transition":transition,
        "finalStates":finalStates
    }
    outfile=open("uploads/nfa.json","w")
    json.dump(nfa,outfile,indent=4)