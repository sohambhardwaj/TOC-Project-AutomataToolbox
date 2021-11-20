import json
from typing import OrderedDict
import pandas as pd
from IPython.display import HTML

def make_dfa(n,t,nfa,nfa_final_state,nfa_start):

    new_states_list = []   #holds all the new states created in dfa
    dfa = {}  #dfa dictionary/table or the output structure we needed
    keys_list = nfa_start         #conatins all the states in nfa plus the states created in dfa are also appended further
    path_list = list(nfa[keys_list[0]].keys())    #list of all the paths eg: [a,b] or [0,1]
    ###################################################

    # Computing first row of DFA transition table

    dfa[keys_list[0]] = {}                               #creating a nested dictionary in dfa 
    for y in range(t):
        var = "".join(nfa[keys_list[0]][path_list[y]])   #creating a single string from all the elements of the list which is a new state
        var = ''.join(sorted(var))
        dfa[keys_list[0]][path_list[y]] = var            #assigning the state in DFA table
        if var not in keys_list:                         #if the state is newly created 
            new_states_list.append(var)                  #then append it to the new_states_list
            keys_list.append(var)                        #as well as to the keys_list which contains all the states
            
    ###################################################
    
    # Computing the other rows of DFA transition table
    while len(new_states_list) != 0:                     #consition is true only if the new_states_list is not empty
        dfa[new_states_list[0]] = {}                     #taking the first element of the new_states_list and examining it
        for i in range(len(path_list)):
            temp = []                                #creating a temporary list
            for j in range(len(new_states_list[0])): # travel all the states for every variable present in the state
                temp += nfa[new_states_list[0][j]][path_list[i]]  #UNION of the states
            temp=list(OrderedDict.fromkeys(temp)) #Remove Duplicates present after doing union eg. ABB -> AB
            temp.sort()
            s = ""
            s = s.join(temp)                         #creating a single string(new state) from all the elements of the list
            if s not in keys_list:                   #if the state is newly created
                new_states_list.append(s)            #then append it to the new_states_list
                keys_list.append(s)                  #as well as to the keys_list which contains all the states
            dfa[new_states_list[0]][path_list[i]] = s   #assigning the new state in the DFA table
            
        new_states_list.remove(new_states_list[0])       #Removing the first element in the new_states_list

    dfa_table = pd.DataFrame(dfa)
    dfa_table=dfa_table.transpose()
    dfa_table.replace('','ϕ',inplace=True)
    html=dfa_table.to_html(classes='table table-bordered table-hover table-condensed table-striped')
    print(html)

    dfa_states_list = list(dfa.keys())
    dfa_final_states = []
    for x in dfa_states_list:
        for i in x:
            if i in nfa_final_state:
                dfa_final_states.append(x)
                break

    dfa_out={
        "states": list(dfa_table.index),
        "terminals": path_list,
        "transition": dfa,
        "finalStates":dfa_final_states
    }
    outfile=open("out_Dfa/dfa.json","w")
    json.dump(dfa_out,outfile, indent=4)
    outfile.close()
    table=open("static/dfa_table.html","w")
    table.write(html)
    table.close()
