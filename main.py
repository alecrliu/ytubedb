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
'''
with open('data/channels.json', 'r', encoding='utf-8') as file:
    channel_data = json.load(file)
'''
with open('data/videos.json', 'r', encoding='utf-8') as file:
    videos = json.load(file)


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


@app.route('/channels/<int:page_num>')  # channels page displays multiple channels
def showChannels(page_num):
    #channels_info = channel_data['items']
    channels_info = Channel.query.paginate(per_page=9, page=page_num, error_out=True)
    return render_template('channels.html', channels=channels_info)


# channel page displays detail channel info
'''
@app.route('/channel/<string:channelId>')
def showChannel(channelId):
    # Directly use channel_data['items'] if channels is not defined elsewhere
    channel_info = next(
        (channel for channel in channel_data['items'] if channel['id'] == channelId), None)
    if channel_info is None:
        return "Channel not found", 404
    return render_template('channel.html', channel=channel_info)
'''
@app.route('/channel/<string:channelId>')
def showChannel(channelId):
    channel_info = Channel.query.filter_by(channel_id=channelId).first()
    if channel_info is None:
        return "Channel not found", 404
    return render_template('channel.html', channel=channel_info)

    # Fetch videos and playlists associated with the channel from the database
    # Placeholder for actual database query
    #videos = Video.query.filter_by(channel_id=channelId).all()
    #playlists = Playlist.query.filter_by(channel_id=channelId).all()
    #return render_template('channel.html', channel=channel_info, videos=videos, playlists=playlists)


@app.route('/videos/<int:page_num>')  # videos page displays multiple videos
def showVideos(page_num):
    videos_info = Video.query.paginate(per_page=9, page=page_num, error_out=True)
    return render_template('videos.html', videos=videos_info)


@app.route('/video/<string:videoId>')  # video page displays single video
def oneVideo(videoId):
    video = None
    for vid in videos["items"]:
        if vid['id'] == videoId:
            video = vid
            break
    return render_template('video.html', video=video, videoId=videoId)


# playlists page display multiple videos
@app.route('/playlists/<int:page_num>')
def showPlaylist(page_num):
    playlists_info = Playlist.query.paginate(per_page=9, page=page_num, error_out=True)
    return render_template('playlists.html', playlists=playlists_info)


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
