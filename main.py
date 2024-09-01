# Store this code in 'app.py' file

from flask import Flask, render_template, request, redirect, url_for,session
import psycopg2
from datetime import date
import re
import os
import base64
from werkzeug.utils import secure_filename

def get_base64_encoded_image(image_path):
	with open(image_path, "rb") as img_file:
		return base64.b64encode(img_file.read()).decode('utf-8')


app = Flask(__name__)
upload_folder = os.path.join('static', 'uploads')
app.config['UPLOAD'] = upload_folder
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'


def create_connection():
    # Connect to the database
    # using the psycopg2 adapter.
    # Pass your database name ,# username , password ,
    # hostname and port number
    conn = psycopg2.connect(dbname='FPS',
                            user='postgres',
                            password='changeme',
                            host='localhost',
                            port='5432')
    # Get the cursor object from the connection object
    curr = conn.cursor()
    return conn, curr	

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		print("cbjs")
		username = request.form['username']
		password = request.form['password']
		conn, cursor = create_connection()
		print("aaaaaa")
		print(username, password)
		query = "SELECT * FROM users WHERE name = '"+username+"' AND password = '"+password+"';"
		cursor.execute(query)
		account = cursor.fetchone()
		if account:
			#msg = 'Logged in successfully !'
			return render_template('aadhar.html', msg = msg)
		else:
			msg = 'Incorrect username / password !'
		conn.close()
	return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
	#session.pop('loggedin', None)
	#session.pop('id', None)
	#session.pop('username', None)
	#return redirect(url_for('login'))
        #return render_template('login.html', msg = msg)
        return render_template('login.html')

@app.route('/check', methods =['GET', 'POST'])
def check():
	if request.method == 'POST':
		aadhar = request.form['aadhar']
		session["aadhar"]=aadhar
		file = request.files['img']
		conn, cursor = create_connection()
		print(aadhar)
		query = "SELECT * FROM fps_t1 WHERE  aadhar_no= '"+aadhar+"';"
		cursor.execute(query)	
		check = cursor.fetchone()  
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD'], filename))
		img = os.path.join(app.config['UPLOAD'], filename)
		if check:
			msg = 'AADHAR MATCHED'
			print(check[1],check[0])
			if (check[4]==get_base64_encoded_image(img)):
				fp='fingerprint matched with given aadhar no'
				if (check[1]>18):
					"""a='age is aplicable'
					date_check="SELECT * FROM fps_t1 WHERE  aadhar_no= '"+aadhar+"' AND last_buy=current_date ;" 
					cursor.execute(date_check)    
					date = cursor.fetchone()             
					if date:
						b='not eligible to purchase on this date'
					else:
						b='eligible to buy alchol today'
						updat_date="UPDATE fps_t1 SET last_buy= current_date WHERE aadhar_no ='"+aadhar+"';"
						cursor.execute(updat_date)  
						conn.commit()
					return render_template('check.html', msg = msg,name ='name='+check[0],age ='age='+str(check[1]),aadharno ='aadharno='+str(check[2]),fp=fp,a=a,b=b)"""
					return render_template('match.html',name ='NAME     :'+check[0],age ='AGE      :'+str(check[1]),aadharno ='AADHAR NO:'+str(check[2]))
				else:
					return render_template('match2.html',name ='name='+check[0],age ='age='+str(check[1]),aadharno ='aadharno='+str(check[2]),fp=fp)
			else:
				fp='fingerprint is not matched with given aadhar no'
				return render_template('aadhar.html',fp=fp)
		else:
			msg = 'there is no such aadhar number'
			return render_template('aadhar.html',msg=msg)
		conn.close()		
        
	return render_template('login.html')

@app.route('/check_limit', methods =['GET', 'POST'])
def check_limit():
	if request.method == 'POST':
		aadhar =session.get("aadhar",None)
		conn, cursor = create_connection()
		query = "SELECT * FROM fps_t1 WHERE  aadhar_no= '"+aadhar+"';"
		cursor.execute(query)
		check = cursor.fetchone()  
		print(check[0])
		date_check="SELECT * FROM fps_t1 WHERE  aadhar_no= '"+aadhar+"' AND last_buy=current_date ;" 
		cursor.execute(date_check)    
		date = cursor.fetchone()  
		if date:
			return render_template('check_limit2.html',name =check[0],last_buy=check[5])
		else:
			return render_template('check_limit.html',name =check[0],last_buy=check[5]),aadhar
		
@app.route('/update', methods =['GET', 'POST'])
def update():
	if request.method == 'POST':
		aadhar=session.get("aadhar",None)
		conn, cursor = create_connection()
		updat_date="UPDATE fps_t1 SET last_buy= current_date WHERE aadhar_no ='"+aadhar+"';"
		cursor.execute(updat_date)  
		conn.commit()
		return render_template('aadhar.html')

@app.route('/go_aadhar', methods =['GET', 'POST'])
def go_aadhar():
	return render_template('aadhar.html')


if __name__ =="__main__":
    app.run()
				