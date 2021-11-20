from collections import defaultdict

transitions=defaultdict(defaultdict)
transitions[2][3]='a'
transitions[4][5]='b'
for fromstate, tostates in transitions.items():
    for state in tostates:
        print(tostates[state])