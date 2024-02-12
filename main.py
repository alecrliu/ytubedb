from flask import Flask, render_template, request, redirect, url_for, jsonify


app = Flask(__name__)
# import json
import json
# 
with open('data/playlist.json') as f:
    playlist_data = json.load(f)

with open('data/channel.json') as file:
    channel_data = json.load(file)

# ------------
# index
# ------------

videos = [{'title': 'Software Engineering', 'id': '1'},
          {'title': 'Algorithm Design', 'id': '2'},
          {'title': 'Python', 'id': '3'}]


@app.route('/')
def index():
    return render_template('splash.html')

@app.route('/About')
def about():
    return render_template('about.html')

@app.route('/videos')
def showVideos():
    return render_template('videos.html', videos=videos)

@app.route('/Playlist')
def showPlaylist():
    return render_template('playlist.html', playlists=playlist_data['items'])

@app.route('/Channels')
def showChannels():
    channels_info = channel_data['items']  
    return render_template('channel.html', channels=channels_info)

# debug=True to avoid restart the local development server manually after each change to your code.
# host='0.0.0.0' to make the server publicly available.
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
