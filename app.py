from flask import Flask, render_template, request, redirect, session
from flaskext.mysql import MySQL

import os

mysql = MySQL()
app = Flask('__name__')
app.config['SECRET_KEY']=os.urandom(20)
app.config['MYSQL_DATABASE_USER'] = 'dbms'
app.config['MYSQL_DATABASE_PASSWORD'] = 'justanothersecret'
app.config['MYSQL_DATABASE_DB'] = 'erp'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/')
def index():
	if 'username' in session:
		return redirect('/dashboard')
	return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
	if 'username' in session:
		return redirect('/dashboard')	
	username = request.form.get('username')
	password = request.form.get('password')
	cursor = mysql.connect().cursor()
	cursor.execute("SELECT * FROM user where username='" + username + "' and password='" + password + "'")
	data = cursor.fetchone()
	if data is None:
		return render_template('wrong-login.html')
	else:
		session['username'] = username
		session['type'] = data[2] 
		return redirect('/dashboard')

@app.route('/logout')
def logout():
	session.pop('username')
	session.pop('type') 
	return redirect('/')

@app.route('/dashboard')
def homepage():
	if 'username' not in session:
		return redirect('/')
	return render_template("dashboard.html")

@app.route('/help')
def help():
	return render_template("help.html")

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=8000,debug=True)