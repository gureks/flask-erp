from flask import Flask, render_template
import os

app = Flask('__name__')
app.config['SECRET_KEY']=os.urandom(20)

@app.route('/')
def index():
	return '''Hi, Flask app is running.'''

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=80,debug=True)