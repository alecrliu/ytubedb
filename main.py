"""Routing with queries for each page"""


import json
from flask import Flask, render_template, request, redirect, url_for, session
from database import app, db, Channel, Playlist, Video
from gitlabStats import commit_counts, issue_counts


@app.route('/')  # splash page
def index():
    return render_template('splash.html')


@app.route('/about')  # about page
def about():
    return render_template(
        'about.html',
        nirmalCommits=commit_counts["Nirmal"],
        nirmalIssues=issue_counts["Nirmal"],
        adrianCommits=commit_counts["Adrian"],
        adrianIssues=issue_counts["Adrian"],
        alecCommits=commit_counts["Alec"],
        alecIssues=issue_counts["Alec"],
        junyuCommits=commit_counts["Junyu"],
        junyuIssues=issue_counts["Junyu"],
        totalCommits=sum(commit_counts.values()),
        totalIssues=sum(issue_counts.values())
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
    return render_template('channels.html', channels=channels_info, current_page=page_num)


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
    per_page = request.args.get('per_page', type=int, default=12)
    videos_info = Video.query.paginate(
        per_page=per_page, page=page_num, error_out=True)
    return render_template('videos.html', videos=videos_info, current_page=page_num, per_page=per_page)


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
    return render_template('playlists.html', playlists=playlists_info, current_page=page_num)


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