from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flaskext.mysql import MySQL
from image_links import *
import random

app = Flask(__name__)
app.config['MYSQL_DATABASE_HOST'] = 'sql12.freemysqlhosting.net'
app.config['MYSQL_DATABASE_USER'] = 'sql12243879'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Cr49XjeJ2y'
app.config['MYSQL_DATABASE_DB'] = 'sql12243879'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

mysql = MySQL()
mysql.init_app(app)
connection = mysql.connect()

@app.route('/')
def hello():
    return render_template("index.html",image=useful_links[random.randint(1,8)])

@app.route('/read_quotes')
def read_quotes():
	cursor = connection.cursor()
	cursor.execute('''SELECT * FROM Quotes''')
	result = cursor.fetchall()
	return render_template("display_quotes.html",dis=result)

@app.route('/quotes',methods=['GET','POST'])
def quotes():
	cursor = connection.cursor()
	cursor.execute('''SELECT * FROM Quotes''')
	result = cursor.fetchall()
	if request.method=='GET':
		return render_template("quotes.html",dis=result)
	else:
		name=request.form['name']
		quote=request.form['quote']
		cursor = connection.cursor()
		cursor.execute('''SELECT MAX(id) FROM Quotes''')
		maxId=cursor.fetchone()
		cursor.execute('''INSERT INTO Quotes(id,name,quote) VALUES(%s,%s,%s)''',(maxId[0]+1,name,quote))
		connection.commit()
		return redirect(url_for('quotes'))


@app.route('/login',methods=['GET','POST'])
def login():
	if request.method=='GET':
		return render_template("login.html",image=useful_links[random.randint(1,8)])
	else:
		username=request.form['username']
		password=request.form['password']
		cursor = connection.cursor()
		cursor.execute('''SELECT pwd FROM credentials WHERE email=%s''',(username))
		pwd = cursor.fetchone()
		cursor.execute('''SELECT firstName FROM credentials WHERE email=%s''',(username))
		firstName=cursor.fetchone()
		cursor.execute('''SELECT lastName FROM credentials WHERE email=%s''',(username))
		lastName=cursor.fetchone()
		if(pwd[0]==password):
			return render_template("quotes.html",first=firstName[0],last=lastName[0])
		else:
			return render_template("wrongPass.html",sel="login")

@app.route('/register',methods=['GET','POST'])
def register():
	if request.method=='GET':
		return render_template("register.html",image=useful_links[random.randint(1,8)])
	else:
		firstName=request.form['firstName']
		lastName=request.form['lastName']
		username=request.form['username']
		password=request.form['password']
		cnfPassword=request.form['cnfPassword']
		if(password != cnfPassword):
			return render_template("wrongPass.html",sel="register")
		else: 
			cursor = connection.cursor()
			cursor.execute('''INSERT INTO credentials(firstName,lastname,email,pwd) VALUES(%s,%s,%s,%s)''',(firstName,lastName,username,password))
			connection.commit()
			return render_template("registered.html",firstName=firstName,lastName=lastName,username=username,password=password)

@app.route('/contact')
def contact():
	return render_template("contact.html",image=useful_links[random.randint(1,8)])

if __name__ == '__main__':
    app.run(host='localhost',port=5000,debug=True)
