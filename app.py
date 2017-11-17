from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
app = Flask(__name__)
mysql = MySQL()

# MySQL config
app.config['MYSQL_DATABASE_USER'] = 'Jay'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Jay'
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

#app.route() decorator tells Flask what URL should trigger function
@app.route("/")
def main():
	return render_template('index.html')
#returns message we want to display in the user's browser

@app.route('/showSignup')
def showSignUp():
	return render_template('signup.html')

@app.route('/signUp',methods=['POST'])  #methods is used for setting HTTP method
				        #HTTP methods tells server what the client wants
					#to do with the requested page
						#GET = get the info stored on that page/store
						#HEAD = get the info but only interested in headers
						#POST = tells server that it wants to post new info to that URL
						#	typical way to transmit data to the server
						#PUT = similar to POST, but server might triger store multiple times
						#      overwriting in the process. Backup usage	
def signUp():
	try:
		_name = request.form['inputName'] #remember these "labels" from signup.html?
		_email = request.form['inputEmail']
		_password = request.form['inputPassword']
	
		#double checking / validating
		if _name and _email and _password:
			conn = mysql.connect()
			cursor = conn.cursor()
			_hashed_password = generate_password_hash(_password)
			cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
			data = cursor.fetchall() #this method fetches all (or all remaining) rows of a query result set

			if len(data) is 0:
				conn.commit()
				return json.dumps({'message': 'All fields good'})
			else:
				return json.dumps({'error': 'Enter the required fields'})
		else:
			return json.dumps({'html':'<span>meh</span>'})
	except Exception as e:
		return json.dumps({'err':str(e)})

if __name__ == "__main__":
	app.run(port=5002)
