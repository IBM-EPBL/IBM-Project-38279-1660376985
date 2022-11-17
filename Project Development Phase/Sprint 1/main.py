from flask import Flask, render_template, request,redirect,session, url_for
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import mysql.connector
import os
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key=os.urandom(24)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'test'


mail_settings = {
 "MAIL_SERVER": 'smtp.gmail.com',
 "MAIL_PORT": 465,
 "MAIL_USE_TLS": False,
 "MAIL_USE_SSL": True,
 "MAIL_USERNAME": 'xxxxxxxxxxxxxxxxx',
 "MAIL_PASSWORD": 'xxxxxxxxxxxxxxxxx'
}

app.config.update(mail_settings)
mysql = MySQL(app)
mail = Mail(app)

s = URLSafeTimedSerializer('Thisisasecret!')

@app.route('/')
def login():
 return render_template('login.html')

@app.route('/register/')
def about():
 return render_template('register.html')

@app.route('/home')
def home():
 if 'email' in session:
 return render_template('home.html')
 else:
 return redirect('/')

@app.route('/login_validation',methods=['POST'])
def login_validation():
 email=request.form.get('email')
 password=request.form.get('password')
 if mysql:
 print("Connection Successful!")
 cursor = mysql.connection.cursor()
 cursor.execute(
 """SELECT * FROM `user_details` where `email` LIKE '{}' and `password` LIKE '{}'""".format(email, password))
 users = cursor.fetchall()
 cursor.close()
 else:
 print("Connection Failed!")

 if len(users)>0:
 session['email'] = users[0][1]
 return redirect('/home')
 else:
 return redirect('/')
 return "Vetri Nitchayam"

@app.route('/add_user',methods=['POST'])
def add_user():
 username=request.form.get('username')
 email = request.form.get('email')
 password = request.form.get('password')
 occupation = request.form.get('occupation')
 phone = request.form.get('phone')
 if mysql:
 print("Connection Successful!")
 cursor = mysql.connection.cursor()
 cursor.execute(
 """INSERT INTO `user_details` (`username`,`email`,`phone`,`occupation`,`password`) VALUES ('{}','{}','{}','{}','{}')""".format(username,email, phone,occupation,password))

 email = request.form['email']
 token = s.dumps(email, salt='email-confirm')

 msg = Message('Confirm Email', sender='db0096299ef646', recipients=[email])

 link = url_for('confirm_email', token=token, _external=True)

 msg.body = 'Your link is {}'.format(link)
 print(email)
 mail.send(msg)

 mysql.connection.commit()
 cursor.close()
 else:
 print("Connection Failed!")
 return "User Registered Successfully. Kindly Confirm the Mail sent to the provided Mail ID"

@app.route('/confirm_email/<token>')
def confirm_email(token):
 try:
 email = s.loads(token, salt='email-confirm', max_age=3600)
 except SignatureExpired:
 return '<h1>The token is expired!</h1>'
 return '<h1>The token works!</h1>'

@app.route('/logout')
def logout():
 session.pop('email')
 return redirect('/')

if __name__=="__main__":
 app.run(debug=True)
