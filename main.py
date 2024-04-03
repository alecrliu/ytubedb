"""Routing with queries for each page"""


import json
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_cors import CORS
import math
from database import app, db, Channel, Playlist, Video
from gitlabStats import commit_counts, issue_counts

CORS(app)

# splash page


@app.route('/')
def index():
    return render_template('splash.html')

# about page


@app.route('/about')
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


@app.route('/api/about', methods=['GET'])
def aboutAPI():
    response = {
        'nirmalCommits': commit_counts["Nirmal"],
        'nirmalIssues': issue_counts["Nirmal"],
        'adrianCommits': commit_counts["Adrian"],
        'adrianIssues': issue_counts["Adrian"],
        'alecCommits': commit_counts["Alec"],
        'alecIssues': issue_counts["Alec"],
        'junyuCommits': commit_counts["Junyu"],
        'junyuIssues': issue_counts["Junyu"],
        'totalCommits': sum(commit_counts.values()),
        'totalIssues': sum(issue_counts.values())
    }
    return jsonify(response)

# channels page displays multiple channels


@app.route('/channels/<int:page_num>')
def showChannels(page_num):
    channels_info = Channel.query.paginate(
        per_page=12, page=page_num, error_out=True)
    return render_template('channels.html', channels=channels_info, current_page=page_num)


@app.route('/api/channels/<int:page_num>', methods=['GET'])
def showChannelsAPI(page_num):
    per_page = 12
    total_channels = Channel.query.count()
    total_pages = math.ceil(total_channels / per_page)
    channels_info = Channel.query.paginate(
        per_page=12, page=page_num, error_out=True)
    channels = [channel.to_dict() for channel in channels_info.items]
    return jsonify(current_page=page_num, total_pages=total_pages, channels=channels)

# channel page displays single channel


@app.route('/channel/<string:channelId>')
def showChannel(channelId):
    channel_info = Channel.query.filter_by(channel_id=channelId).first()
    if channel_info is None:
        return "Channel not found", 404
    videos = Video.query.filter_by(channel_id=channelId).all()
    playlists = Playlist.query.filter_by(channel_id=channelId).all()
    return render_template('channel.html', channel=channel_info, videos=videos, playlists=playlists)


@app.route('/api/channel/<string:channelId>', methods=['GET'])
def showChannelAPI(channelId):
    channel_info = Channel.query.filter_by(channel_id=channelId).first()
    if channel_info is None:
        return jsonify({'error': 'Channel not found'}), 404
    videos = [video.to_dict()
              for video in Video.query.filter_by(channel_id=channelId).all()]
    playlists = [playlist.to_dict() for playlist in Playlist.query.filter_by(
        channel_id=channelId).all()]
    return jsonify(channel=channel_info.to_dict(), videos=videos, playlists=playlists)

# videos page displays multiple videos


@app.route('/videos/<int:page_num>')
def showVideos(page_num):
    per_page = request.args.get('per_page', type=int, default=12)
    videos_info = Video.query.paginate(
        per_page=per_page, page=page_num, error_out=True)
    return render_template('videos.html', videos=videos_info, current_page=page_num, per_page=per_page)


@app.route('/api/videos/<int:page_num>', methods=['GET'])
def showVideosAPI(page_num):
    per_page = request.args.get('per_page', type=int, default=12)
    total_videos = Video.query.count()
    total_pages = math.ceil(total_videos / per_page)
    videos_info = Video.query.paginate(
        per_page=per_page, page=page_num, error_out=True)
    videos_info = [video.to_dict() for video in videos_info.items]
    return jsonify(current_page=page_num, total_pages=total_pages, videos=videos_info)

# video page displays single video


@app.route('/video/<string:videoId>')
def oneVideo(videoId):
    video = Video.query.filter_by(video_id=videoId).first()
    channel = None
    playlists = []
    if video is not None:
        channel = video.channels
        playlists = video.inPlaylist
    else:
        return "Video not found", 404
    return render_template('video.html', video=video, channel=channel, playlists=playlists)


@app.route('/api/video/<string:videoId>', methods=['GET'])
def oneVideoAPI(videoId):
    video = Video.query.filter_by(video_id=videoId).first()
    if video is None:
        return jsonify({'error': 'Video not found'}), 404
    channel_dict = video.channels.to_dict() if video.channels else None
    playlists_dict = [playlist.to_dict()
                      for playlist in video.inPlaylist] if video.inPlaylist else []
    video_dict = video.to_dict()
    return jsonify(video=video_dict, channel=channel_dict, playlists=playlists_dict)


# playlists page displays multiple playlists

@app.route('/playlists/<int:page_num>')
def showPlaylist(page_num):
    playlists_info = Playlist.query.paginate(
        per_page=12, page=page_num, error_out=True)
    return render_template('playlists.html', playlists=playlists_info, current_page=page_num)


@app.route('/api/playlists/<int:page_num>', methods=['GET'])
def showPlaylistAPI(page_num):
    per_page = 12
    total_playlists = Playlist.query.count()
    total_pages = math.ceil(total_playlists / per_page)
    playlists_info = Playlist.query.paginate(
        per_page=12, page=page_num, error_out=True)
    playlists_info = [playlists.to_dict()
                      for playlists in playlists_info.items]
    return jsonify(current_page=page_num, total_pages=total_pages, playlists=playlists_info)


# playlist page displays single playlist

@app.route('/playlist/<string:playlistId>')
def playlist(playlistId):
    playlist_info = Playlist.query.filter_by(playlist_id=playlistId).first()
    if playlist_info is None:
        return "Playlist not found", 404
    channel = playlist_info.channels
    videos = playlist_info.videos
    return render_template('playlist.html', playlist=playlist_info, channel=channel, videos=videos)


@app.route('/api/playlist/<string:playlistId>', methods=['GET'])
def playlistAPI(playlistId):
    playlist_info = Playlist.query.filter_by(playlist_id=playlistId).first()
    if playlist_info is None:
        return jsonify({'error': 'Playlist not found'}), 404
    channel_dict = playlist_info.channels.to_dict() if playlist_info.channels else None
    videos_dict = [video.to_dict()
                   for video in playlist_info.videos] if playlist_info.videos else []
    playlist_dict = playlist_info.to_dict()
    return jsonify(playlist=playlist_dict, channel=channel_dict, videos=videos_dict)


# debug=True to avoid restart the local development server manually after each change to your code.
# host='0.0.0.0' to make the server publicly available.
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
