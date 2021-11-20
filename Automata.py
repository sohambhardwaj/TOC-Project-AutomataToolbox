import string
from collections import defaultdict

from graphviz import Digraph

star = '*'
plus = '+'
dot = '·'
leftBracket, rightBracket = '(', ')'
non_symbols = ['+', '*', '.', '(', ')']
symbols = list(string.ascii_uppercase) + list(string.ascii_lowercase) + ['0','1','2','3','4','5','6','7','8','9']
epsilon = 'ε'


class Automata:
    """
    Automata class to represnt any automata.
    states: set(int), set of all states present
    symbol: set, { a,b,...},  symbols or transition paths present in the automata
    transitions: dictionary inside dictionary. default dict to avoid key error
        eg. transitions[2][3]='a' , means transition from 2 to 3 exists using the path 'a'
            transitions[4][5]='b' , means transition from 4 to 5 exists using the path 'b'
    startState: 1 or 2 or ... , initial state of Automata
    finalStates: list, final state of Automata
    """


    def __init__(self, symbol = set()):
        self.states = set()
        self.symbol = symbol    # input symbol
        self.transitions = defaultdict(defaultdict)
        self.startState = None
        self.finalStates = []

    def setStart(self, state):
        self.startState = state
        self.states.add(state)

    def addFinal(self, state):
        if isinstance(state, int):
            state = [state]
        for s in state:
            if s not in self.finalStates:
                self.finalStates.append(s)

    def addTransition(self, fromstate, tostate, inputch):   # add only one 
        if isinstance(inputch, str):
            inputch = set(inputch)
        self.states.add(fromstate)
        self.states.add(tostate)
        if fromstate in self.transitions and tostate in self.transitions[fromstate]: # if state already reachable by some other path then union the other path
            self.transitions[fromstate][tostate] = \
            self.transitions[fromstate][tostate].union(inputch)
        else:
            self.transitions[fromstate][tostate] = inputch

    def addTransition_dict(self, transitions):  # add transitions of smaller nfa to the bigger nfa
        for fromstate, tostates in transitions.items():
            for state in tostates:
                self.addTransition(fromstate, state, tostates[state])

    def newBuildFromNumber(self, startnum):
        # print(startnum)
    # change the states' representing number to start with the given startnum
        translations = {}
        for i in self.states:
            translations[i] = startnum
            startnum += 1
        rebuild = Automata(self.symbol)
        rebuild.setStart(translations[self.startState])
        rebuild.addFinal(translations[self.finalStates[0]])
        for fromstate, tostates in self.transitions.items():
            for state in tostates:
                rebuild.addTransition(translations[fromstate], translations[state], tostates[state])
        return [rebuild, startnum]

    def getEpsilonClosure(self, state):
        # print(state)
        ecstates = set() 
        states = [state]
        while len(states):
            state = states.pop()
            ecstates.add(state) # current states is always a part of its epsilon closure
            if state in self.transitions:
                for tostate in self.transitions[state]:
                    if epsilon in self.transitions[state][tostate] and tostate not in ecstates:
                        states.append(tostate)
        return ecstates

    def reachableStates(self, state, skey):
        if isinstance(state, int):
            state = [state]
        trstates = set()
        for st in state:
            if st in self.transitions:
                for tns in self.transitions[st]:
                    if skey in self.transitions[st][tns]:
                        trstates.add(tns)
        #trstates contain all the reachable states by epsilon closure when travelled through ch
        return trstates

    def display(self, fname, pname):
        print(self.transitions)
        fa = Digraph(pname, filename = fname, format = 'png')
        fa.attr(rankdir='LR')

        fa.attr('node', shape = 'doublecircle')
        for fst in self.finalStates:
            fa.node(chr(fst+64),color="red",width="0.7")

        fa.attr('node', shape = 'circle')
        for fromstate, tostates in self.transitions.items():
            for state in tostates:
                tmp = ''
                for s in tostates[state]:
                    tmp += s # Union
                fa.edge(chr(fromstate+64),chr(state+64), label = tmp,arrowhead="vee")

        fa.attr('node', shape = 'point')
        fa.edge('', chr(self.startState+64))

        fa.attr('node', shape = 'circle')
        fa.node(chr(self.startState+64),color="green")

        fa.render("static/"+fname,view=False, cleanup=True)

        if fname=="dfa.gv":
            fa = Digraph(pname, filename = fname, format = 'png')
            fa.attr(rankdir='LR')

            fa.attr('node', shape = 'doublecircle')
            for fst in self.finalStates:
                stateset='{'+','.join([chr(x+64) for x in self.allstates[fst]])+'}'
                fa.node(stateset,color="red",width="1")

            fa.attr('node', shape = 'circle')
            for fromstate, tostates in self.transitions.items():
                for state in tostates:
                    tmp = ''
                    for s in tostates[state]:
                        tmp += s
                    fa.edge('{'+','.join([chr(x+64) for x in self.allstates[fromstate]])+'}','{'+','.join([chr(x+64) for x in self.allstates[state]])+'}', label = tmp,arrowhead="vee")

            fa.attr('node', shape = 'point')
            fa.edge('', '{'+','.join([chr(x+64) for x in self.allstates[self.startState]])+'}')

            fa.attr('node', shape = 'circle')
            fa.node('{'+','.join([chr(x+64) for x in self.allstates[self.startState]])+'}',color="green")

            fa.render("static/"+"eclosure"+fname,view=False, cleanup=True)
