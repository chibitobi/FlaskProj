from flask import Flask, render_template
app = Flask(__name__)


#app.route() decorator tells Flask what URL should trigger function
@app.route("/")
def main():
	return render_template('index.html')
#returns message we want to display in the user's browser

@app.route('/showSignUp')
def showSignup():
	return render_template('signup.html')

if __name__ == "__main__":
	app.run()
