"""Routing with queries for each page"""


import json


from flask import Flask, render_template, request, redirect, url_for, session
# # Uncomment when done with database.py
from database import app, db, Channel, Playlist, Video
from gitlabStats import root_url, gitlab_ids, getCommits, getIssues


# app = Flask(__name__)
# import json data (will remove and use database instead)
# TODO: Move all data modification to the database.py file
with open('data/playlists.json', 'r', encoding='utf-8') as file:
    playlist_data = json.load(file)


@app.route('/')  # splash page
def index():
    return render_template('splash.html')


@app.route('/about')  # about page
def about():
    curr_commits = getCommits(root_url, gitlab_ids)
    curr_issues = getIssues(root_url, gitlab_ids)
    return render_template(
        'about.html',
        nirmalCommits=curr_commits["Nirmal"],
        nirmalIssues=curr_issues["Nirmal"],
        adrianCommits=curr_commits["Adrian"],
        adrianIssues=curr_issues["Adrian"],
        alecCommits=curr_commits["Alec"],
        alecIssues=curr_issues["Alec"],
        junyuCommits=curr_commits["Junyu"],
        junyuIssues=curr_issues["Junyu"],
        totalCommits=sum(curr_commits.values()),
        totalIssues=sum(curr_issues.values())
    )


# channels page displays multiple channels
@app.route('/channels/<int:page_num>')
# channels page displays multiple channels
@app.route('/channels/<int:page_num>')
def showChannels(page_num):
    # channels_info = channel_data['items']
    channels_info = Channel.query.paginate(
        per_page=12, page=page_num, error_out=True)
    # channels_info = channel_data['items']
    channels_info = Channel.query.paginate(
        per_page=12, page=page_num, error_out=True)
    return render_template('channels.html', channels=channels_info)


# channel page displays detail channel info
@app.route('/channel/<string:channelId>')
def showChannel(channelId):
    channel_info = Channel.query.filter_by(channel_id=channelId).first()
    if channel_info is None:
        return "Channel not found", 404
    videos = Video.query.filter_by(channel_id=channelId).all()
    playlists = Playlist.query.filter_by(channel_id=channelId).all()
    return render_template('channel.html', channel=channel_info, videos=videos, playlists=playlists)


@app.route('/videos/<int:page_num>')  # videos page displays multiple videos
def showVideos(page_num):
    videos_info = Video.query.paginate(
        per_page=12, page=page_num, error_out=True)
    videos_info = Video.query.paginate(
        per_page=12, page=page_num, error_out=True)
    return render_template('videos.html', videos=videos_info)


@app.route('/video/<string:videoId>')  # video page displays single video
def oneVideo(videoId):
    video = Video.query.filter_by(video_id=videoId).first()
    channel = None
    playlists = []
    if video is not None:
        channel = video.channels
        playlists = video.inPlaylist
    return render_template('video.html', video=video, channel=channel, playlists=playlists)


# playlists page display multiple videos
@app.route('/playlists/<int:page_num>')
def showPlaylist(page_num):
    playlists_info = Playlist.query.paginate(
        per_page=12, page=page_num, error_out=True)
    return render_template('playlists.html', playlists=playlists_info)


# playlists page display single playlist
@app.route('/playlist/<string:playlistId>')
def playList(playlistId):
    playlist_info = Playlist.query.filter_by(playlist_id=playlistId).first()
    if playlist_info is None:
        return "Playlist not found", 404
    channel = playlist_info.channels
    videos = playlist_info.videos
    return render_template('playlist.html', playlist=playlist_info, channel=channel, videos=videos)


# debug=True to avoid restart the local development server manually after each change to your code.
# host='0.0.0.0' to make the server publicly available.
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
