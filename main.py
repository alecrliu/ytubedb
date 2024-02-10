from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# ------------
# index
# ------------

videos = [{'title': 'Software Engineering', 'id': '1'},
          {'title': 'Algorithm Design', 'id': '2'},
          {'title': 'Python', 'id': '3'}]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/videos')
def showVideos():
    return render_template('videos.html', videos=videos)


# debug=True to avoid restart the local development server manually after each change to your code.
# host='0.0.0.0' to make the server publicly available.
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
