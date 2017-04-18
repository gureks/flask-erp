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

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if 'username' in session:
		return redirect('/dashboard')
	if request.method == "GET":
		if 'alerts' in session:
			alert = session['alerts']
		else:
			alert = None
		return render_template("signup.html", alert=alert)
	elif request.method == "POST":
		username = request.form.get('username')
		password = request.form.get('password')
		name = request.form.get('name')
		sex = request.form.get('sex')
		dob = "2017-04-18"
		address = request.form.get('address')
		email = request.form.get('email')
		number = request.form.get('number')
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM user where username ='" + username + "'")
		data = cursor.fetchone()
		if data is not None:
			msg = "username already exists <br />"
		flag = 0
		flag = cursor.execute("INSERT INTO user VALUES('"+username+"','"+password+"','user')")
		flag = cursor.execute("INSERT INTO profile VALUES('"+username+"','"+name+"','"+dob+"','"+sex+"','"+email+"','"+address+"','"+number+"')")
		conn.commit()
		if flag == 0:
			msg = "wrong inputs, try again. <br />"
		else: 
			msg = "you were successful, please login from index."
		session['alerts'] = msg
		return redirect("/signup")

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
		print(session['username'],session['type'])
		return redirect('/dashboard')

@app.route('/admin/users')
def users():
	if 'username' not in session:
		return redirect('/')
	cursor = mysql.connect().cursor()
	cursor.execute("SELECT type FROM user where username='" + session['username'] + "'")
	data = cursor.fetchone()
	if "admin" not in data:
		return "you don't have access to this cause you're not an admin."
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("SELECT username FROM user WHERE EXISTS(SELECT * FROM user WHERE type = \"admin\")")
	data = cursor.fetchall()
	return render_template("users.html",data=data)

@app.route('/logout')
def logout():
	if 'username' not in session:
		return redirect('/')
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
	if 'alerts' in session:
		alert = session['alerts']
		session.pop('alerts')
	else:
		alert = None
	return render_template('settings.html', data=data, alert=alert)

@app.route('/dashboard')
def dashboard():
	if 'username' not in session:
		return redirect('/')
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("SELECT username FROM user WHERE NOT EXISTS (SELECT * FROM profile WHERE user.username = profile.username)")
	data = cursor.fetchone()
	if data is not None:
		if session['username'] in data:
			cursor.execute("DELETE FROM user WHERE username = '"+session['username']+"'")
			conn.commit()
			session.pop('username')
			session.pop('type')
			return "Your details are not filled. Please sign up again <a href=\"/signup\">here</a>. Account has been suspended."
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
	conn = mysql.connect()
	cursor = conn.cursor()
	msg = " "
	if username is not "" and username is not None:
		if username == session['username']:
			msg = msg + "<br /> Same Username "
		else:
			cursor.execute("SELECT username FROM user WHERE username = \"" + username + "\"")
			data = cursor.fetchone()
			if data is None:
				msg = msg + "<br /> Username Available"
				cursor.execute("UPDATE user SET username = \"" + username + "\" WHERE username = \"" + session['username'] + "\"" )
				cursor.execute("UPDATE profile SET username = \"" + username + "\" WHERE username = \"" + session['username'] + "\"" )
				conn.commit()
				session['username'] = username
				msg = msg + "<br />username changed to " + username
			else:
				msg = msg + "<br />username already exists"
	else:
		msg = msg + "<br /> username is none"
	if password is not "" and password is not None:
		cursor.execute("SELECT password FROM user WHERE username = \"" + username + "\"")
		data = cursor.fetchone()
		if password == data:
			msg = msg + "<br /> Same Password."
		else:
			cursor.execute("UPDATE user SET password = \"" + password + "\" WHERE username = \"" + session['username'] + "\"" )
			conn.commit()
	msg = msg + "<br /> Password changed."
	if newAdmin is not "" and newAdmin is not None:
		cursor.execute("SELECT type FROM user WHERE username = \"" + str(newAdmin) + "\"")
		data = cursor.fetchone()
		if data[0] == "admin":
			msg = msg + "<br /> Already admin "
		else:
			cursor.execute("UPDATE user SET type = \"admin\" WHERE username = \"" + str(newAdmin) + "\"" )
			conn.commit()
			msg = msg + "<br />" + newAdmin + " is now admin "
	session['alerts'] = msg		
	return redirect("/settings")

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=8000,debug=True)