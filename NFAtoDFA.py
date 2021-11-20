from Automata import Automata
class NFA2DFA:
    """
    Class for Converting NFA to DFA. build DFA method is run first. 
    
    
    """
    def __init__(self, nfa):
        self.buildDFA(nfa)

    def buildDFA(self, nfa):    # subset construction method
        allstates = dict()  # dictionary of the visited subsets
        eclosure = dict()   #  stores e-closure for every state. eg eclosure[1]={1,2,3,5,8}
        ec_state1 = nfa.getEpsilonClosure(nfa.startState) # eclosure of first state of nfa
        # print(ec_state1)
        eclosure[nfa.startState] = ec_state1
        cnt = 1 
        dfa = Automata(nfa.symbol)
        dfa.setStart(cnt)
        states = [[ec_state1, dfa.startState]] # visit all states in states untill no left
        allstates[cnt] = ec_state1
        cnt += 1
        while len(states):
            [state, fromindex] = states.pop() #state=EC_STATE-1
            for ch in dfa.symbol: # ch='a' 'b'
                trstates = nfa.reachableStates(state, ch) # gives set of all states reachable by state=prev epsilonclosure through ch
                # print(trstates) = {4}
                for s in list(trstates):   # Convert to list, which is equivalent to using a temporary variable
                    if s not in eclosure: # means new state so calc its closure
                        eclosure[s] = nfa.getEpsilonClosure(s)
                    trstates = trstates.union(eclosure[s]) 

                # trstates is the new state of the dfa through ch
                if len(trstates):
                    if trstates not in allstates.values(): # means new state is not present
                        states.append([trstates, cnt]) # append new state in dfa table for further states
                        allstates[cnt] = trstates
                        toindex = cnt
                        cnt += 1
                    else: # means new state is already present
                        toindex = [key for key, val in allstates.items() if val  ==  trstates][0]
                    dfa.addTransition(fromindex, toindex, ch)
            for value, state in allstates.items():
                if nfa.finalStates[0] in state:
                    dfa.addFinal(value)
        self.dfa = dfa
        self.dfa.allstates=allstates
        # print(self.allstates)

    def plotDFA(self):
        self.dfa.display('dfa.gv', 'nfa')