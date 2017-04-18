from flask import Flask, render_template, request, redirect, session, abort
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

@app.route('/settings')
def settings():
	if 'username' not in session:
		return redirect('/')
	cursor = mysql.connect().cursor()
	cursor.execute("SELECT name, dob, sex, email, number, address FROM user, profile where user.username = \"" + session['username'] + "\" and user.username = profile.username")
	data = cursor.fetchone()
	if data is None:
		return abort(404)
	return render_template('settings.html', data=data)

@app.route('/dashboard')
def dashboard():
	if 'username' not in session:
		return redirect('/')
	cursor = mysql.connect().cursor()
	cursor.execute("SELECT name, dob, sex, email, number, address FROM user, profile where user.username = \"" + session['username'] + "\" and user.username = profile.username")
	data = cursor.fetchone()
	if data is None:
		return abort(404)
	return render_template("dashboard.html",data=data)

@app.route('/help')
def help():
	return render_template("help.html")

@app.route('/changesettings', methods=['GET','POST'])
def changesettings():
	if 'username' not in session:
		return redirect('/')
	username = request.form.get('username')
	password = request.form.get('password')
	newAdmin = request.form.get('newAdmin')
	msg = username + " " + password + " " + newAdmin + " " 
	if username is not None:
		if username == session['username']:
			msg = msg + "<br />same username "
		else:
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute("SELECT username FROM user WHERE username = \"" + username + "\"")
			data = cursor.fetchone()
			if data is None:
				msg = msg + "<br /> Username available"
				print("UPDATE user SET username = \"" + username + "\" WHERE username = \"" + session['username'] + "\"" )
				cursor.execute("UPDATE user SET username = \"" + username + "\" WHERE username = \"" + session['username'] + "\"" )
				cursor.execute("UPDATE profile SET username = \"" + username + "\" WHERE username = \"" + session['username'] + "\"" )
				data = cursor.fetchone()
				print(data)
				conn.commit()
				session['username'] = username
			else:
				msg = msg + "<br />username already exists"
	else:
		msg = msg + "<br /> username is none"
	return msg + "<br /> username now is " + session['username']	


if __name__ == '__main__':
	app.run(host='0.0.0.0',port=8000,debug=True)