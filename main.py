import json

from flask import Flask,redirect, render_template, request, url_for

from create_NFA import create_nfa
from nfa_dfa import make_dfa
from NFAtoDFA import NFA2DFA
from plot_dfa import plotdfa
from plot_nfa import plotnfa
from regexToNFA import Regex_to_NFA


app=Flask(__name__)
app.config['SECRET_KEY']='d4ba78ce80527a1f2685d491f85ea57e'

@app.route("/regex2dfa",methods=['GET','POST'])
def regex2dfa():
    if request.method=='POST':
        regex=request.form.get("regex")
        a = Regex_to_NFA(regex)
        a.plotNFA()
        b = NFA2DFA(a.nfa)
        b.plotDFA()
        return redirect(url_for('Display_regex_dfa'))
    return render_template("home.html")

@app.route("/",methods=['GET','POST'])
@app.route("/home",methods=['GET','POST'])
def home():
    if request.method == 'POST':
        f = request.files['file']
        if f.filename == '':
            allStates=request.form.get("allStates")
            ss=request.form.get("ss")
            es=request.form.get("es")
            fullname = request.form.getlist('field[]')
            tp=request.form.get("path")
            create_nfa(fullname,allStates,ss,es,tp)
            return redirect(url_for('displayDFA')) 
        else :
            f.filename='nfa.json'
            f.save('uploads/'+ f.filename)
            return redirect(url_for('displayDFA')) 
    return render_template('NFA2DFA.html')



@app.route("/DFA", methods=['GET','POST'])
def displayDFA():
    process() # makes dfa from uploads/nfa.json and stores the output dfa json in out_Dfa/dfa.json
    f=open("out_Dfa/dfa.json")
    data=json.load(f)
    plotdfa(data)
    f_in=open("uploads/nfa.json")
    data_in=json.load(f_in)
    plotnfa(data_in)
    return render_template('displayDFA.html')

@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/displayreg2dfa")
def Display_regex_dfa():
    return render_template('displayreg2dfa.html')

def process():
    f = open('uploads/nfa.json')
    NFA_dict = json.load(f)
    n=len(NFA_dict["states"])
    t=len(NFA_dict["terminals"])
    nfa = NFA_dict['transition']
    nfa_start=list(NFA_dict["startState"])
    nfa_final_state=NFA_dict['finalStates']
    make_dfa(n,t,nfa,nfa_final_state,nfa_start)

if __name__ == '__main__':
    app.run(port=8000,debug=True)
