from Automata import *

class Regex_to_NFA:
    """

    Class for Converting Regular Expression to NFA. Construct NFA method is run first. 
    It adds . in between the characters of regex
    then produces postfix expression using Shunting yard algorithm.
    then uses Thompsons Method to calculate E-NFA of the regex.

    priority from highest to lowest: 1. Kleen Star (*)
                                     2. Concatenation (.)
                                     3. Addition (+)
    
    """

    def __init__(self, regex):
        self.regex = regex
        self.constructNFA()

    def constructNFA(self):
       #################################################################################################
        # Adding concat symbol explicitly
        symbol = set()
        final = ''
        prev = ''
        for char in self.regex: # traverse each character of regex
            if char in symbols:
                symbol.add(char) # if character then simply add to the  output
            if char in symbols or char == leftBracket:
                if prev != dot and (prev in symbols or prev in [star, rightBracket]):
                    final += dot  #add dot only if prev is not dot and (prev is symbol or ) or * )
            final += char
            prev = char
        self.regex = final


        #################################################################################################
        # Shunting Yard Algorithm
        final = ''
        stack = []
        for char in self.regex:
            if char in symbols: #if symbol add directly to the final regex
                final += char
            elif char == leftBracket: # if left bracket add directly to the operator stack
                stack.append(char)
            elif char == rightBracket:
                while(stack[-1] != leftBracket): # keep popping until you find leftbracket
                    final += stack[-1]
                    stack.pop()
                stack.pop()    # pop the left bracket also
            else:
                while(len(stack) and Regex_to_NFA.calcPriority(stack[-1]) >= Regex_to_NFA.calcPriority(char)): # keep popping until top of the stack has less priority than the char
                    final += stack[-1]
                    stack.pop()
                stack.append(char)
        while(len(stack) > 0): # for left over characters
            final += stack.pop()
        self.regex = final

        #################################################################################################
        # Thompsons' Algorithm
        self.automata = []
        for ch in self.regex:
            if ch in symbols:
                newNFA=Regex_to_NFA.symbolNFA(ch)
                # print(newNFA.states)
                # print(newNFA.symbol)
                self.automata.append(newNFA)
            elif ch == plus:
                b = self.automata.pop()
                a = self.automata.pop()
                newNFA=Regex_to_NFA.plusNFA(a, b)
                # print(newNFA.states)
                # print(newNFA.symbol)
                self.automata.append(newNFA)
            elif ch == dot:
                b = self.automata.pop()
                a = self.automata.pop()
                newNFA=Regex_to_NFA.dotNFA(a, b)
                self.automata.append(newNFA)
            elif ch == star:
                a = self.automata.pop()
                newNFA=Regex_to_NFA.starNFA(a)
                # print(newNFA.states)
                # print(newNFA.symbol)
                self.automata.append(newNFA)

        self.nfa = self.automata.pop() # last/top element of the automata stack is our final e-nfa
        self.nfa.symbol = symbol
        # print(self.nfa.startState)
        # print("SYMBOL ", symbol)

    def plotNFA(self):
        self.nfa.display('nfa.gv', 'nondeterministic_finite_state_machine')


    def calcPriority(char):
        if char == plus:
            return 1
        elif char == dot:
            return 2
        elif char == star:
            return 3
        else:       # left bracket 
            return 0

    
    def symbolNFA(inputch):   # Regex = a -> NFA
        state1 = 1
        state2 = 2
        basic = Automata(set(inputch))
        basic.setStart(state1)
        basic.addFinal(state2)
        basic.addTransition(state1, state2, inputch)
        return basic

    
    def plusNFA(a, b):   # Regex = a | b -> NFA
        [a, m1] = a.newBuildFromNumber(2)
        # print(a.states)
        [b, m2] = b.newBuildFromNumber(m1)
        # print(b.states)
        state1 = 1
        state2 = m2 #m2=6
        plusFA = Automata(a.symbol.union(b.symbol))
        plusFA.setStart(state1)
        plusFA.addFinal(state2)
        plusFA.addTransition(plusFA.startState, a.startState, epsilon)
        plusFA.addTransition(plusFA.startState, b.startState, epsilon)
        plusFA.addTransition(a.finalStates[0], plusFA.finalStates[0], epsilon)
        plusFA.addTransition(b.finalStates[0], plusFA.finalStates[0], epsilon)
        plusFA.addTransition_dict(a.transitions)## add transitions of smaller nfa to the bigger nfa
        plusFA.addTransition_dict(b.transitions)
        return plusFA

    
    def dotNFA(a, b):    # Regex = a · b -> NFA
        [a, m1] = a.newBuildFromNumber(1) #building from 1 because in dot initial state of a will be initial state of final
        [b, m2] = b.newBuildFromNumber(m1)
        state1 = 1
        state2 = m2 - 1 #subtracting 1 because final state of final will be same as final state of b.
        dotFA = Automata(a.symbol.union(b.symbol))
        dotFA.setStart(state1)
        dotFA.addFinal(state2)
        dotFA.addTransition(a.finalStates[0], b.startState, epsilon)
        dotFA.addTransition_dict(a.transitions)
        dotFA.addTransition_dict(b.transitions)
        return dotFA

    
    def starNFA(a):  # Regex = a* -> NFA
        [a, m1] = a.newBuildFromNumber(2)
        state1 = 1
        state2 = m1
        starFA = Automata(a.symbol)
        starFA.setStart(state1)
        starFA.addFinal(state2)
        starFA.addTransition(starFA.startState, a.startState, epsilon)
        starFA.addTransition(starFA.startState, starFA.finalStates[0], epsilon)
        starFA.addTransition(a.finalStates[0], starFA.finalStates[0], epsilon)
        starFA.addTransition(a.finalStates[0], a.startState, epsilon)
        starFA.addTransition_dict(a.transitions)
        return starFA
