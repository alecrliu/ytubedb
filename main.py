import json
from flask import Flask, render_template, request, redirect, url_for, jsonify


app = Flask(__name__)
# import json data
with open('data/playlist.json') as f:
    playlist_data = json.load(f)

with open('data/channel.json') as file:
    channel_data = json.load(file)

with open('data/video.json') as file:
    videos = json.load(file)

# ------------
# index
# ------------


@app.route('/')
def index():
    return render_template('splash.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/channels')
def showChannels():
    channels_info = channel_data['items']
    return render_template('channel.html', channels=channels_info)


@app.route('/videos')
def showVideos():
    return render_template('videos.html', videos=videos["items"])


@app.route('/playlists')
def showPlaylist():
    return render_template('playlist.html', playlists=playlist_data['items'])


# debug=True to avoid restart the local development server manually after each change to your code.
# host='0.0.0.0' to make the server publicly available.
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
