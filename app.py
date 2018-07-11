from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from image_links import *
import random
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	firstName = db.Column(db.String(50), nullable=False)
	lastName = db.Column(db.String(50), nullable=False)
	username = db.Column(db.String(20), unique=True, nullable=False)
	password = db.Column(db.String(20), nullable=False)

	def __repr__(self):
		return "User('{}','{}','{}','{}')".format(self.firstName, self.lastName, self.username, self.password)

class Quotes(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)
	content = db.Column(db.String(500), nullable=False)
	likes = db.Column(db.Integer)
	def __repr__(self):
		return "Quotes('{}','{}','{}')".format(self.name, self.content, self.likes)

@app.route('/')
def home():
	result = Quotes.query.all()
	return render_template("index.html", image=useful_links[random.randint(1,8)], dis=result)

@app.route('/login',methods=['GET','POST'])
def login():
	if request.method=='GET':
		return render_template("login.html",image=useful_links[random.randint(1,8)])
	else:
		username = request.form['username']
		password = request.form['password']
		user1 = User.query.filter_by(username=username).all()
		if(len(user1)==0): return render_template("wrongPass.html",sel="login")
		pwd = user1[0].password
		f_name = user1[0].firstName
		l_name = user1[0].lastName
		#return str(user1[0])
		if(pwd==password):
			return render_template("quotes.html",first=f_name,last=l_name)
		else:
			return render_template("wrongPass.html",sel="login")

@app.route('/register',methods=['GET','POST'])
def register():
	if request.method=='GET':
		return render_template("register.html",image=useful_links[random.randint(1,8)])
	else:
		firstName = request.form['firstName']
		lastName = request.form['lastName']
		username = request.form['username']
		password = request.form['password']
		cnfPassword = request.form['cnfPassword']
		if(password != cnfPassword):
			return render_template("wrongPass.html",sel="register")
		else: 
			newuser = User(firstName=firstName, lastName=lastName, username=username, password=password)
			db.session.add(newuser)
			db.session.commit()
			return render_template("registered.html",firstName=firstName,lastName=lastName,username=username,password=password)

@app.route('/quotes',methods=['GET','POST'])
def quotes():
	result = Quotes.query.all()
	if request.method=='GET':
		return render_template("quotes.html",dis=result)
	else:
		name = request.form['name']
		quote = request.form['quote']
		newpost = Quotes(name=name, content=quote, likes=0)
		db.session.add(newpost)
		db.session.commit()
		return redirect(url_for('quotes'))

@app.route('/read_quotes',methods=['GET','POST'])
def read_quotes():
	result = Quotes.query.all()
	return render_template("display_quotes.html",dis=result)


@app.route('/contact')
def contact():
	return render_template("contact.html",image=useful_links[random.randint(1,8)])

if __name__ == '__main__':
    app.run(host='localhost',port=5000,debug=True)
