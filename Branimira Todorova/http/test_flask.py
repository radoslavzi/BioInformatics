from flask import Flask, session, redirect, url_for, make_response
import os, requests

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', "secret-key")

@app.route('/')
def hello():
    return "Hello"

@app.route('/hello')
def hello_test():
    return "Hello test"

@app.route('/<name>')
def hello_name(name):
    return 'Hello ' + str(name)

@app.route('/color/<any(blue, white, red):color>')
def three_colors(color):
    return '<p> Test color :' + str(color) +  '</p>'

@app.route('/login')
def login():
    session['logged_in'] = True
    session['test_prop'] = { "name" : 1}
    return redirect(url_for('hello_test')) 

@app.route('/v1/sequence/gene/id/<id>')
def sequence(id):
    server = "https://rest.ensembl.org"
    ext = "/family/id/PTHR15573?"
    
    r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
    
    
    decoded = r.json()
    return repr(decoded)


if __name__ == '__main__':
	app.run(host='localhost', port=5000, debug=False)    