"""Routing with queries for each page"""


import json
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_cors import CORS
from sqlalchemy import func, or_, desc, asc
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
'''
@app.route('/channels/<int:page_num>')
def showChannels(page_num):
    channels_info = Channel.query.paginate(
        per_page=12, page=page_num, error_out=True)
    return render_template('channels.html', channels=channels_info, current_page=page_num)
'''
'''
@app.route('/channels/<int:page_num>')
def showChannels(page_num):
    sort_option = request.args.get('sort', 'default')  # Get the sort parameter from URL
    if sort_option == 'subscribers':
        channels_info = Channel.query.order_by(Channel.subscriberCount.desc()).paginate(per_page=12, page=page_num, error_out=True)
    elif sort_option == 'views':
        channels_info = Channel.query.order_by(Channel.viewCount.desc()).paginate(per_page=12, page=page_num, error_out=True)
    elif sort_option == 'videos':
        channels_info = Channel.query.order_by(Channel.videoCount.desc()).paginate(per_page=12, page=page_num, error_out=True)
    elif sort_option == 'name':
        channels_info = Channel.query.order_by(Channel.channelName).paginate(per_page=12, page=page_num, error_out=True)
    else:
        channels_info = Channel.query.paginate(per_page=12, page=page_num, error_out=True)
    return render_template('channels.html', channels=channels_info, current_page=page_num)
'''


@app.route('/channels/<int:page_num>')
def showChannels(page_num):
    sort_option = request.args.get(
        'sort', 'default')  # sort parameter from URL
    search_query = request.args.get('search', '')  # search parameter from URL
    query = Channel.query
    if search_query:
        search = f"%{search_query}%"
        query = query.filter(
            or_(
                Channel.channelName.ilike(search),
                Channel.description.ilike(search)
            )
        )
    if sort_option == 'subscribers':
        query = query.order_by(Channel.subscriberCount.desc())
    elif sort_option == 'views':
        query = query.order_by(Channel.viewCount.desc())
    elif sort_option == 'videos':
        query = query.order_by(Channel.videoCount.desc())
    elif sort_option == 'name':
        query = query.order_by(Channel.channelName)

    channels_info = query.paginate(per_page=12, page=page_num, error_out=True)

    return render_template('channels.html', channels=channels_info, current_page=page_num, search_query=search_query)


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
    sort_option = request.args.get('sort', 'default')
    order_option = request.args.get('order', 'desc')
    search_query = request.args.get('search', '')
    query = Video.query
    if search_query:
        search = f"%{search_query}%"
        query = query.filter(
            or_(
                Video.title.ilike(search),
                Video.description.ilike(search)
            )
        )
    if sort_option == 'title':
        query = query.order_by(
            desc(Video.title) if order_option == 'desc' else asc(Video.title))
    elif sort_option == 'views':
        query = query.order_by(
            desc(Video.viewCount) if order_option == 'desc' else asc(Video.viewCount))
    elif sort_option == 'likes':
        query = query.order_by(
            desc(Video.likeCount) if order_option == 'desc' else asc(Video.likeCount))
    elif sort_option == 'comments':
        query = query.order_by(
            desc(Video.commentCount) if order_option == 'desc' else asc(Video.commentCount))
    videos_info = query.paginate(per_page=15, page=page_num, error_out=True)
    return render_template('videos.html', videos=videos_info, current_page=page_num, search_query=search_query)


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
def process_search_playlist(search_arg):
    search_text = ''.join(c for c in search_arg if c.isalnum() or c == " ")
    search_words = [word.lower() for word in search_text.split()]
    query = Playlist.query
    if search_words:
        conditions = []
        for word in search_words:
            conditions.append(Playlist.title.ilike(f'%{word}%'))
        query = query.filter(or_(*conditions))
    return query, search_text


def process_filter_playlist(query, filter_arg, filter_min_arg, filter_max_arg):
    filter_min_arg = int(filter_min_arg) if filter_min_arg.isdigit() else 0
    filter_max_arg = int(
        filter_max_arg) if filter_max_arg.isdigit() else 1000000000000
    if filter_max_arg < filter_min_arg:
        filter_min_arg, filter_max_arg = 0, 1000000000000
    filter_arg_map = {
        "video count": "videoCount",
        "total views": "totalViews",
        "total likes": "totalLikes",
        "total comments": "totalComments"
    }
    if filter_arg:
        filter_key = getattr(Playlist, filter_arg_map[filter_arg]).between(
            filter_min_arg, filter_max_arg)
        query = query.filter(filter_key)
    return query


def process_sort_playlist(query, page_num, sort_arg, sort_ord):
    sort_arg_map = {
        "title": "title",
        "published at": "publishedAt",
        "video count": "videoCount",
        "total views": "totalViews",
        "total likes": "totalLikes",
        "total comments": "totalComments"
    }
    if sort_arg:
        sort_key = getattr(Playlist, sort_arg_map[sort_arg])
        if sort_arg == "title":
            sort_key = func.lower(getattr(Playlist, sort_arg_map[sort_arg]))
        sort_key.asc()
        if sort_ord == "desc":
            sort_key = sort_key.desc()
        playlists_info = query.order_by(sort_key).paginate(
            per_page=12, page=page_num, error_out=True)
        playlists_info = query.order_by(sort_key).paginate(
            per_page=12, page=page_num, error_out=True)
    else:
        playlists_info = query.paginate(
            per_page=12, page=page_num, error_out=True)
    return playlists_info


@app.route('/playlists/<int:page_num>', methods=['GET'])
def showPlaylist(page_num):
    # Search
    search_arg = request.args.get('search_arg', type=str, default="").strip()
    query, search_text = process_search_playlist(search_arg)
    # Filter
    filter_arg = request.args.get('filter_arg', type=str, default="")
    filter_min_arg = request.args.get(
        'filter_min_arg', type=str, default="").strip()
    filter_max_arg = request.args.get(
        'filter_max_arg', type=str, default="").strip()
    query = process_filter_playlist(
        query, filter_arg, filter_min_arg, filter_max_arg)
    # Sort
    sort_arg = request.args.get('sort_arg', type=str, default="")
    sort_ord = request.args.get('sort_ord', type=str, default="asc")
    playlists_info = process_sort_playlist(query, page_num, sort_arg, sort_ord)
    return render_template(
        'playlists.html', playlists=playlists_info, current_page=page_num, search_arg=search_text,
        filter_arg=filter_arg, filter_min_arg=filter_min_arg, filter_max_arg=filter_max_arg,
        sort_arg=sort_arg, sort_ord=sort_ord
    )


@app.route('/api/playlists/<int:page_num>', methods=['GET'])
def showPlaylistAPI(page_num):
    # Search
    search_arg = request.args.get('search_arg', type=str, default="").strip()
    query, search_text = process_search_playlist(search_arg)
    # Filter
    filter_arg = request.args.get('filter_arg', type=str, default="")
    filter_min_arg = request.args.get(
        'filter_min_arg', type=str, default="").strip()
    filter_max_arg = request.args.get(
        'filter_max_arg', type=str, default="").strip()
    query = process_filter_playlist(
        query, filter_arg, filter_min_arg, filter_max_arg)
    # Sort
    sort_arg = request.args.get('sort_arg', type=str, default="")
    sort_ord = request.args.get('sort_ord', type=str, default="asc")
    playlists_info = process_sort_playlist(query, page_num, sort_arg, sort_ord)
    playlists_info = [playlists.to_dict()
                      for playlists in playlists_info.items]
    per_page = 12
    total_playlists = query.count()
    total_pages = math.ceil(total_playlists / per_page)
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
