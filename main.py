from flask import Flask, render_template

app = Flask(__name__)

# ------------
# index
# ------------
@app.route('/')
def index():
	return render_template('index.html')


# debug=True to avoid restart the local development server manually after each change to your code. 
# host='0.0.0.0' to make the server publicly available. 
if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0',port='5003')
