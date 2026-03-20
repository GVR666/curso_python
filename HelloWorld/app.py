from flask import Flask

app = Flask(_name_)

@app.route('/') # Home or root of site
def index():
    return '<html><head><title>HELLO WORLD</title></head><body><h1>Hello world</h1><p>Ir a <a href="/about">About</a></p></body></html>'

@app.route('/about') 
def about():
    return '<html><head><title>HELLO WORLD</title>About this page</title></head><body> Everything about this website. Back to <a href="/">Hello world</a></body></html>'

if _name_ == '_main_':
    app.run(debug=True)