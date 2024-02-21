import json
from flask import Flask, render_template, request, redirect, url_for, jsonify


app = Flask(__name__)
# import json data
with open('data/playlist.json', 'r', encoding='utf-8') as f:
    playlist_data = json.load(f)

with open('data/channel.json', 'r', encoding='utf-8') as file:
    channel_data = json.load(file)

with open('data/video.json', 'r', encoding='utf-8') as file:
    videos = json.load(file)

# ------------
# index
# ------------

# splash page
@app.route('/')
def index():
    return render_template('splash.html')

# about page
@app.route('/about')
def about():
    return render_template('about.html')

# channels page display multiple channels
@app.route('/channels')
def showChannels():
    channels_info = channel_data['items']
    return render_template('channels.html', channels=channels_info)

# channel page display detail channel info
@app.route('/channel/<string:channelId>')
def showChannel(channelId):
    # Directly use channel_data['items'] if channels is not defined elsewhere
    channel_info = next(
        (channel for channel in channel_data['items'] if channel['id'] == channelId), None)
    if channel_info is None:
        return "Channel not found", 404
    return render_template('channel.html', channel=channel_info)

# videos page display multiple videos
@app.route('/videos')
def showVideos():
    return render_template('videos.html', videos=videos["items"])

# video page display single video
@app.route('/video/<string:videoId>')
def playVideo(videoId):
    video_info = None
    video_list = videos["items"]
    for video in video_list:
        if video['id'] == videoId:
            video_info = video
            break
    return render_template('video.html', video=video_info, videoId=videoId)


# playlists page display mutiple videos
@app.route('/playlists')
def showPlaylist():
    return render_template('playlists.html', playlists=playlist_data['items'])

# playlists page display single playlist
@app.route('/playlist/<string:playlistId>')
def playList(playlistId):
    playlist_info = None
    playlist_list = playlist_data["items"]
    for playlist in playlist_list:
        if playlist['id'] == playlistId:
            playlist_info = playlist
            break
    return render_template('playlist.html', playlist=playlist_info, playlistId=playlistId)


# debug=True to avoid restart the local development server manually after each change to your code.
# host='0.0.0.0' to make the server publicly available.
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
