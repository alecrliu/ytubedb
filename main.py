"""Routing with queries for each page and API endpoints"""

from flask import render_template, request, jsonify
from flask_cors import CORS
from sqlalchemy import func, or_, and_, desc, asc, func
from sqlalchemy.orm import joinedload
import math
from database import app, db, Channel, Playlist, Video
from gitlabStats import commit_counts, issue_counts


CORS(app)


@app.route('/')
def index():
    """
    splash page
    """
    return render_template('splash.html')


@app.route('/about')
def about():
    """
    about page
    """
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


def process_search_channel(search_arg):
    search_text = ''.join(
        c for c in search_arg if c.isalnum() or c == " " or c == "\"")
    search_words = [word.lower().strip()
                    for word in search_text.split("\"") if word.strip()]
    query = Channel.query
    if search_words:
        conditions = []
        full_text = Channel.channelName + "\n" + Channel.description
        for word in search_words:
            conditions.append(full_text.ilike(f'%{word}%'))
        query = query.filter(and_(*conditions))
    return query, search_text


def process_filter_channel(query, filter_arg, filter_min_arg, filter_max_arg):
    filter_min_arg = int(filter_min_arg) if filter_min_arg.isdigit() else 0
    filter_max_arg = int(
        filter_max_arg) if filter_max_arg.isdigit() else 1000000000000
    if filter_max_arg < filter_min_arg:
        filter_min_arg, filter_max_arg = 0, 1000000000000
    filter_arg_map = {
        "subscribers": "subscriberCount",
        "views": "viewCount",
        "video count": "videoCount"
    }
    if filter_arg:
        filter_key = getattr(Channel, filter_arg_map[filter_arg]).between(
            filter_min_arg, filter_max_arg)
        query = query.filter(filter_key)
    return query


def process_sort_channel(query, sort_arg, sort_ord):
    sort_arg_map = {
        "title": "channelName",
        "subscribers": "subscriberCount",
        "views": "viewCount",
        "video count": "videoCount",
        "creation date": "publishedAt"
    }
    if sort_arg:
        sort_key = getattr(Channel, sort_arg_map[sort_arg])
        if sort_arg == "title":
            sort_key = func.lower(getattr(Channel, sort_arg_map[sort_arg]))
        sort_key.asc()
        if sort_ord == "desc":
            sort_key = sort_key.desc()
        query = query.order_by(sort_key)
    return query


@app.route('/channels/<int:page_num>')
def showChannels(page_num):
    """
    channels page displays multiple channels
    """
    # Search
    search_arg = request.args.get('search_arg', type=str, default="").strip()
    query, search_text = process_search_channel(search_arg)
    # Filter
    filter_arg = request.args.get('filter_arg', type=str, default="")
    filter_min_arg = request.args.get(
        'filter_min_arg', type=str, default="").strip()
    filter_max_arg = request.args.get(
        'filter_max_arg', type=str, default="").strip()
    query = process_filter_channel(
        query, filter_arg, filter_min_arg, filter_max_arg)
    # Sort
    sort_arg = request.args.get('sort_arg', type=str, default="")
    sort_ord = request.args.get('sort_ord', type=str, default="desc")
    query = process_sort_channel(query, sort_arg, sort_ord)
    channels_info = query.paginate(per_page=12, page=page_num, error_out=True)
    return render_template(
        'channels.html', channels=channels_info, current_page=page_num, search_arg=search_text,
        filter_arg=filter_arg, filter_min_arg=filter_min_arg, filter_max_arg=filter_max_arg,
        sort_arg=sort_arg, sort_ord=sort_ord
    )


@app.route('/channel/<string:channelId>')
def showChannel(channelId):
    """
    channel page displays single channel
    """
    channel_info = Channel.query.filter_by(channel_id=channelId).first()
    if channel_info is None:
        return "Channel not found", 404
    videos = Video.query.filter_by(channel_id=channelId).all()
    playlists = Playlist.query.filter_by(channel_id=channelId).all()
    return render_template('channel.html', channel=channel_info, videos=videos, playlists=playlists)


def process_search_video(search_arg):
    search_text = ''.join(
        c for c in search_arg if c.isalnum() or c == " " or c == "\"")
    search_words = [word.lower().strip()
                    for word in search_text.split("\"") if word.strip()]
    query = Video.query
    if search_words:
        conditions = []
        full_text = Video.title + "\n" + Video.description
        for word in search_words:
            conditions.append(full_text.ilike(f'%{word}%'))
        query = query.filter(and_(*conditions))
    return query, search_text


def process_filter_video(query, filter_arg, filter_min_arg, filter_max_arg):
    filter_min_arg = int(filter_min_arg) if filter_min_arg.isdigit() else 0
    filter_max_arg = int(
        filter_max_arg) if filter_max_arg.isdigit() else 1000000000000
    if filter_max_arg < filter_min_arg:
        filter_min_arg, filter_max_arg = 0, 1000000000000
    filter_arg_map = {
        "views": "viewCount",
        "likes": "likeCount",
        "comments": "commentCount"
    }
    if filter_arg:
        filter_key = getattr(Video, filter_arg_map[filter_arg]).between(
            filter_min_arg, filter_max_arg)
        query = query.filter(filter_key)
    return query


def process_sort_video(query, sort_arg, sort_ord):
    sort_arg_map = {
        "title": "title",
        "views": "viewCount",
        "likes": "likeCount",
        "comments": "commentCount",
        "upload date": "publishedAt"
    }
    if sort_arg:
        sort_key = getattr(Video, sort_arg_map[sort_arg])
        if sort_arg == "title":
            sort_key = func.lower(getattr(Video, sort_arg_map[sort_arg]))
        sort_key.asc()
        if sort_ord == "desc":
            sort_key = sort_key.desc()
        query = query.order_by(sort_key)
    return query


@app.route('/videos/<int:page_num>')
def showVideos(page_num):
    """
    videos page displays multiple videos
    """
    # Search
    search_arg = request.args.get('search_arg', type=str, default="").strip()
    query, search_text = process_search_video(search_arg)
    # Filter
    filter_arg = request.args.get('filter_arg', type=str, default="")
    filter_min_arg = request.args.get(
        'filter_min_arg', type=str, default="").strip()
    filter_max_arg = request.args.get(
        'filter_max_arg', type=str, default="").strip()
    query = process_filter_video(
        query, filter_arg, filter_min_arg, filter_max_arg)
    # Sort
    sort_arg = request.args.get('sort_arg', type=str, default="")
    sort_ord = request.args.get('sort_ord', type=str, default="desc")
    query = process_sort_video(query, sort_arg, sort_ord)
    per_page = request.args.get('per_page', type=int, default=12)
    videos_info = query.paginate(
        per_page=per_page, page=page_num, error_out=True)
    return render_template(
        'videos.html', videos=videos_info, current_page=page_num, search_arg=search_text,
        filter_arg=filter_arg, filter_min_arg=filter_min_arg, filter_max_arg=filter_max_arg,
        sort_arg=sort_arg, sort_ord=sort_ord, per_page=per_page
    )


@app.route('/video/<string:videoId>')
def oneVideo(videoId):
    """
    video page displays single video
    """
    video = Video.query.filter_by(video_id=videoId).first()
    channel = None
    playlists = []
    if video is not None:
        channel = video.channels
        playlists = video.inPlaylist
    else:
        return "Video not found", 404
    return render_template('video.html', video=video, channel=channel, playlists=playlists)


def process_search_playlist(search_arg):
    search_text = ''.join(
        c for c in search_arg if c.isalnum() or c == " " or c == "\"")
    search_words = [word.lower().strip()
                    for word in search_text.split("\"") if word.strip()]
    query = Playlist.query
    if search_words:
        conditions = []
        for word in search_words:
            conditions.append(Playlist.title.ilike(f'%{word}%'))
        query = query.filter(and_(*conditions))
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


def process_sort_playlist(query, sort_arg, sort_ord):
    sort_arg_map = {
        "title": "title",
        "creation date": "publishedAt",
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
        query = query.order_by(sort_key)
    return query


@app.route('/playlists/<int:page_num>', methods=['GET'])
def showPlaylist(page_num):
    """
    playlists page displays multiple playlists
    """
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
    sort_ord = request.args.get('sort_ord', type=str, default="desc")
    query = process_sort_playlist(query, sort_arg, sort_ord)
    playlists_info = query.paginate(per_page=12, page=page_num, error_out=True)
    return render_template(
        'playlists.html', playlists=playlists_info, current_page=page_num, search_arg=search_text,
        filter_arg=filter_arg, filter_min_arg=filter_min_arg, filter_max_arg=filter_max_arg,
        sort_arg=sort_arg, sort_ord=sort_ord
    )


@app.route('/playlist/<string:playlistId>')
def playlist(playlistId):
    """
    playlist page displays single playlist
    """
    playlist_info = Playlist.query.filter_by(playlist_id=playlistId).first()
    if playlist_info is None:
        return "Playlist not found", 404
    channel = playlist_info.channels
    videos = playlist_info.videos
    return render_template('playlist.html', playlist=playlist_info, channel=channel, videos=videos)

# APIs


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


@app.route('/api/channels/<int:page_num>', methods=['GET'])
def showChannelsAPI(page_num):
    # Search
    search_arg = request.args.get('search_arg', type=str, default="").strip()
    query, search_text = process_search_channel(search_arg)
    # Filter
    filter_arg = request.args.get('filter_arg', type=str, default="")
    filter_min_arg = request.args.get(
        'filter_min_arg', type=str, default="").strip()
    filter_max_arg = request.args.get(
        'filter_max_arg', type=str, default="").strip()
    query = process_filter_channel(
        query, filter_arg, filter_min_arg, filter_max_arg)
    # Sort
    sort_arg = request.args.get('sort_arg', type=str, default="")
    sort_ord = request.args.get('sort_ord', type=str, default="asc")
    query = process_sort_channel(query, sort_arg, sort_ord)
    per_page = 12
    total_channels = Channel.query.count()
    total_pages = math.ceil(total_channels / per_page)
    channels_info = Channel.query.paginate(
        per_page=12, page=page_num, error_out=True)
    channels = [channel.to_dict() for channel in channels_info.items]
    return jsonify(current_page=page_num, total_pages=total_pages, channels=channels, search_arg=search_text,
                   filter_arg=filter_arg, filter_min_arg=filter_min_arg, filter_max_arg=filter_max_arg,
                   sort_arg=sort_arg, sort_ord=sort_ord)


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


@app.route('/api/videos/<int:page_num>', methods=['GET'])
def showVideosAPI(page_num):
    # Search
    search_arg = request.args.get('search_arg', type=str, default="").strip()
    query, search_text = process_search_video(search_arg)
    # Filter
    filter_arg = request.args.get('filter_arg', type=str, default="")
    filter_min_arg = request.args.get(
        'filter_min_arg', type=str, default="").strip()
    filter_max_arg = request.args.get(
        'filter_max_arg', type=str, default="").strip()
    query = process_filter_video(
        query, filter_arg, filter_min_arg, filter_max_arg)
    # Sort
    sort_arg = request.args.get('sort_arg', type=str, default="")
    sort_ord = request.args.get('sort_ord', type=str, default="asc")
    query = process_sort_video(query, sort_arg, sort_ord)
    per_page = request.args.get('per_page', type=int, default=12)
    videos_info = query.paginate(
        per_page=per_page, page=page_num, error_out=True)
    total_videos = query.count()
    total_pages = math.ceil(total_videos / per_page)
    videos_info = [video.to_dict() for video in videos_info.items]
    return jsonify(current_page=page_num, total_pages=total_pages, videos=videos_info, search_arg=search_text,
                   filter_arg=filter_arg, filter_min_arg=filter_min_arg, filter_max_arg=filter_max_arg,
                   sort_arg=sort_arg, sort_ord=sort_ord)


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
    query = process_sort_playlist(query, sort_arg, sort_ord)
    per_page = 12
    playlists_info = query.paginate(
        per_page=per_page, page=page_num, error_out=True)
    total_playlists = query.count()
    total_pages = math.ceil(total_playlists / per_page)
    playlists_info = [playlist.to_dict() for playlist in playlists_info.items]
    return jsonify(current_page=page_num, total_pages=total_pages, playlists=playlists_info, search_arg=search_text,
                   filter_arg=filter_arg, filter_min_arg=filter_min_arg, filter_max_arg=filter_max_arg,
                   sort_arg=sort_arg, sort_ord=sort_ord)


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
