from flask import Flask, render_template,request
import spellcheck as sp
app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def hello_world():
    s = {}
    if request.method == 'POST':
        sentence=request.form["content"]
        s["corrections"], s["suggestions"] = sp.check(sentence)
        s["sentence"] = sentence
    return render_template("main.html", s=s)
